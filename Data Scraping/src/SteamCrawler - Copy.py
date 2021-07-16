from typing import Pattern
from bs4 import BeautifulSoup
import requests
import json
import re
from requests.sessions import dispatch_hook

# url = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&snr=1_7_7_7000_7&filter=topsellers&infinite=1"
url ="https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&force_infinite=1&category1=998%2C994%2C21%2C10%2C997&filter=topsellers&snr=1_7_7_7000_7&infinite=1"

monthList = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def convertStringToRawString (text):
    strRaw = repr(text)
    strRaw2 = ''
    for i in range (1, len(strRaw)-1,1):
        strRaw2 = strRaw2 + strRaw[i]
    return strRaw2

def findQueueMonth(month):
    n = len(monthList)
    for i in range (n):
        # Apply regex
        textSource = monthList[i]
        search = convertStringToRawString(month)
        pattern = re.compile(search, re.IGNORECASE)
        match = pattern.findall(textSource)
        if (match):
            if (i>9):
                return str(i+1)
            else:
                return "0"+str(i+1)
    

def normalizeDatePattern(date):
    # Date that's scrapped from Steam is in format DD MMM, YYYY (Ex : 5 Aug, 2021)
    # Convert it to a format that's easy to process with database YYYY-MM-DD (2021-08-05)
    # Find Day
    pattern = re.compile(r'(\d+)\s\w{3},\s\d{4}')
    day = pattern.findall(date)[0]
    if (int(day)<=9):
        day = '0' + day
    # Find month
    pattern = re.compile(r'\d+\s(\w{3}),\s\d{4}')
    month = pattern.findall(date)[0]
    month = findQueueMonth(month)
    # Find Year
    pattern = re.compile(r'\d+\s\w{3},\s(\d{4})')
    year = pattern.findall(date)[0]
    dateNormalized = year + '-' + month + '-' + day
    return dateNormalized


def requestData(url):
    source = requests.get(url)
    data = dict(source.json())
    dataResult = data["results_html"]
    return dataResult


def parseDataGamePage(gameURL):
    # List declaration
    gameGenreList = []
    gameDevsList = []
    try :
        # Request from URL of specific game
        cookies = { 'birthtime': '283993201', 'mature_content': '1' }
        source = requests.get(gameURL, cookies=cookies).text
        soup = BeautifulSoup(source, 'html5lib')

        # Finding matching tags
        game = soup.find('div', "game_meta_data")
        game = game.find('div', id="genresAndManufacturer")
        
        # Getting Game Developers
        gameDev = game.find('div', class_="dev_row")
        gameDev = gameDev.find_all('a')
        for dev in gameDev :
            gameDevsList.append(dev.text)

        # Getting Game Genres   
        gameGenres = game.find_all('a')
        for gameGenre in gameGenres:
            gameGenreList.append(gameGenre.text)
        idxDev = gameGenreList.index(gameDevsList[0])
        for i in range (len(gameGenreList)-idxDev ):
            gameGenreList.pop()
    except Exception as e:
        pass
    return gameGenreList, gameDevsList

def parseDataSearchPage(dataResult):
    soup = BeautifulSoup(dataResult, 'html5lib')
    # print(soup.prettify())
    games = soup.find_all('a')
    # print(game.prettify())
    gameList = []
    for game in games:
        # Game Title
        gameTitle = game.find('span', class_="title").text
        print("Game Title : ",gameTitle)

        # Release Date
        try:
            releaseDate = game.find("div", class_="search_released").text
            releaseDate = normalizeDatePattern(releaseDate)
        except Exception as e:
            releaseDate = None
        print("Release Date : " , releaseDate)
        
        # Price (BELUM)
        priceAll = game.find("div", class_="search_price").text.strip() #.replace(" ","")#.split("Rp")
        if (priceAll == "Free to Play" or priceAll == "Free To Play") :
            originalPrice = 0
            discPrice = 0
        elif (priceAll==""):
            originalPrice = None
            discPrice = None
        else :
            priceAll = priceAll.replace(" ","").split("Rp")
            originalPrice = priceAll[1]
            try:
                discPrice = priceAll[2]
            except Exception as e:
                discPrice = originalPrice
        print("Original Price : " , originalPrice)
        print("Price after discount : " , discPrice)

        # # amount of discount
        # try:
        #     discount = game.find("div", class_="search_discount").span.text
        # except Exception as e:
        #     discount = None
        # print("Discount : " , discount)

        # Game Review and Rating
        try:
            ratingAll = game.find("div", class_="search_reviewscore").span
            ratingAll = ratingAll["data-tooltip-html"]
            ## Game rating conclusion
            pattern = re.compile(r'(.+)<br>\d+')
            gameRatingConcs = pattern.findall(ratingAll)
            gamingRatingConc = gameRatingConcs[0]
            print("Game Rating Summary : ", gamingRatingConc)
            ## Game rating percentage
            pattern = re.compile(r'<br>(.+)%')
            gameRatingPercentage = pattern.findall(ratingAll)[0]
            print("Game Rating Percentage : ",gameRatingPercentage)
            ## Total user reviews
            pattern = re.compile(r'the\s(.+)\suser')
            totalUserReviews = pattern.findall(ratingAll)[0]
            totalUserReviews = re.sub(',','', totalUserReviews)
            print("Total User Reviews : ",totalUserReviews)
        except Exception as e:
            gamingRatingConc = None
            gameRatingPercentage = None
            totalUserReviews = None
        
        # Platform
        ## Windows compatibility
        if (game.find("span", class_="platform_img win")):
            winCompatibility = True
        else:
            winCompatibility = False
        ## Mac compatibility
        if (game.find("span", class_="platform_img mac")):
            macCompatibility = True
        else:
            macCompatibility = False
        ## Linux compatibility
        if (game.find("span", class_="platform_img linux")):
            linuxCompatibility = True
        else:
            linuxCompatibility = False
        ## VR (Virtual Reality) compatibility
        if (game.find("span", class_="vr_supported")):
            vrCompatibility = True
        else:
            vrCompatibility = False
        ## VR (Virtual Reality) only game
        if (game.find("span", class_="vr_required")):
            vrOnly = True
        else:
            vrOnly = False
        print("Win comp : ",winCompatibility)
        print("Mac comp : ",macCompatibility)
        print("Linux comp : ",linuxCompatibility)
        print("VR comp : ",vrCompatibility)
        print("VR Only : ",vrOnly)
        
        # Link game (Game URL)
        gameURL = game["href"]
        print("Link Game : " , gameURL)

        # Game Genre, Developer, Publisher
        gameGenres, gameDeveloper = parseDataGamePage(gameURL)
        print("Game Genres : ",gameGenres)
        print("Game Developer : ",gameDeveloper)

        print()
        mygame = {
            'game_title': gameTitle,
            'release_date': releaseDate,
            'original_price': originalPrice,
            'disc_price' : discPrice,
            'gaming_rating' : gamingRatingConc,
            'game_rating_percentage' : gameRatingPercentage,
            'total_user_reviews' : totalUserReviews,
            'win_compatibility' : winCompatibility,
            'mac_compatibility' : macCompatibility,
            'linux_compatibility' : linuxCompatibility,
            'vr_compatibility' : vrCompatibility,
            'vr_only' : vrOnly,
            'game_URL' : gameURL,
            'game_genres' : gameGenres,
            'game_developer' : gameDeveloper
        }
        gameList.append(mygame)
    return gameList

def getTotalCountGames(url):
    source = requests.get(url)
    data = dict(source.json())
    TotalCountGames = data["total_count"]
    return TotalCountGames

def SteamCrawlerMain(url):
    dataResult = requestData(url)
    gameList = parseDataSearchPage(dataResult)
    GameDictionary = {
        "GamesData" : gameList
    }
    with open('Steam.json', 'w') as f:
        json.dump(GameDictionary, f, indent=2)

SteamCrawlerMain(url)