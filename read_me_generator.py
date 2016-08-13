from urllib.request import urlopen
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

def add_header(header):
  file.write("\n\n")
  file.write("# " + header + "\n")

def get_soup(url):
  response = urlopen(url).read().decode('utf-8')
  response = response.encode('utf-8')
  
  return BeautifulSoup(response, 'html.parser')

def add_list(compileType, list):
  file.write("```groovy\n")
  for pair in list:
    file.write('// ' + pair.title + "\n")
    file.write(compileType + " '" + pair.dependency + "'\n\n")
  file.write("```\n")

def add_platform(url):
  tags = get_soup(url).table
  for a in tags.find_all('a'):
    path = a['href']

  write(str(tags))

def add_espresso(url):
  title = None
  list =[]
  for tag in get_soup(url).find_all('span', ["c1","s1"]):
    if tag['class'][0] == 'c1':
      title = tag
    if tag['class'][0] == 's1':
      list.append(Pair(title.string[3:], tag.string[1:-1]))
  add_list('androidTestCompile', list)

def add_android_studio(url):
  soup = get_soup(url)
  android_studio = None
  emulator = None
  entries = soup.find_all('entry')

  for entry in entries:
    title = entry.title.string
    for link in entry.find_all('link'):
      if link['rel'][0] == 'alternate':
        if android_studio == None:
          android_studio = "[" +  title + "](" + link['href'] +")"
        if "Emulator" in title:
          if emulator == None:
            index = title.find("Emulator")
            emulator = "[" +  title[index:] + "](" + link['href'] +")"

    if android_studio != None and emulator != None:
      write(android_studio + "\n\n" + emulator)
      return

def add_google_play_service(url):
  soup = get_soup(url)
  tags = soup.find_all(['td'])
  list = []
  iterator = iter(tags);
  # while (iterator.next() != None)
  try:
    while True:
      pair = Pair(iterator.next().string, iterator.next().string)
      list.append(pair)
  except:
    pass
  add_list('compile', list)

def add_support_libraries(url):
  soup = get_soup(url)
  tags = soup.find_all(['h2','h3','pre'])

  list = []
  title = None
  for tag in tags:
    if tag.name == 'h2' or tag.name == 'h3':
      title = tag.string
    if tag.name == 'pre' and "renderscript" not in tag.string:
      pair = Pair(title, str(tag.string).encode('unicode_escape')[2:-2])
      list.append(pair)

  add_list('compile', list)

def add_firebase(url):
  soup = get_soup(url)
  tags = soup.find_all(['td'])

  list = []
  for i in range(0, len(tags)-1, 2):
    title = tags[i+1].string
    dependency = tags[i].string
    pair = Pair(title, dependency)
    list.append(pair)

  add_list('compile', list)

def add_maven_repo(title, groupId, artifactId):
  url = 'https://maven-badges.herokuapp.com/maven-central/' + groupId+'/' + artifactId
  res = urllib2.urlopen(url)
  finalurl = res.geturl()

  list = finalurl.split('%7C')
  dependency= list[1] + ":" + list[2] + ":" + list[3]
  return Pair(title, dependency)

with open('README.md', 'w+') as file:
  write("[Android Platform](#android-platform) | [Android Studio](#android-studio) | [Google Play Services](#google-play-services) | [Support Library](#support-library) | [Firebase](#firebase) | [Test](#test) | [Others](#others)\n\n")
  write("---")

  add_header("Android Platform")
  add_platform('http://developer.android.com/guide/topics/manifest/uses-sdk-element.html')

  add_header("Android Studio")
  add_android_studio('https://sites.google.com/a/android.com/tools/recent/posts.xml')

  add_header("Google Play Services")
  add_google_play_service('https://developers.google.com/android/guides/setup')

  add_header("Support Library")
  add_support_libraries('http://developer.android.com/tools/support-library/features.html')

  add_header("Firebase")
  add_firebase('https://firebase.google.com/docs/android/setup')

  add_header("Test")
  add_espresso('https://google.github.io/android-testing-support-library/downloads/index.html')

  testList = []
  testList.append(add_maven_repo('JUnit','junit', 'junit'))
  testList.append(add_maven_repo('Mockito','org.mockito', 'mockito-core'))
  testList.append(add_maven_repo('AssertJ','org.assertj', 'assertj-core'))
  testList.append(add_maven_repo('Truth','com.google.truth', 'truth'))
  testList.append(add_maven_repo('Robolectric','org.robolectric', 'robolectric'))
  testList.append(add_maven_repo('Robolectric Shadows Support v4','org.robolectric', 'shadows-support-v4'))
  testList.append(add_maven_repo('Robolectric Shadows Play Services','org.robolectric', 'shadows-play-services'))
  testList.append(add_maven_repo('MockServer','com.squareup.okhttp3', 'mockwebserver'))
  add_list('testCompile', testList)

  add_header("Others")
  others = []
  others.append(add_maven_repo('Gson','com.google.code.gson', 'gson'))
  others.append(add_maven_repo('OkHttp3','com.squareup.okhttp3', 'okhttp'))
  others.append(add_maven_repo('OkHttp3 Logging Interceptor','com.squareup.okhttp3', 'logging-interceptor'))
  others.append(add_maven_repo('RxJava','io.reactivex', 'rxjava'))
  others.append(add_maven_repo('RxAndroid','io.reactivex', 'rxandroid'))
  others.append(add_maven_repo('Dagger 2','com.google.dagger', 'dagger'))
  others.append(add_maven_repo('Logger','com.orhanobut','logger'))
  others.append(add_maven_repo('Timber','com.jakewharton.timber','timber'))
  others.append(add_maven_repo('AutoValue','com.google.auto.value','auto-value'))
  add_list('compile', others)

