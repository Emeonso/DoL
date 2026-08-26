#!/usr/bin/env python3
import fileinput
import re
import sys

WARNING = '\033[93m'
ENDC = '\033[0m'

def myprint(*args):
	global filename
	print(WARNING, filename + ":", ENDC,*args)

def yield_line_and_islastline(f):
	global filename
	global linenumber
	try:
		prevline = next(f)
		filename = fileinput.filename()
		linenumber = fileinput.filelineno()
	except StopIteration:
		return
	for line in f:
		yield (prevline, f.isfirstline())
		filename = fileinput.filename()
		linenumber = fileinput.filelineno()
		prevline = line
	yield prevline, True

pattern = re.compile(r'(<<(\/?) *(if|for|else|elseif|switch|case|replace|link)\b.*?>>)')

def mask_html_comments(line, in_comment):
	"""Replace HTML comment contents with spaces without changing line text."""
	output = []
	position = 0

	while position < len(line):
		if in_comment:
			end = line.find("-->", position)
			if end == -1:
				output.append(" " * (len(line) - position))
				return "".join(output), True
			output.append(" " * (end + 3 - position))
			position = end + 3
			in_comment = False
			continue

		start = line.find("<!--", position)
		if start == -1:
			output.append(line[position:])
			break

		output.append(line[position:start])
		end = line.find("-->", start + 4)
		if end == -1:
			output.append(" " * (len(line) - start))
			return "".join(output), True
		output.append(" " * (end + 3 - start))
		position = end + 3

	return "".join(output), in_comment

tagfound = []
in_html_comment = False
try:
	for raw_line, isLastLine in yield_line_and_islastline(fileinput.input()):
		line, in_html_comment = mask_html_comments(raw_line, in_html_comment)
		for (whole,end,tag) in re.findall(pattern,line):
			if tag in ("else", "elseif", "case"):
				if len(tagfound) == 0:
					myprint("Found", tag, "but with no opening tag:")
					myprint("  ", linenumber,":", whole)
					fileinput.nextfile()
				lasttag = tagfound[-1]
				if (tag in ("else", "elseif") and lasttag["tag"] != "if") or (tag == "case" and lasttag["tag"] != "switch"):
					myprint("Mismatched else: Opening tag was:")
					myprint("  ",lasttag["linenumber"],":", lasttag["whole"])
					myprint("But this tag was:")
					myprint("  ",linenumber,":", whole)
					fileinput.nextfile()
					break
			elif end != '/':
				tagfound.append({"whole": whole, "linenumber":linenumber,"tag":tag})
			else:
				if len(tagfound) == 0:
					myprint("Found closing tag but with no opening tag:")
					myprint("  ", linenumber,":", whole)
					fileinput.nextfile()
					break
				lasttag = tagfound.pop()
				if lasttag["tag"] != tag:
					myprint("Mismatched tag: Opening tag was:")
					myprint("  ",lasttag["linenumber"],":", lasttag["whole"])
					myprint("Closing tag was:")
					myprint("  ",linenumber,":", whole)
					fileinput.nextfile()
					break

		if isLastLine:
			if len(tagfound) != 0:
				myprint("End of file found but", len(tagfound), ("tag hasn't" if len(tagfound)==1 else "tags haven't"), "been closed:")
			for tag in tagfound:
				myprint("  ", tag["linenumber"],":", tag["whole"])
			tagfound = []
except UnicodeDecodeError as e:
	myprint(e)
	print("   Hint: In Linux, you can get more details about Unicode errors by running:")
	print("	 isutf8", fileinput.filename())
	print("   :Note it might be caused by ", filename)
