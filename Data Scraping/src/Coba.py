from typing import Pattern
from bs4 import BeautifulSoup
import requests
import json
import re
from requests.sessions import dispatch_hook

# text = "Rp 300 000 Rp 600 000"
# splitted = text.split("Rp")
# print(splitted)

# a ="yahya"
# b ="ibrahim"
# print("Nama :", a)


# print("RAW")
# strRaw = repr(a)

# print(strRaw[0])
# print(len(strRaw))

# ratingAll = "Very Positive<br>94% of the 246,780 user reviews for this game are positive."
# ## Game rating conclusion
# pattern = re.compile(r'(.+)<br>')
# gameRatingConcs = pattern.findall(ratingAll)
# gamingRatingConc = gameRatingConcs[0]
# print(gamingRatingConc)
# ## Game rating percentage
# pattern = re.compile(r'<br>(.+)%')
# gameRatingPercentage = pattern.findall(ratingAll)[0]
# print(gameRatingPercentage)
# ## Total user reviews
# pattern = re.compile(r'the\s(.+)\suser')
# totalUserReviews = pattern.findall(ratingAll)[0]
# totalUserReviews = re.sub(',','', totalUserReviews)
# print(totalUserReviews)

def accumulate(attributes_so_far, key, value):
    if not isinstance(attributes_so_far[key], list):
        attributes_so_far[key] = [attributes_so_far[key]]
    attributes_so_far[key].append(value)

gameURL = "https://store.steampowered.com/app/1556110/Total_War_WARHAMMER_II__The_Silence__The_Fury/?snr=1_7_7_7000_150_1"
gameURL = "https://store.steampowered.com/app/208650/Batman_Arkham_Knight/"
gameURL = "https://store.steampowered.com/app/414700/Outlast_2/"
gameURL = "https://store.steampowered.com/app/1172470/Apex_Legends/?snr=1_7_7_7000_150_1"
gameURL = "https://store.steampowered.com/app/236390/War_Thunder/"
gameURL = "https://store.steampowered.com/app/1289670/EA_Play/?snr=1_7_7_7000_150_1"

def parseDataGamePage(gameURL):
    # List declaration
    gameDevPubList = []
    gameGenreList = []
    gameDevsList = []
    gamePubsList = []
    gameFranchisesList = []
    try:
        # Request from URL of specific game
        cookies = { 'birthtime': '283993201', 'mature_content': '1' }
        source = requests.get(gameURL, cookies=cookies).text
        soup = BeautifulSoup(source, 'html5lib')
        game = soup.find('div', "game_meta_data")
        
        
        game = game.find('div', id="genresAndManufacturer")
        
        # Getting Game Developers
        gameDev = game.find('div', class_="dev_row")
        gameDev = gameDev.find_all('a')
        for dev in gameDev :
            gameDevsList.append(dev.text)
        
        # Getting Game Publisher
        # gamePubs = soup.find('div', "glance_ctn_responsive_left")
        # gamePubs = gamePubs.find('div', string="Publisher:")
        # gamePubs = gamePubs.find_parent('div')
        # gamePubs = gamePubs.find_all('a')
        # print(len(gamePubs))
        # for pubs in gamePubs:
        #     gamePubsList.append(pubs.text)
        #     print(pubs.text)

        # Getting Game Franchise
        # gameFranchises = gameDevPubs[2]
        # gameFranchises = gameFranchises.find_all('a')
        # for franchises in gameFranchises:
        #     gameFranchisesList.append(franchises.text)

        # Getting Game Genres   
        gameGenres = game.find_all('a')
        for gameGenre in gameGenres:
            gameGenreList.append(gameGenre.text)
        idxDev = gameGenreList.index(gameDevsList[0])
        for i in range (len(gameGenreList)-idxDev ):
            gameGenreList.pop()

        # print(gameGenreList)
        # print(gameDevsList)
        # print(gamePubsList)
        # print(gameFranchisesList)
    except Exception as e:
        pass
    return gameGenreList, gameDevsList


genre, dev = parseDataGamePage(gameURL)
print(genre)
print(dev)
# print(pub)