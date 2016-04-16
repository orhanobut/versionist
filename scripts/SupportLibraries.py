import urllib2 
import os

from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
	def __init__(self, file):
		HTMLParser.__init__(self)
		self.data = None
		self.titleData = None
		self.file = file
	def handle_endtag(self, tag):
		if tag == 'h2' or tag =='h3':
			self.titleData = self.data

		# Prints the title and gradle dependency
		if tag == 'pre' and "renderscript" not in self.data:
			data = self.data.encode('string_escape')[2:-2]
			self.file.write("```groovy\n// " + self.titleData.upper() + "\n")
			self.file.write("compile '" + data + "'\n```\n")

	def handle_data(self, data):
		self.data = data

def generateSupport(url):
	with open("temp.txt", "w+") as f:
		parser = MyHTMLParser(f)
		parser.feed(urllib2.urlopen(url).read())
	with open("temp.txt") as f:
		content= f.read()

	os.remove("temp.txt")
	return content

# print generateSupport('http://developer.android.com/tools/support-library/features.html')