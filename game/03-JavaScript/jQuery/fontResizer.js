/*
	Resizes text to fit inside an element.
	Optionally add a margin.
*/

(function ($) {
	$.fn.fontResizer = function (options) {
		const settings = $.extend(
			{
				margin: 2, // Default margin before overflow
			},
			options
		);

		return this.each(function () {
			const container = $(this);
			const previousBinding = container.data("dolFontResizer");
			if (previousBinding) {
				$(window).off("resize" + previousBinding.namespace);
				clearTimeout(previousBinding.initialTimer);
			}
			const resizeHandler = () => {
				if (!container.data("originalSize")) {
					container.data("originalSize", parseFloat(container.css("font-size")));
				}
				const originalSize = container.data("originalSize");
				container.css("font-size", originalSize + "px");

				const contWidth = container.innerWidth();
				let totalTextWidth = 0;

				container.children().each(function () {
					totalTextWidth += $(this)[0].scrollWidth;
				});

				if (totalTextWidth === 0) {
					totalTextWidth = container[0].scrollWidth;
				}

				const desiredFontSize = ((contWidth - settings.margin) * originalSize) / totalTextWidth;
				const newFontSize = Math.min(desiredFontSize, originalSize).toFixed(2);
				container.css("font-size", newFontSize + "px");
			};

			const namespace = ".dolFontResizer" + (container[0].id ? "_" + container[0].id.replace(/[^a-zA-Z0-9_]/g, "_") : "_" + Math.random().toString(36).slice(2));
			$(window).off("resize" + namespace).on("resize" + namespace, $.debounce(100, resizeHandler));
			const initialTimer = setTimeout(resizeHandler, 0);
			container.data("dolFontResizer", { namespace, initialTimer });
		});
	};
})(jQuery);
