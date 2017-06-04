import ssl
from urllib.request import urlopen

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
    context = ssl._create_unverified_context()

    response = urlopen(url, context=context).read().decode('utf-8')
    response = response.encode('utf-8')

    return BeautifulSoup(response, 'html.parser')


def add_list(compile_type, dependency_list):
    file.write("```groovy\n")
    for pair in dependency_list:
        file.write('// ' + pair.title + "\n")
        file.write(compile_type + " '" + str(pair.dependency) + "'\n\n")
    file.write("```\n")


def add_platform(url):
    tags = get_soup(url).table
    for a in tags.find_all('a'):
        path = a['href']

    write(str(tags))


def add_espresso(url):
    title = None
    dependency_list = []
    for tag in get_soup(url).find_all('span', ["c1", "s1"]):
        if tag['class'][0] == 'c1':
            title = tag
        if tag['class'][0] == 's1':
            dependency_list.append(Pair(title.string[3:], tag.string[1:-1]))
    add_list('androidTestCompile', dependency_list)


def add_android_studio(url):
    soup = get_soup(url)
    android_studio = None
    emulator = None
    entries = soup.find_all('entry')

    for entry in entries:
        title = entry.title.string
        for link in entry.find_all('link'):
            if link['rel'][0] == 'alternate':
                if android_studio is None:
                    android_studio = "[" + title + "](" + link['href'] + ")"
                if "Emulator" in title:
                    if emulator is None:
                        index = title.find("Emulator")
                        emulator = "[" + title[index:] + "](" + link['href'] + ")"

        if android_studio is not None and emulator is not None:
            write(android_studio + "\n\n" + emulator)
            return


def add_google_play_service(url):
    soup = get_soup(url)
    tags = soup.find_all(['td'])
    dependency_list = []
    iterator = iter(tags)
    for item in iterator:
        title = item.string
        deps = next(iterator).string
        dependency_list.append(Pair(title, deps))
    add_list('compile', dependency_list)


def add_support_libraries(url):
    soup = get_soup(url)
    tags = soup.find_all(['h2', 'h3', 'pre'])

    dependency_list = []
    title = None
    for tag in tags:
        if tag.name == 'h2' or tag.name == 'h3':
            title = tag.string
        if tag.name == 'pre' and "renderscript" not in tag.string:
            pair = Pair(title, str(tag.string).encode('unicode_escape')[2:-2])
            dependency_list.append(pair)

    add_list('compile', dependency_list)


def add_firebase(url):
    soup = get_soup(url)
    tags = soup.find_all(['td'])

    dependency_list = []
    for i in range(0, len(tags) - 1, 2):
        title = tags[i + 1].string
        dependency = tags[i].string
        pair = Pair(title, dependency)
        dependency_list.append(pair)

    add_list('compile', dependency_list)


def add_maven_repo(title, group_id, artifact_id):
    url = 'https://maven-badges.herokuapp.com/maven-central/' + group_id + '/' + artifact_id
    context = ssl._create_unverified_context()
    res = urlopen(url, context=context)
    final_url = res.geturl()

    dependency_list = final_url.split('%7C')
    dependency = dependency_list[1] + ":" + dependency_list[2] + ":" + dependency_list[3]
    return Pair(title, dependency)


with open('README.md', 'w+') as file:
    print("Generating content links")
    write("[Android Platform](#android-platform) | [Android Studio](#android-studio) "
          "| [Google Play Services](#google-play-services) | [Support Library](#support-library) "
          "| [Firebase](#firebase) | [Test](#test) | [Others](#others)\n\n")
    write("---")

    print("Generating Android Platform")
    add_header("Android Platform")
    add_platform('http://developer.android.com/guide/topics/manifest/uses-sdk-element.html')

    print("Generating Android Studio")
    add_header("Android Studio")
    add_android_studio('https://sites.google.com/a/android.com/tools/recent/posts.xml')

    print("Generating Google Play Services")
    add_header("Google Play Services")
    add_google_play_service('https://developers.google.com/android/guides/setup')

    print("Generating Support Library")
    add_header("Support Library")
    add_support_libraries('http://developer.android.com/tools/support-library/features.html')

    print("Generating Firebase")
    add_header("Firebase")
    add_firebase('https://firebase.google.com/docs/android/setup')

    print("Generating Test")
    add_header("Test")
    add_espresso('https://google.github.io/android-testing-support-library/downloads/index.html')

    testList = [
        add_maven_repo('JUnit', 'junit', 'junit'), add_maven_repo('Mockito', 'org.mockito', 'mockito-core'),
        add_maven_repo('AssertJ', 'org.assertj', 'assertj-core'),
        add_maven_repo('Truth', 'com.google.truth', 'truth'),
        add_maven_repo('Robolectric', 'org.robolectric', 'robolectric'),
        add_maven_repo('Robolectric Shadows Support v4', 'org.robolectric', 'shadows-support-v4'),
        add_maven_repo('Robolectric Shadows Play Services', 'org.robolectric', 'shadows-play-services'),
        add_maven_repo('MockServer', 'com.squareup.okhttp3', 'mockwebserver')
    ]
    add_list('testCompile', testList)

    print("Generating Kotlin")
    add_header("Kotlin")
    kotlin = [
        add_maven_repo('Kotlin Gradle Plugin', 'org.jetbrains.kotlin', 'kotlin-gradle-plugin'),
        add_maven_repo('Kotlin Android Extension', 'org.jetbrains.kotlin', 'kotlin-android-extensions')
    ]
    add_list('classpath', kotlin)

    print("Generating Others")
    add_header("Others")
    others = [
        add_maven_repo('Gson', 'com.google.code.gson', 'gson'),
        add_maven_repo('OkHttp3', 'com.squareup.okhttp3', 'okhttp'),
        add_maven_repo('OkHttp3 Logging Interceptor', 'com.squareup.okhttp3', 'logging-interceptor'),
        add_maven_repo('RxJava', 'io.reactivex', 'rxjava'),
        add_maven_repo('RxAndroid', 'io.reactivex', 'rxandroid'),
        add_maven_repo('Dagger 2', 'com.google.dagger', 'dagger'),
        add_maven_repo('Logger', 'com.orhanobut', 'logger'),
        add_maven_repo('Timber', 'com.jakewharton.timber', 'timber'),
        add_maven_repo('AutoValue', 'com.google.auto.value', 'auto-value')
    ]
    add_list('compile', others)
