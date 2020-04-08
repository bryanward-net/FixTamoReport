#!python
import os, sys, getopt, re

def help():
	print("Usage:")
	print('\n\tFixTamoReport.py -i <inputfile>')



def main(argv):
	##### Setup
	filename = None
	try:
		opts, args = getopt.getopt(argv,"hi:",["ifile="])
	except getopt.GetoptError:
		help()
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			help()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			filename = arg
	if not filename:
		print('File not specified!\n')
		help()
		sys.exit(1)
	
	print('Input file is ', filename)


	try:
		filedata = None
		with open(filename, "r") as file:
			filedata = file.read()
		#Exiting the WITH block closes the file automatically
	except:
		print('Error reading file "', filename)
		sys.exit(1)

	#Change Title of Report for Consistency
	newtitle = ""
	print()
	print("Title of report:")
	print("\t1\tWiFi Survey Report")
	print("\t2\tWiFi Prediction Report")
	print("\t3\tCUSTOM TITLE")
	userchoice = input("Enter Selection: ")
	if userchoice == "1":
		newtitle = "WiFi Survey Report"
	elif userchoice == "2":
		newtitle = "WiFi Prediction Report"
	else:
		newtitle = input("Enter Title: ")
	filedata = re.sub(r'<h1.*?>(.+?)</h1>', r'<h1>' + newtitle + '</h1>', filedata)



	#Add Subtitle
	newtitle = ""
	print()
	newtitle = input("Enter New Subtitle [blank for none]: ")
	filedata = re.sub(r'<div class="title_page">\n<h1>(.*)</h1>\n<hr/>\n<h2>(.*)</h2>', r'<div class="title_page">\n<h1>\1</h1>\n<hr/>\n<h2>' + newtitle + '</h2>', filedata)

	#Remove blue background color
	strFind = '</head>'
	strRepl = '<style>body {background-color: #FFFFFF !important;}</style>\n</head>'
	filedata = filedata.replace(strFind, strRepl)

	#Add new CSS
	strFind = '</style>'
	strRepl = ' .page, .title_page { width: 8.5in !important; height: 11in !important; max-width: 8.5in !important; max-height: 11in !important; padding: 0.25in; margin: .25in auto; text-align: center; overflow: hidden; } img:not(.logoimg) { max-height: 7.5in !important; max-width: 7.5in !important; height: auto !important; width: auto !important; } @page { size: letter; margin: 0; } @media print { html, body { width: 8.5in; height: 11in; } .page, .title_page { margin: 0; border: initial; border-radius: initial; width: initial; min-height: initial; box-shadow: initial; background: initial; page-break-after: always; max-width: 8.5in !important; max-height: 11in !important; text-align: center; } img:not(.logoimg) { max-height: 7.5in !important; max-width: 7.5in !important; height: auto !important; width: auto !important; } }</style>'
	filedata = filedata.replace(strFind, strRepl)

	#Remove AP Color Market from Tables
	filedata = re.sub(r'<td class="col1 marker" style="(.*)background-color:\#......"(.*)></td>', r'<td class="col1 marker" style="\1\2"></td>', filedata)


	#Insert Page Break and Header before "List of APs"
#	strInst = None
#	for line in filedata.splitlines():
#		if line.startswith('<p class="header">'):
#			if not line.startswith('<p class="header"></p>'):
#				strInst = line
#				break
#	if strInst:
#		strFind = '<h2>List of APs</h2>'
#		strRepl = '</div><div class="page">\n' + strInst + '\n<h2>List of APs</h2>'
#		filedata = filedata.replace(strFind, strRepl)
#	else:
#		print("Header text not found!?")
#		exit(3)

	#Insert Page Break before "List of APs"
	strFind = '<h2>List of APs</h2>'
	strRepl = '</div><div class="page">\n<h2>List of APs</h2>'
	filedata = filedata.replace(strFind, strRepl)

	#Set title page logo image to a different CSS class
	strFind = '<div class="logo"><img src='
	strRepl = '<div class="logo"><img class="logoimg" src='
	filedata = filedata.replace(strFind, strRepl)

	#Fix H4 text alignment on the Requirements Page
	filedata = re.sub(r'<h2>Requirement Definitions</h2>\n<h4>(.*)</h4>(.*)<h4>(.*)</h4>(.*)</div>', r'<h2>Requirement Definitions</h2>\n<h4 style="text-align:left">\1</h4>\2<h4 style="text-align:left">\3</h4>\4</div>', filedata)


	#Fix the Map with no visualizations header
	#Need to use header from Signal Level page, as the MapNoVis page has a wrong header...
	matches = re.finditer(r'</div><div class=\"page\">\n<p class=\"header\">(.+?)</p>\n<h2>Map with no visualizations</h2>\n<div class=\"image\"><img src=\"(.+?)\"/></div>\n</div><div class=\"page\">\n<p class=\"header\">(.+?)</p>\n<h2>Signal Level</h2>', filedata)
	if matches:
		for match in matches:
			oldheadercode = match.string[match.start(0):match.end(0)]
			newheadercode = re.sub(match.group(1), match.group(3), oldheadercode)
			filedata = re.sub(oldheadercode, newheadercode, filedata)
			#filedata = filedata[:match.start()] + newheadercode + filedata[match.end():]	#Can't do this since filedata is modified by this loop and the matches are based on start and end position in the filedata string

	#Add section titles
	matches = re.finditer(r'<div class=\"page\">\n<p class=\"header\">(.+?)</p>\n<h2>Map with no visualizations</h2>', filedata)
	if matches:
		for match in matches:
			oldheadercode = match.string[match.start(0):match.end(0)]
			newheadercode = '<div class=\"page\">\n<p class=\"header\">' + match.group(1) + '</p>\n<h2><div style=\"text-decoration: underline !important; font-weight: bold !important;">\n' + match.group(1) + '</div></h2>\n<h2>Map with no visualizations</h2>'
			filedata = re.sub(oldheadercode, newheadercode, filedata)



	#Remove all page headers
#	filedata = re.sub(r'<p class=\"header\">(.+?)</p>', '<p class=\"header\"></p>', filedata)

	#Replace All headers
#	strRepl = "New Header Here"
#	filedata = re.sub(r'<p class=\"header\">(.+?)</p>', '<p class=\"header\">' + strRepl + '</p>', filedata)

	#Replace Empty headers
#	strRepl = "New Header Here"
#	filedata = re.sub(r'<p class=\"header\"></p>', '<p class=\"header\">' + strRepl + '</p>', filedata)



	#Empty the Page Headers from some pages
	filedata = re.sub(r'<div class=\"page\">\n<p class=\"header\">(.+?)</p>\n<h2>Requirement Definitions</h2>', '<div class=\"page\">\n<p class=\"header\"></p>\n<h2>Requirement Definitions</h2>', filedata)
	filedata = re.sub(r'<div class=\"page\">\n<p class=\"header\">(.+?)</p>\n<h2>Comments</h2>', '<div class=\"page\">\n<p class=\"header\"></p>\n<h2>Comments</h2>', filedata)

	try:
		with open(filename+"-MOD.html", "w") as file:
			print('Writing file...')
			file.write(filedata)
			#print()
			#print()
			#print()
			#print(filedata)
			#print()
		#Exiting the WITH block closes the file automatically
	except:
		print('Error writing file "', filename)
		sys.exit(1)

	print("Done!")
	sys.exit(0)



if __name__ == "__main__":
		main(sys.argv[1:])