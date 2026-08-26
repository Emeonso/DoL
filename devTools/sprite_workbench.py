#!/usr/bin/env python3
"""Deterministic sprite compositor and pixel-editing workbench.

The workbench is intentionally recipe-driven.  A recipe describes loose image
layers and explicit edits; running it twice produces the same PNG and preview.
It is designed for DoL's small indexed PNG layers, but does not depend on the
game's source tree or renderer.

Requires Pillow:
    python -m pip install Pillow

Examples:
    python devTools/sprite_workbench.py inspect img/hair/sides/default/short.png
    python devTools/sprite_workbench.py run devTools/sprite_recipe.json
    python devTools/sprite_workbench.py run devTools/sprite_recipe.json --watch
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from PIL import Image, ImageChops, ImageDraw


RGBA = tuple[int, int, int, int]


def rgba(value: Any) -> RGBA:
    if isinstance(value, str):
        value = value.lstrip("#")
        if len(value) == 6:
            value += "ff"
        if len(value) != 8:
            raise ValueError(f"colour must be #RRGGBB or #RRGGBBAA: {value!r}")
        return tuple(int(value[i : i + 2], 16) for i in range(0, 8, 2))  # type: ignore[return-value]
    if isinstance(value, list) and len(value) in (3, 4):
        values = [int(v) for v in value]
        return tuple(values + [255]) if len(values) == 3 else tuple(values)  # type: ignore[return-value]
    raise ValueError(f"invalid colour: {value!r}")


def box(value: Any) -> tuple[int, int, int, int]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError(f"box must be [left, top, right, bottom]: {value!r}")
    return tuple(int(v) for v in value)  # type: ignore[return-value]


def resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def resolve_output(root: Path, value: str) -> Path:
    """Resolve a write path and keep it inside the recipe directory."""
    recipe_root = root.resolve()
    output = resolve(root, value).resolve()
    try:
        output.relative_to(recipe_root)
    except ValueError as error:
        raise ValueError(f"refusing to write outside recipe directory: {output}") from error
    return output


def load_rgba(path: Path) -> Image.Image:
    with Image.open(path) as source:
        image = source.convert("RGBA")
    return image


def parse_layers(recipe: dict[str, Any], root: Path) -> tuple[list["Layer"], tuple[int, int]]:
    layers: list[Layer] = []
    canvas = recipe.get("canvas")
    canvas_size = None
    if canvas:
        canvas_size = (int(canvas["width"]), int(canvas["height"]))

    for index, spec in enumerate(recipe.get("layers", [])):
        if isinstance(spec, str):
            spec = {"path": spec}
        is_new = bool(spec.get("new", False))
        path = resolve(root, spec["path"]) if spec.get("path") else Path("<new-layer>")
        if is_new:
            declared_size = spec.get("size")
            if not declared_size or len(declared_size) != 2:
                raise ValueError(f"new layer {spec.get('name', index)!r} needs size: [width, height]")
            image = Image.new("RGBA", (int(declared_size[0]), int(declared_size[1])), rgba(spec.get("fill", "#00000000")))
        else:
            if not spec.get("path"):
                raise ValueError(f"layer {spec.get('name', index)!r} needs path or new: true")
            image = load_rgba(path)
        if canvas_size is None:
            canvas_size = image.size
        layers.append(
            Layer(
                name=spec.get("name", path.stem or f"layer-{index}"),
                path=path,
                image=image,
                x=int(spec.get("x", 0)),
                y=int(spec.get("y", 0)),
                opacity=float(spec.get("opacity", 1.0)),
            )
        )
    if not layers:
        raise ValueError("recipe must contain at least one layer")
    assert canvas_size is not None
    return layers, canvas_size


@dataclass
class Layer:
    name: str
    path: Path
    image: Image.Image
    x: int = 0
    y: int = 0
    opacity: float = 1.0


def find_layer(layers: Iterable[Layer], name: str) -> Layer:
    for layer in layers:
        if layer.name == name:
            return layer
    available = ", ".join(layer.name for layer in layers)
    raise ValueError(f"unknown layer {name!r}; available: {available}")


def pixel_at(layer: Layer, x: int, y: int) -> RGBA:
    if not (0 <= x < layer.image.width and 0 <= y < layer.image.height):
        raise ValueError(f"pixel ({x}, {y}) is outside layer {layer.name!r} {layer.image.size}")
    return layer.image.getpixel((x, y))  # type: ignore[return-value]


def draw_curved_feather(image: Image.Image, edit: dict[str, Any]) -> int:
    """Rasterise one tapered feather along a quadratic Bezier centreline."""
    root = tuple(float(value) for value in edit["root"])
    control = tuple(float(value) for value in edit["control"])
    tip = tuple(float(value) for value in edit["tip"])
    root_width = float(edit.get("root_width", 1.5))
    mid_width = float(edit.get("mid_width", 4.0))
    tip_width = float(edit.get("tip_width", 0.25))
    samples = max(8, int(edit.get("samples", 20)))
    outline = rgba(edit.get("outline", "#596579ff"))
    fill = rgba(edit.get("colour", "#eef2f7ff"))
    highlight = rgba(edit.get("highlight", "#ffffffff"))
    left: list[tuple[int, int]] = []
    right: list[tuple[int, int]] = []
    centre: list[tuple[int, int]] = []
    for index in range(samples + 1):
        t = index / samples
        one_minus = 1.0 - t
        x = one_minus * one_minus * root[0] + 2 * one_minus * t * control[0] + t * t * tip[0]
        y = one_minus * one_minus * root[1] + 2 * one_minus * t * control[1] + t * t * tip[1]
        dx = 2 * one_minus * (control[0] - root[0]) + 2 * t * (tip[0] - control[0])
        dy = 2 * one_minus * (control[1] - root[1]) + 2 * t * (tip[1] - control[1])
        length = max(0.001, math.hypot(dx, dy))
        normal_x, normal_y = -dy / length, dx / length
        width = root_width * one_minus + tip_width * t + mid_width * math.sin(math.pi * t)
        left.append((round(x + normal_x * width), round(y + normal_y * width)))
        right.append((round(x - normal_x * width), round(y - normal_y * width)))
        centre.append((round(x), round(y)))
    polygon = left + list(reversed(right))
    draw = ImageDraw.Draw(image)
    draw.polygon(polygon, fill=outline)
    inner = polygon
    if len(polygon) >= 6:
        # A one-pixel inset is approximated by narrowing the whole feather.
        inner_edit = dict(edit)
        inner_edit["root_width"] = max(0.4, root_width - 0.8)
        inner_edit["mid_width"] = max(0.8, mid_width - 0.9)
        inner_edit["tip_width"] = max(0.1, tip_width - 0.1)
        inner_edit["outline"] = colour_text(fill)
        inner_edit["colour"] = colour_text(fill)
        inner_edit["highlight"] = colour_text(fill)
        inner_edit["shaft"] = False
        # Inline the narrowed polygon calculation without recursive drawing.
        inner_left: list[tuple[int, int]] = []
        inner_right: list[tuple[int, int]] = []
        for index in range(samples + 1):
            t = index / samples
            one_minus = 1.0 - t
            x = one_minus * one_minus * root[0] + 2 * one_minus * t * control[0] + t * t * tip[0]
            y = one_minus * one_minus * root[1] + 2 * one_minus * t * control[1] + t * t * tip[1]
            dx = 2 * one_minus * (control[0] - root[0]) + 2 * t * (tip[0] - control[0])
            dy = 2 * one_minus * (control[1] - root[1]) + 2 * t * (tip[1] - control[1])
            length = max(0.001, math.hypot(dx, dy))
            normal_x, normal_y = -dy / length, dx / length
            width = max(0.35, (root_width - 0.8) * one_minus + max(0.1, tip_width - 0.1) * t + max(0.8, mid_width - 0.9) * math.sin(math.pi * t))
            inner_left.append((round(x + normal_x * width), round(y + normal_y * width)))
            inner_right.append((round(x - normal_x * width), round(y - normal_y * width)))
        inner = inner_left + list(reversed(inner_right))
        draw.polygon(inner, fill=fill)
    if edit.get("shaft", True):
        shaft_start = max(0, int(samples * 0.08))
        shaft_end = max(shaft_start + 1, int(samples * 0.82))
        draw.line(centre[shaft_start:shaft_end], fill=highlight, width=1)
    return len(polygon) + len(inner)


def apply_edit(layer: Layer, edit: dict[str, Any]) -> int:
    op = edit["op"]
    changed = 0
    if op == "feather":
        return draw_curved_feather(layer.image, edit)
    if op in ("pixel", "erase"):
        x, y = int(edit["x"]), int(edit["y"])
        before = pixel_at(layer, x, y)
        after = (0, 0, 0, 0) if op == "erase" else rgba(edit["colour"])
        if before != after:
            layer.image.putpixel((x, y), after)
            changed = 1
        return changed

    if op == "replace":
        source = rgba(edit["from"])
        target = rgba(edit["to"])
        for y in range(layer.image.height):
            for x in range(layer.image.width):
                if layer.image.getpixel((x, y)) == source:
                    layer.image.putpixel((x, y), target)
                    changed += 1
        return changed

    if op == "shift":
        left, top, right, bottom = box(edit["box"])
        dx, dy = int(edit.get("dx", 0)), int(edit.get("dy", 0))
        if not (0 <= left <= right <= layer.image.width and 0 <= top <= bottom <= layer.image.height):
            raise ValueError(f"shift box outside layer {layer.name!r}: {edit['box']}")
        region = layer.image.crop((left, top, right, bottom))
        layer.image.paste((0, 0, 0, 0), (left, top, right, bottom))
        destination = (left + dx, top + dy, right + dx, bottom + dy)
        clipped = (max(0, destination[0]), max(0, destination[1]), min(layer.image.width, destination[2]), min(layer.image.height, destination[3]))
        if clipped[0] < clipped[2] and clipped[1] < clipped[3]:
            source_crop = region.crop((clipped[0] - destination[0], clipped[1] - destination[1], clipped[2] - destination[0], clipped[3] - destination[1]))
            layer.image.alpha_composite(source_crop, (clipped[0], clipped[1]))
        return max(0, (right - left) * (bottom - top))

    if op == "mirror":
        left, top, right, bottom = box(edit["box"])
        target_x = int(edit["target_x"])
        if not (0 <= left <= right <= layer.image.width and 0 <= top <= bottom <= layer.image.height):
            raise ValueError(f"mirror box outside layer {layer.name!r}: {edit['box']}")
        width = right - left
        if not (0 <= target_x <= target_x + width <= layer.image.width):
            raise ValueError(f"mirror target outside layer {layer.name!r}: {target_x}")
        source = [[layer.image.getpixel((x, y)) for x in range(left, right)] for y in range(top, bottom)]
        for row, y in zip(source, range(top, bottom)):
            for offset, colour in enumerate(reversed(row)):
                layer.image.putpixel((target_x + offset, y), colour)
        return width * (bottom - top)

    if op == "copy":
        left, top, right, bottom = box(edit["box"])
        target_x = int(edit.get("target_x", left))
        target_y = int(edit.get("target_y", top))
        if not (0 <= left <= right <= layer.image.width and 0 <= top <= bottom <= layer.image.height):
            raise ValueError(f"copy box outside layer {layer.name!r}: {edit['box']}")
        width, height = right - left, bottom - top
        if not (0 <= target_x <= target_x + width <= layer.image.width and 0 <= target_y <= target_y + height <= layer.image.height):
            raise ValueError(f"copy target outside layer {layer.name!r}: ({target_x}, {target_y})")
        region = layer.image.crop((left, top, right, bottom))
        layer.image.paste(region, (target_x, target_y))
        return width * height

    if op == "rect":
        left, top, right, bottom = box(edit["box"])
        colour = rgba(edit.get("colour", "#00000000"))
        fill = edit.get("fill", True)
        draw = ImageDraw.Draw(layer.image)
        draw.rectangle((left, top, right - 1, bottom - 1), fill=colour if fill else None, outline=None if fill else colour, width=1)
        return max(0, (right - left) * (bottom - top)) if fill else max(0, 2 * (right - left) + 2 * (bottom - top) - 4)

    if op in ("polygon", "line", "ellipse"):
        draw = ImageDraw.Draw(layer.image)
        colour = rgba(edit.get("colour", "#00000000"))
        width = max(1, int(edit.get("width", 1)))
        if op == "polygon":
            points = [tuple(int(value) for value in point) for point in edit["points"]]
            draw.polygon(points, fill=colour if edit.get("fill", True) else None, outline=colour if edit.get("outline", False) else None)
            return len(points)
        if op == "line":
            points = [tuple(int(value) for value in point) for point in edit["points"]]
            draw.line(points, fill=colour, width=width, joint="curve")
            return max(1, len(points) - 1) * width
        left, top, right, bottom = box(edit["box"])
        draw.ellipse((left, top, right - 1, bottom - 1), fill=colour if edit.get("fill", True) else None, outline=colour if edit.get("outline", False) else None, width=width)
        return max(1, (right - left) * (bottom - top))

    raise ValueError(f"unknown edit operation: {op!r}")


def compose(layers: list[Layer], size: tuple[int, int]) -> Image.Image:
    output = Image.new("RGBA", size, (0, 0, 0, 0))
    for layer in layers:
        image = layer.image
        if layer.opacity != 1.0:
            image = image.copy()
            alpha = image.getchannel("A").point(lambda value: int(value * layer.opacity))
            image.putalpha(alpha)
        output.alpha_composite(image, (layer.x, layer.y))
    return output


def save_png(image: Image.Image, path: Path, recipe: dict[str, Any], root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = recipe.get("output_mode", "RGBA").upper()
    if mode == "PRESERVE_PALETTE":
        palette_source = resolve(root, recipe["palette_from"])
        with Image.open(palette_source) as source:
            # Keep the source's actual indexed palette for copy-and-edit
            # exports.  Adaptive quantization is only needed for non-indexed
            # palette sources.
            palette = source.copy().convert("P") if source.mode == "P" else source.convert("RGB").quantize(colors=256)
        # Pillow cannot quantize RGBA directly.  Quantize RGB, then rebuild a
        # palette transparency table from the edited image's alpha channel.
        indexed = image.convert("RGB").quantize(palette=palette, dither=Image.Dither.NONE)
        alpha_by_index = [255] * 256
        for index, alpha in zip(indexed.tobytes(), image.getchannel("A").tobytes()):
            alpha_by_index[index] = min(alpha_by_index[index], alpha)
        if min(alpha_by_index) < 255:
            indexed.info["transparency"] = bytes(alpha_by_index)
        image = indexed
    elif mode != "RGBA":
        raise ValueError("output_mode must be RGBA or preserve_palette")
    image.save(path, format="PNG", optimize=False)


def preview_image(image: Image.Image, scale: int, grid: bool) -> Image.Image:
    preview = image.resize((image.width * scale, image.height * scale), Image.Resampling.NEAREST)
    if grid and scale >= 4:
        draw = ImageDraw.Draw(preview)
        line = (255, 255, 255, 45)
        for x in range(0, preview.width, scale):
            draw.line((x, 0, x, preview.height), fill=line)
        for y in range(0, preview.height, scale):
            draw.line((0, y, preview.width, y), fill=line)
    return preview


def render_diff(current: Image.Image, reference: Image.Image) -> Image.Image:
    if current.size != reference.size:
        raise ValueError(f"diff images have different sizes: {current.size} vs {reference.size}")
    diff = ImageChops.difference(current, reference)
    # Make small differences easy to see while retaining alpha.
    return diff.point(lambda value: min(255, value * 4))


def checkerboard(size: tuple[int, int], tile: int = 16) -> Image.Image:
    image = Image.new("RGBA", size, (45, 45, 45, 255))
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if ((x // tile) + (y // tile)) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(70, 70, 70, 255))
    return image


def visible_image(image: Image.Image, scale: int) -> Image.Image:
    return preview_image(Image.alpha_composite(checkerboard(image.size, max(4, scale * 2)), image), scale, False)


def make_contact_sheet(layers: list[Layer], result: Image.Image, scale: int) -> Image.Image:
    entries: list[tuple[str, Image.Image]] = [("COMPOSITE", result)]
    entries.extend((layer.name, layer.image) for layer in layers)
    tiles = []
    label_height = max(24, scale * 8)
    for name, image in entries:
        if image.size != result.size:
            canvas = Image.new("RGBA", result.size, (0, 0, 0, 0))
            crop = image.crop((0, 0, min(image.width, result.width), min(image.height, result.height)))
            canvas.alpha_composite(crop)
            image = canvas
        tile = Image.new("RGBA", (result.width * scale, result.height * scale + label_height), (25, 25, 25, 255))
        tile.alpha_composite(visible_image(image, scale), (0, label_height))
        ImageDraw.Draw(tile).text((6, 5), name, fill=(255, 255, 255, 255))
        tiles.append(tile)
    columns = 2
    rows = (len(tiles) + columns - 1) // columns
    sheet = Image.new("RGBA", (tiles[0].width * columns, tiles[0].height * rows), (15, 15, 15, 255))
    for index, tile in enumerate(tiles):
        sheet.alpha_composite(tile, ((index % columns) * tile.width, (index // columns) * tile.height))
    return sheet


def write_pixel_grid(image: Image.Image, path: Path) -> None:
    alpha = image.getchannel("A")
    bounds = alpha.getbbox() or (0, 0, image.width, image.height)
    left, top, right, bottom = bounds
    colours = image.crop(bounds).getcolors(maxcolors=1_000_000) or []
    opaque = [(count, colour) for count, colour in colours if colour[3] > 0]
    opaque.sort(reverse=True)
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    colour_symbols: dict[RGBA, str] = {}
    legend: list[str] = []
    for index, (_count, colour) in enumerate(opaque[: len(symbols)]):
        char = symbols[index]
        colour_symbols[colour] = char
        legend.append(f"  {char} = {colour_text(colour)}")
    lines = [f"bounds: x={left}..{right - 1}, y={top}..{bottom - 1}", "legend: . transparent, + partial alpha"] + legend
    lines.append("")
    for y in range(top, bottom):
        row = []
        for x in range(left, right):
            colour = image.getpixel((x, y))
            if colour[3] == 0:
                row.append(".")
            elif colour[3] < 255:
                row.append("+")
            else:
                row.append(colour_symbols.get(colour, "#"))
        lines.append(f"{y:03d} " + "".join(row))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def snapshot_recipe(recipe_path: Path) -> list[Path]:
    recipe = load_recipe(recipe_path)
    root = recipe_path.parent
    layers, size = parse_layers(recipe, root)
    operation_counts: list[int] = []
    for edit in recipe.get("edits", []):
        operation_counts.append(apply_edit(find_layer(layers, edit["layer"]), edit))
    result = compose(layers, size)
    folder = resolve_output(root, recipe.get("inspection_dir", f"out/{recipe_path.stem}-inspection"))
    folder.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    final_path = folder / "composite.png"
    save_png(result, final_path, recipe, root)
    outputs.append(final_path)
    outputs.extend(export_layers(recipe, layers, root))
    scale = int(recipe.get("inspection_scale", recipe.get("preview_scale", 8)))
    preview_path = folder / f"composite-{scale}x.png"
    visible_image(result, scale).save(preview_path, format="PNG", optimize=False)
    outputs.append(preview_path)
    contact_path = folder / "layers-contact-sheet.png"
    make_contact_sheet(layers, result, max(1, int(recipe.get("contact_scale", 2)))).save(contact_path, format="PNG", optimize=False)
    outputs.append(contact_path)

    grid_layer = recipe.get("grid_layer", "composite")
    grid_image = result if grid_layer == "composite" else find_layer(layers, grid_layer).image
    grid_path = folder / f"{grid_layer.replace(' ', '_')}-pixel-grid.txt"
    write_pixel_grid(grid_image, grid_path)
    outputs.append(grid_path)

    alpha = result.getchannel("A")
    report = {
        "recipe": str(recipe_path),
        "canvas": {"width": size[0], "height": size[1]},
        "layers": [{"name": layer.name, "path": str(layer.path), "size": list(layer.image.size), "x": layer.x, "y": layer.y, "opacity": layer.opacity} for layer in layers],
        "edits": len(recipe.get("edits", [])),
        "edit_operation_pixel_counts": operation_counts,
        "composite_nontransparent_bounds": list(alpha.getbbox() or []),
        "grid_layer": grid_layer,
        "outputs": [str(path) for path in outputs] + [str(folder / "report.json")],
    }
    report_path = folder / "report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    outputs.append(report_path)
    print(f"{recipe_path}: inspection snapshot")
    for path in outputs:
        print(f"  wrote {path}")
    return outputs


def export_layers(recipe: dict[str, Any], layers: list[Layer], root: Path) -> list[Path]:
    """Write explicitly requested new layer assets without touching sources."""
    outputs: list[Path] = []
    for export in recipe.get("exports", []):
        layer = find_layer(layers, export["layer"])
        output = resolve_output(root, export["path"])
        source_path = layer.path.resolve() if layer.path.exists() else None
        if source_path and output.resolve() == source_path:
            raise ValueError(f"refusing to export over source layer {source_path}")
        export_recipe = {
            "output_mode": export.get("mode", "preserve_palette" if source_path else "RGBA"),
        }
        palette_from = export.get("palette_from")
        if palette_from:
            export_recipe["palette_from"] = palette_from
        elif source_path:
            export_recipe["palette_from"] = str(source_path)
        if export_recipe["output_mode"].upper() == "PRESERVE_PALETTE" and "palette_from" not in export_recipe:
            raise ValueError(f"palette-preserving export for {layer.name!r} needs palette_from")
        save_png(layer.image, output, export_recipe, root)
        outputs.append(output)
        print(f"  exported {layer.name} -> {output}")
    return outputs


def run_recipe(recipe_path: Path) -> list[Path]:
    with recipe_path.open(encoding="utf-8") as stream:
        recipe = json.load(stream)
    root = recipe_path.parent
    layers, size = parse_layers(recipe, root)
    edits = recipe.get("edits", [])
    changed = 0
    for edit in edits:
        layer = find_layer(layers, edit["layer"])
        changed += apply_edit(layer, edit)
    result = compose(layers, size)

    output_value = recipe.get("output", f"out/{recipe_path.stem}.png")
    output = resolve_output(root, output_value)
    save_png(result, output, recipe, root)
    outputs = [output]
    outputs.extend(export_layers(recipe, layers, root))

    preview_value = recipe.get("preview")
    if preview_value:
        preview = resolve_output(root, preview_value)
        preview_image(result, int(recipe.get("preview_scale", 8)), bool(recipe.get("grid", False))).save(preview, format="PNG", optimize=False)
        outputs.append(preview)

    reference_value = recipe.get("diff_against")
    if reference_value:
        reference = load_rgba(resolve(root, reference_value))
        diff_value = recipe.get("diff_output", f"out/{recipe_path.stem}-diff.png")
        diff = resolve_output(root, diff_value)
        render_diff(result, reference).save(diff, format="PNG", optimize=False)
        outputs.append(diff)

    print(f"{recipe_path}: {len(edits)} edits, {changed} pixel operations")
    for path in outputs:
        print(f"  wrote {path}")
    return outputs


def load_recipe(recipe_path: Path) -> dict[str, Any]:
    with recipe_path.open(encoding="utf-8") as stream:
        return json.load(stream)


def build_recipe_state(recipe: dict[str, Any], root: Path, extra_edits: list[dict[str, Any]] | None = None) -> tuple[list[Layer], tuple[int, int]]:
    layers, size = parse_layers(recipe, root)
    edits = list(recipe.get("edits", [])) + list(extra_edits or [])
    for edit in edits:
        apply_edit(find_layer(layers, edit["layer"]), edit)
    return layers, size


def colour_text(value: RGBA) -> str:
    return "#" + "".join(f"{part:02x}" for part in value)


class SpriteEditor:
    """Small Tk editor that records clicks as deterministic recipe edits."""

    def __init__(self, recipe_path: Path):
        try:
            import tkinter as tk
            from tkinter import colorchooser, ttk
        except ImportError as error:
            raise RuntimeError("Tkinter is required for the edit command") from error

        self.tk = tk
        self.colorchooser = colorchooser
        self.ttk = ttk
        self.recipe_path = recipe_path.resolve()
        self.recipe = load_recipe(self.recipe_path)
        self.session_edits: list[dict[str, Any]] = []
        self.zoom = int(self.recipe.get("editor_zoom", self.recipe.get("preview_scale", 8)))
        self.grid = True
        self.last_pixel: tuple[str, int, int] | None = None
        self.layers, self.size = build_recipe_state(self.recipe, self.recipe_path.parent)

        self.window = tk.Tk()
        self.window.title(f"Sprite Workbench - {self.recipe_path.name}")
        self.window.minsize(760, 520)
        self.window.bind("<Control-s>", lambda _event: self.save())
        self.window.bind("<Control-z>", lambda _event: self.undo())

        controls = ttk.Frame(self.window, padding=6)
        controls.pack(fill="x")
        self.layer_var = tk.StringVar(value=self.layers[-1].name)
        self.tool_var = tk.StringVar(value="pencil")
        self.colour_var = tk.StringVar(value="#ff8d8fff")
        self.zoom_var = tk.IntVar(value=self.zoom)
        self.grid_var = tk.BooleanVar(value=True)

        ttk.Label(controls, text="Layer").pack(side="left")
        self.layer_menu = ttk.Combobox(controls, textvariable=self.layer_var, values=[layer.name for layer in self.layers], state="readonly", width=18)
        self.layer_menu.pack(side="left", padx=(4, 10))
        self.layer_menu.bind("<<ComboboxSelected>>", lambda _event: self.status("Active layer changed"))
        ttk.Label(controls, text="Tool").pack(side="left")
        tool_menu = ttk.Combobox(controls, textvariable=self.tool_var, values=["pencil", "eraser"], state="readonly", width=9)
        tool_menu.pack(side="left", padx=(4, 10))
        ttk.Label(controls, text="Colour").pack(side="left")
        colour_entry = ttk.Entry(controls, textvariable=self.colour_var, width=11)
        colour_entry.pack(side="left", padx=(4, 3))
        ttk.Button(controls, text="Choose", command=self.choose_colour).pack(side="left", padx=(0, 10))
        ttk.Button(controls, text="Save recipe", command=self.save).pack(side="left", padx=2)
        ttk.Button(controls, text="Undo", command=self.undo).pack(side="left", padx=2)
        ttk.Label(controls, text="Zoom").pack(side="left", padx=(12, 3))
        zoom_spin = ttk.Spinbox(controls, from_=1, to=32, textvariable=self.zoom_var, width=4, command=self.redraw)
        zoom_spin.pack(side="left")
        ttk.Checkbutton(controls, text="Grid", variable=self.grid_var, command=self.redraw).pack(side="left", padx=8)

        canvas_frame = ttk.Frame(self.window)
        canvas_frame.pack(fill="both", expand=True, padx=6, pady=(0, 4))
        self.canvas = tk.Canvas(canvas_frame, background="#202020", highlightthickness=0)
        horizontal = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        vertical = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=horizontal.set, yscrollcommand=vertical.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        canvas_frame.rowconfigure(0, weight=1)
        canvas_frame.columnconfigure(0, weight=1)
        self.canvas.bind("<Button-1>", self.paint)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-3>", self.sample)
        self.canvas.bind("<Motion>", self.motion)
        self.status_var = tk.StringVar(value="Left-click paints; right-click samples; Ctrl+S saves; Ctrl+Z undoes")
        ttk.Label(self.window, textvariable=self.status_var, anchor="w", padding=(6, 3)).pack(fill="x")
        self.photo = None
        self.redraw()

    def status(self, message: str) -> None:
        self.status_var.set(message)

    def selected_layer(self) -> Layer:
        return find_layer(self.layers, self.layer_var.get())

    def display_image(self) -> Image.Image:
        image = compose(self.layers, self.size)
        checker = Image.new("RGBA", self.size, (45, 45, 45, 255))
        checker_draw = ImageDraw.Draw(checker)
        tile = max(4, min(16, self.zoom * 2))
        for y in range(0, self.size[1], tile):
            for x in range(0, self.size[0], tile):
                if ((x // tile) + (y // tile)) % 2:
                    checker_draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(70, 70, 70, 255))
        return Image.alpha_composite(checker, image)

    def redraw(self) -> None:
        self.zoom = max(1, min(32, int(self.zoom_var.get())))
        image = preview_image(self.display_image(), self.zoom, bool(self.grid_var.get()) and self.zoom >= 4)
        # Use an in-memory PNG so this works consistently across Tk builds.
        import io
        buffer = io.BytesIO()
        image.save(buffer, format="PNG", optimize=False)
        self.photo = self.tk.PhotoImage(data=buffer.getvalue())
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        self.canvas.configure(scrollregion=(0, 0, image.width, image.height))

    def canvas_pixel(self, event: Any) -> tuple[int, int] | None:
        x = int(self.canvas.canvasx(event.x) // self.zoom)
        y = int(self.canvas.canvasy(event.y) // self.zoom)
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            return x, y
        return None

    def paint(self, event: Any) -> None:
        point = self.canvas_pixel(event)
        if point is None:
            return
        layer = self.selected_layer()
        x, y = point[0] - layer.x, point[1] - layer.y
        if not (0 <= x < layer.image.width and 0 <= y < layer.image.height):
            self.status(f"Canvas pixel {point} is outside layer {layer.name}")
            return
        marker = (layer.name, x, y)
        if marker == self.last_pixel:
            return
        self.last_pixel = marker
        if self.tool_var.get() == "eraser":
            edit = {"op": "erase", "layer": layer.name, "x": x, "y": y}
        else:
            try:
                edit = {"op": "pixel", "layer": layer.name, "x": x, "y": y, "colour": colour_text(rgba(self.colour_var.get()))}
            except ValueError as error:
                self.status(str(error))
                return
        if pixel_at(layer, x, y) == ((0, 0, 0, 0) if edit["op"] == "erase" else rgba(edit["colour"])):
            return
        self.session_edits.append(edit)
        self.layers, self.size = build_recipe_state(self.recipe, self.recipe_path.parent, self.session_edits)
        self.redraw()
        self.status(f"Edited {layer.name} ({x}, {y}); {len(self.session_edits)} unsaved edits")

    def sample(self, event: Any) -> None:
        point = self.canvas_pixel(event)
        if point is None:
            return
        layer = self.selected_layer()
        x, y = point[0] - layer.x, point[1] - layer.y
        if 0 <= x < layer.image.width and 0 <= y < layer.image.height:
            self.colour_var.set(colour_text(pixel_at(layer, x, y)))
            self.tool_var.set("pencil")
            self.status(f"Sampled {self.colour_var.get()} from {layer.name} ({x}, {y})")

    def motion(self, event: Any) -> None:
        point = self.canvas_pixel(event)
        if point is not None:
            self.status(f"Canvas pixel: {point[0]}, {point[1]}")

    def choose_colour(self) -> None:
        selected = self.colorchooser.askcolor(title="Sprite colour")
        if selected[1]:
            self.colour_var.set(selected[1] + "ff")

    def undo(self) -> None:
        if self.session_edits:
            self.session_edits.pop()
            self.layers, self.size = build_recipe_state(self.recipe, self.recipe_path.parent, self.session_edits)
            self.redraw()
            self.status(f"Undid last edit; {len(self.session_edits)} unsaved edits remain")
        else:
            self.status("Nothing to undo")

    def save(self) -> None:
        self.recipe["edits"] = list(self.recipe.get("edits", [])) + self.session_edits
        with self.recipe_path.open("w", encoding="utf-8", newline="\n") as stream:
            json.dump(self.recipe, stream, indent=2)
            stream.write("\n")
        self.session_edits = []
        self.layers, self.size = build_recipe_state(self.recipe, self.recipe_path.parent)
        run_recipe(self.recipe_path)
        self.redraw()
        self.status(f"Saved recipe and rendered outputs: {self.recipe_path}")

    def start(self) -> None:
        self.window.mainloop()


def inspect(path: Path) -> None:
    with Image.open(path) as image:
        rgba_image = image.convert("RGBA")
        colours = rgba_image.getcolors(maxcolors=1_000_000) or []
        alpha = rgba_image.getchannel("A")
        bbox = alpha.getbbox()
        print(f"path: {path}")
        print(f"format: {image.format}, mode: {image.mode}, size: {image.size}")
        print(f"colours: {len(colours)}, nontransparent bounds: {bbox}")
        print(f"alpha values: {len(set(alpha.tobytes()))}")
        if image.mode == "P" and "transparency" in image.info:
            print(f"palette transparency: {image.info['transparency']!r}")
        print("most common colours:")
        for count, colour in sorted(colours, reverse=True)[:12]:
            print(f"  {count:6d} {colour}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)
    inspect_parser = subparsers.add_parser("inspect", help="print dimensions, alpha, bounds, and palette information")
    inspect_parser.add_argument("image", type=Path)
    run_parser = subparsers.add_parser("run", help="run a deterministic JSON recipe")
    run_parser.add_argument("recipe", type=Path)
    run_parser.add_argument("--watch", action="store_true", help="rerun when the recipe or its inputs change")
    run_parser.add_argument("--interval", type=float, default=0.5)
    edit_parser = subparsers.add_parser("edit", help="open the coordinate-grid editor for a JSON recipe")
    edit_parser.add_argument("recipe", type=Path)
    snapshot_parser = subparsers.add_parser("snapshot", help="emit AI-readable previews, layer sheet, pixel grid, and report")
    snapshot_parser.add_argument("recipe", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "inspect":
            inspect(args.image)
            return 0
        if args.command == "edit":
            SpriteEditor(args.recipe).start()
            return 0
        if args.command == "snapshot":
            snapshot_recipe(args.recipe)
            return 0
        if args.command == "run":
            if not args.watch:
                run_recipe(args.recipe)
                return 0
            last_signature = None
            print("watching; press Ctrl+C to stop")
            while True:
                recipe_mtime = args.recipe.stat().st_mtime_ns
                with args.recipe.open(encoding="utf-8") as stream:
                    recipe = json.load(stream)
                input_paths = [args.recipe] + [resolve(args.recipe.parent, layer["path"] if isinstance(layer, dict) else layer) for layer in recipe.get("layers", [])]
                signature = tuple((path, path.stat().st_mtime_ns) for path in input_paths if path.exists())
                if signature != last_signature:
                    run_recipe(args.recipe)
                    last_signature = signature
                time.sleep(max(0.05, args.interval))
    except KeyboardInterrupt:
        print("stopped")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as error:
        print(f"sprite_workbench: error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
