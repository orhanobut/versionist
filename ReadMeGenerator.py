import urllib2 
import os
from bs4 import BeautifulSoup

class Pair:
  title = None
  dependency = None

  def __init__(self, title, dependency):
    self.title = title
    self.dependency = dependency

  def __str__(self):
    return self.title + '   ' + self.dependency

def write(text):
  file.write(text)

def addHeader(header):
  file.write("\n\n")
  file.write("# " + header + "\n")

def addItem(title, compileType,  dependency):
  file.write("```groovy\n// " + title.upper() + "\n")
  file.write(compileType + " '" + dependency + "'\n```\n")

def addList(compileType, list):
  for pair in list:
    addItem(pair.title, compileType, pair.dependency)

def getSoup(url):
  return BeautifulSoup(urllib2.urlopen(url).read().decode('utf-8'), 'html.parser')

def generatePlatform(url):
  write(str(getSoup(url).table))

def addEspresso(url):
  title = None
  list =[]
  for tag in getSoup(url).find_all('span', ["c1","s1"]):
    if tag['class'][0] == 'c1':
      title = tag
    if tag['class'][0] == 's1':
      list.append(Pair(title.string[3:], tag.string[1:-1]))
  addList('androidTestCompile', list)

def addAndroidStudio(url):
  soup = getSoup(url)
  androidStudio = None
  emulator = None
  for tag in soup.find_all('title'):
    title= tag.string
    if "Android Studio" in title:
      if androidStudio == None:
        androidStudio = title
    if "Emulator" in title:
      if emulator == None:
        index = title.find("Emulator")
        emulator = title[index:]

    if androidStudio != None and emulator != None:
      write(androidStudio + "\n\n" + emulator)
      return

def addGooglePlayService(url):
  soup = getSoup(url)
  tags = soup.find_all(['td'])
  list = []
  iterator = iter(tags);
  # while (iterator.next() != None)
  try:
    while True:
      pair = Pair(iterator.next().string, iterator.next().string)
      list.append(pair)
  except Exception, e:
    pass
  addList('compile', list)

def generateSupportLibraries(url):
  soup = getSoup(url)
  tags = soup.find_all(['h2','h3','pre'])

  list = []
  title = None
  for tag in tags:
    if tag.name == 'h2' or tag.name == 'h3':
      title = tag.string
    if tag.name == 'pre' and "renderscript" not in tag.name:
      pair = Pair(title, str(tag.string).encode('string_escape')[2:-2])
      list.append(pair)

  addList('compile', list)

def addMavenRepo(title, compileType, groupId, artifactId):
  url = 'https://maven-badges.herokuapp.com/maven-central/' + groupId+'/' + artifactId
  res = urllib2.urlopen(url)
  finalurl = res.geturl()

  list = finalurl.split('%7C')
  dependency= list[1] + ":" + list[2] + ":" + list[3]
  addItem(compileType, title, dependency)

with open('README.md', 'w+') as file:
  addHeader("Android Platform")
  generatePlatform('http://developer.android.com/guide/topics/manifest/uses-sdk-element.html')

  addHeader("Android Studio")
  addAndroidStudio('https://sites.google.com/a/android.com/tools/recent/posts.xml')

  addHeader("Google Play Services")
  addGooglePlayService('https://developers.google.com/android/guides/setup')

  addHeader("Support Library")
  generateSupportLibraries('http://developer.android.com/tools/support-library/features.html')

  addHeader("Test")
  addEspresso('https://google.github.io/android-testing-support-library/downloads/index.html')
  addMavenRepo('testCompile', 'JUnit','junit', 'junit')
  addMavenRepo('testCompile','Mockito','org.mockito', 'mockito-core')
  addMavenRepo('testCompile','AssertJ','org.assertj', 'assertj-core')
  addMavenRepo('testCompile','Robolectric','org.robolectric', 'robolectric')
  addMavenRepo('testCompile','Robolectric Shadows Support v4','org.robolectric', 'shadows-support-v4')
  addMavenRepo('testCompile','Robolectric Shadows Play Services','org.robolectric', 'shadows-play-services')
  addMavenRepo('testCompile','MockServer','com.squareup.okhttp3', 'mockwebserver')

  addHeader("Others")
  addMavenRepo('compile','Gson','com.google.code.gson', 'gson')
  addMavenRepo('compile','OkHttp3','com.squareup.okhttp3', 'okhttp')
  addMavenRepo('compile','OkHttp3 Logging Interceptor','com.squareup.okhttp3', 'logging-interceptor')

with open('README.md') as file:
  print file.read()