# FixTamoReport
A hack of a python script to take an HTML report from TamoGraph and make it more to my liking

**NO LONGER MAINTAINED**

Last updated in March 2017.  It worked then, but I cannot guarantee it works with any newer versions.

##Usage
FixTamoReport.py -i <inputfile>
  inputfile     HTML report output from TamoGraph
  
Makes the following modifications to the report:
- Add new CSS
- Add section titles
- Add Subtitle
- Change Title of Report for Consistency
- Empty the Page Headers from some pages
- Fix H4 text alignment on the Requirements Page
- Fix the Map with no visualizations header
- Insert Page Break and Header before "List of APs"
- Insert Page Break before "List of APs"
- Uses header from Signal Level page, as the MapNoVis page has a wrong header...
- Remove all other page headers
- Remove AP Color Market from Tables
- Remove blue background color
- Replace All headers
- Replace Empty headers
- Set title page logo image to a different CSS class
