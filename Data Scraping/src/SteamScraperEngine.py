from typing import Pattern
from bs4 import BeautifulSoup
import requests
import re
from requests.sessions import dispatch_hook
import time

url ="https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&force_infinite=1&category1=998%2C994%2C21%2C10%2C997&filter=topsellers&snr=1_7_7_7000_7&infinite=1"
urlGenre = "https://store.steampowered.com/tag/browse/#global_492"
monthList = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def convertStringToRawString (text):
    # Convert a regular string to raw string in order 
    # to be able to do regular expression function
    strRaw = repr(text)
    strRaw2 = ''
    for i in range (1, len(strRaw)-1,1):
        strRaw2 = strRaw2 + strRaw[i]
    return strRaw2

def findQueueMonth(month):
    # Convert a "month" value from string (e.g Jan, Feb, Mar, etc)
    # to an index of given month value (e.g 1, 2, 3, 4, etc)
    n = len(monthList)
    for i in range (n):
        # Applying regex
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
    # Finding Day
    pattern = re.compile(r'(\d+)\s\w{3},\s\d{4}')
    day = pattern.findall(date)[0]
    if (int(day)<=9):
        day = '0' + day
    # Finding Month
    pattern = re.compile(r'\d+\s(\w{3}),\s\d{4}')
    month = pattern.findall(date)[0]
    month = findQueueMonth(month)
    # Finding Year
    pattern = re.compile(r'\d+\s\w{3},\s(\d{4})')
    year = pattern.findall(date)[0]
    dateNormalized = year + '-' + month + '-' + day
    return dateNormalized


def requestData(url):
    # Requesting data from given URL
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referrer': 'https://store.steampowered.com/search/?category1=998,994,21,10,997&filter=topsellers/robots.txt',
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'DNT': '1',
    }
    source = requests.get(url, headers=headers)
    data = dict(source.json())
    dataResult = data["results_html"]
    return dataResult


def parseDataGamePage(gameURL):
    # Scrapping values from a specific game page(URL)
    # Values that's scrapped; game genres and game developers
    # Return lists : genres and developers of game
    # List declaration
    gameGenreList = []
    gameDevsList = []
    try :
        # Request from URL of specific game
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'referrer': 'https://store.steampowered.com/search/?category1=998,994,21,10,997&filter=topsellers/robots.txt',
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'DNT': '1',
        }
        cookies = { 'birthtime': '283993201', 'mature_content': '1' }
        source = requests.get(gameURL, headers=headers, cookies=cookies).text
        soup = BeautifulSoup(source, 'html5lib')
        # Parsing data that's needed
        ## Finding matching tags
        game = soup.find('div', "game_meta_data")
        game = game.find('div', id="genresAndManufacturer")
        
        ## Getting Game Developers
        gameDev = game.find('div', class_="dev_row")
        gameDev = gameDev.find_all('a')
        for dev in gameDev :
            gameDevsList.append(dev.text)

        ## Getting Game Genres   
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
    print("##### Getting All the Games Detail #####")
    # Parsing the data from given data given from requesting data 
    # Return a list of games that's already parsed
    soup = BeautifulSoup(dataResult, 'html5lib')
    games = soup.find_all('a')
    gameList = []
    gameDevs = []
    for game in games:
        # Getting Game Title
        gameTitle = game.find('span', class_="title").text
        print("Game Title : ",gameTitle)

        # Getting Release Date of particular game
        # Date in format : "DD MMM, YYYY"
        try:
            releaseDate = game.find("div", class_="search_released").text
            releaseDate = normalizeDatePattern(releaseDate)
        except Exception as e:
            releaseDate = None
        print("Release Date : " , releaseDate)
        
        # Getting Price of particular game
        # There 2 values of price that the functions scrap :
        # 1. The original price of a game (originalPrice)
        # 2. The price of game after a discount is applied (discPrice)
        # Note : A free game (stated as "Free to play"), will return 0 value for its price
        priceAll = game.find("div", class_="search_price").text.strip() #.replace(" ","")#.split("Rp")
        source = priceAll
        pattern = re.compile(r'.*free.*', re.IGNORECASE)
        FreeCounter = pattern.findall(source)
        NFreeCounter = len(FreeCounter)
        if (priceAll == "Free to Play" or priceAll == "Free To Play" or priceAll=="Free" or NFreeCounter>=1) :
            originalPrice = 0
            discPrice = 0
        elif (priceAll==""):
            originalPrice = None
            discPrice = None
        else :
            priceAll = priceAll.replace(" ","").split("Rp")
            originalPrice = int(priceAll[1])
            try:
                discPrice = int(priceAll[2])
            except Exception as e:
                discPrice = originalPrice
        print("Original Price : " , originalPrice)
        print("Price after discount : " , discPrice)

        # Getting Review and Rating of a game
        # There are 3 values that'll be scrapped
        # 1. Rating summary for a game (e.g Very Positive, mixed, etc)
        # 2. Percentage value of people that contribute to the rating summary
        # 3. Total review from users 
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
        
        # Platform Compatibility
        # Finding compatibility for every platform or operating system
        # Includes Windows, Macintosh, Linux, VR Support, VR only game
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
        # Getting specific link/url/page for a game
        gameURL = game["href"]
        print("Link Game : " , gameURL)

        # Game Genre, Developer, Publisher
        gameGenres, gameDeveloper = parseDataGamePage(gameURL)
        gameDevs.extend(gameDeveloper)
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
        time.sleep(1.5)
    gameDevs = list(set(gameDevs))
    # print(gameDevs)
    return gameList, gameDevs

def getGenres(urlGenre):
    print("\n##### Getting All the Genres #####")
    # Making request to urlGenre
    source = requests.get(urlGenre).text
    soup = BeautifulSoup(source, 'html5lib')
    # List Declaration
    allGenreList = []
    # Finding tag that has all the genres
    genres = soup.find('div', id="tag_browse_global")
    genres = genres.find_all('div', "tag_browse_tag")
    for genre in genres:
        allGenreList.append(genre.text)
    print("\n######## List of game genre ########")
    print(allGenreList)
    return allGenreList

def getTotalCountGames(url):
    # Getting value of total game that's available in the search page
    # Used to deal with infinite scrolling of the web
    # Return total of games (int)
    source = requests.get(url)
    data = dict(source.json())
    TotalCountGames = data["total_count"]
    if (TotalCountGames > 150):
        TotalCountGames = 150
    return TotalCountGames

def SteamScraperMain(url, urlGenre):
    # Main Function
    # Scraping game data from games listing on steam
    gameList = []
    gameDevList = []
    for i in range (0, getTotalCountGames(url)+1, 50):
        dataResult = requestData(f'https://store.steampowered.com/search/results/?query&start={i}&count=50&dynamic_data=&force_infinite=1&category1=998%2C994%2C21%2C10%2C997&filter=topsellers&snr=1_7_7_7000_7&infinite=1')
        gameListTemp, gameDevListTemp = parseDataSearchPage(dataResult)
        gameList.extend(gameListTemp)
        gameDevList.extend(gameDevListTemp)
        gameDevList = list(set(gameDevList))
    
    print("\n######## List of game developers ########")
    print(gameDevList)
    # Scraping game genre
    genreList = getGenres(urlGenre)
    return gameList, genreList, gameDevList

# SteamScraperMain(url, urlGenre)
# print(getTotalCountGames(url))