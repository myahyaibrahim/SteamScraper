import SteamScraperEngine
import json
import os.path

url ="https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&force_infinite=1&category1=998%2C994%2C21%2C10%2C997&filter=topsellers&snr=1_7_7_7000_7&infinite=1"
urlGenre = "https://store.steampowered.com/tag/browse/#global_492"

def makeJSON(targetDirectory, accessMode, dictionary, indent):
    # Procedure that converts a python dictionary into an external JSON File
    with open(os.path.dirname(__file__) + targetDirectory, accessMode) as f:
        json.dump(dictionary, f, indent=indent)

print("######## Scraping Data is Running ATM.... ########")
gameList, genreList, gameDevList = SteamScraperEngine.SteamScraperMain(url, urlGenre)
# Creating dictionary that contains list of games
# That's been successfully scraped 
GameDictionary = {
    "GamesData" : gameList,
}

print("######## Creating JSON files ATM.... ########")
# Converting from python dictionary to JSON object
# Creating external JSON file
makeJSON('/../data/SteamGame.json', 'w', GameDictionary, 2)

# Creating dictionary that contains list of gemes
# That's been successfully scraped 
GenreDeveloperDictionary = {
    "GenreData" : genreList,
    "DeveloperData" : gameDevList
}
# Converting from python dictionary to JSON object
# Creating external JSON file
makeJSON('/../data/SteamGenreDeveloper.json', 'w', GenreDeveloperDictionary, 2)
print("######## JSON Files has been cretead successfully.... ########")