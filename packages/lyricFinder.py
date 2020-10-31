import requests
from bs4 import BeautifulSoup as bs
song = input("Enter song and artist: ")

search_url = song.lower()
main_url = "http://songmeanings.com/query/?query=" + search_url
try:
    requestSource = requests.get(main_url) # or "html.parser"
except:
    print ("Failed to establish connection. Check your internet.")
beautifiedSource = bs(requestSource.content, "html.parser")
links = beautifiedSource.findAll("a")
links2 = beautifiedSource.findAll("a", {"class": ""}, {"style": ""})
artistLink = beautifiedSource.findAll("a", {"class": "smalldarkgraytext"})
artistList = []
searchLinks = []
artists = []
titles = []
for i in range(len(links2)):
    if "href" in str(links2[i]):
        if "songmeanings.com" in str(links2[i]["href"]):
            searchLinks.append(links2[i]["href"])
            titles.append(links2[i].text)
try:
    finalurl = searchLinks[0][2:]
except:
    print ("No lyrics found,sorry.")
    exit()

#print titles[0]


for i in range(len(artistLink)):
    if "href" in str(artistLink[i]):
        artistList.append(artistLink[i]["href"])
        artists.append(artistLink[i]["title"])
print ("\nLyrics for " + titles[0] + " by " + artists[0] + "\n")



requestSource = requests.get("http://" + finalurl) # or "html.parser"
beautifiedSource = bs(requestSource.content, "html.parser")
lyrics = beautifiedSource.findAll("div", {"class":"holder lyric-box"})
searchLyric = []
for i in range(len(lyrics)):
    searchLyric = lyrics[i].text
listLyric = list(searchLyric)
for i in range(len(listLyric)):
    if listLyric[i] == "\r":
        listLyric[i] = ""
searchLyric = "".join(listLyric)
index = searchLyric.index("Edit Lyrics")
searchLyric = searchLyric[:index]
print(searchLyric)
