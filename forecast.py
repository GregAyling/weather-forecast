import requests
import os
from bs4 import BeautifulSoup

_HTML_FILENAME = 'forecast.html'
_PAGE_TITLE = "BRISBANE 7-day forecast"
_FORECAST_WEB_PAGE = "http://www.bom.gov.au/qld/forecasts/brisbane.shtml"

# General tag adder...
def _tagged(tag,textin):
	return("<" + tag + ">" + textin + "</" + tag + ">")

if __name__ == "__main__":

	page = requests.get(_FORECAST_WEB_PAGE)
	soup = BeautifulSoup(page.content, 'html.parser')
	day_range = soup.find_all(class_="day")

	# Create HTML file.
	weatherfile=open(_HTML_FILENAME,'w')
	weatherfile.write("<head>")
	weatherfile.write(_tagged("title", _PAGE_TITLE))
	weatherfile.write('<link rel="stylesheet" type="text/css" href="default.css">')
	weatherfile.write("</head>")
	weatherfile.write("<body>")

	# Write data for each day in forecast.
	for dayno in range(7):
		# Period...
		period = day_range[dayno].find('h2')
		weatherfile.write(_tagged("p",_tagged("h1",period.get_text())))
		# Summary...
		summary = day_range[dayno].find(class_="summary")
		if summary is not None:
			weatherfile.write(_tagged("p",summary.get_text()))
		# Minimum...
		min = day_range[dayno].find(class_="min")
		if min is not None:
			weatherfile.write(_tagged("p","Minimum: " + min.get_text()))
		# Maximum...
		max = day_range[dayno].find(class_="max")
		if max is not None:
			weatherfile.write(_tagged("p","Maximum: " + max.get_text()))
		# Rain...
		rain = day_range[dayno].find_all(class_="rain")
		if len(rain) == 3:
			weatherfile.write(_tagged("p",rain[0].get_text() + "   " + rain[2].get_text()))
		else:
			weatherfile.write(_tagged("p",rain[0].get_text()))
		# Detail...
		detail = day_range[dayno].find_all("p")
		if detail[0] is not None:
			weatherfile.write(_tagged("p",detail[0].get_text()))

	weatherfile.write("</body>")
	weatherfile.close()

	# Display file.
	os.startfile(_HTML_FILENAME)