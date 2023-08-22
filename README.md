<h1 align="center">
  <br>
  Data Scraping & Data Storing
  <br>
  <br>
</h1>

<h2 align="center">
  <br>
  Steam Scrape
  <br>
  <br>
</h2>

## Table of Contents

- [Specification of Program](https://github.com/myahyaibrahim/SteamScraper#specification-of-program)
- [Description of the Data and Database Management System (DBMS)](https://github.com/myahyaibrahim/SteamScraper#description-of-the-data-and-database-management-system-dbms)
- [Requirements](https://github.com/myahyaibrahim/SteamScraper#requirements)
- [How to use](https://github.com/myahyaibrahim/SteamScraper#how-to-use)
  - [Data Scraping](https://github.com/myahyaibrahim/SteamScraper#data-scraping)
  - [Data Storing](https://github.com/myahyaibrahim/SteamScraper#data-storing)
- [JSON Structure](https://github.com/myahyaibrahim/SteamScraper#json-structure)
- [Reference](https://github.com/myahyaibrahim/SteamScraper#reference)
- [Online Database](https://github.com/myahyaibrahim/SteamScraper#online-database)
- [Author](https://github.com/myahyaibrahim/SteamScraper#author)

## Specification of Program

Steam Scraper is a program that lets you scrape various data from [Steam listings](https://store.steampowered.com/). It includes listings like games, software, downloadable content, demos, and mods but it doesn't include things like soundtracks, videos, hardware, and inlcude bundles. Beside scraping data from Steam web, the program also facilitates/allows you to convert and store those data into a database (.sql file). Storing the data into a database form gives you freedom and flexibility on how you can utilize the data. For example, you can sort the listings by which app that has the biggest discount so you know what apps that offer the best fot their money, you can listings with a particular review with certain percentage that builds the review itself, etc.

All scripts in this repository are based on python languange with the integration of MariaDB DBMS for it in order to achieve all the database integration functions.

## Description of the Data and Database Management System (DBMS)

Data that are scraped include game title, release date of a game, original price and final price after all discounts are applied, game rating, percentage that builds the rating, total review from all users, game compatibility for each platform (Windows , Mac, Linux, VR compatible, VR only). These data were chosen because they can can be very helpful for users with their buying decision. E.g pricing, discount, review, etc. Hence why the program doesn't scrap listings like soundtracks, videos, hardware, and inlcude bundles because they don't represent the data that we're trying to look for.

For data storing purpose, MariaDB is choosen because it's basically an open source version of MySQL. It's developed to be as compatible with MySQL as possible. MariaDB offers some advantages :

- Because it's open source, it has wide variety of support and wide compatibility. This results in fast migration from one system to others. Plus there is a handful of documentations availabe on internet
- Easy integration with python and that leads to ease when inserting all the data by using a python script
- It's efficient and has better performance (Compared to MySQL). This is because of the large selection of alternative database engines.

Link for listing : https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&force_infinite=1&category1=998%2C994%2C21%2C10%2C997&filter=topsellers&snr=1_7_7_7000_7&infinite=1

Link for genre : https://store.steampowered.com/tag/browse/#global_492

## Requirements

In order to run the whole **Steam Scraper** program, it requires the following programs to be installed in your system first:

1. **Python**, tested using version 3.9.5. You can download latest version of python in [here](https://www.python.org/downloads/)
2. A Database Management System, **MariaDB**. You can download latest version of MariaDB in [here](https://mariadb.com/downloads/)

Alongside those programs, we also need to install a couple of module/packages. **You can run these commands on `command prompt` or `cmd` directly**

1. **beautifulsoup4** python package. This package is used for extracting/pulling out data from given web URL (HTML)
   ```
   pip install beautifulsoup4
   ```
2. A parser module package. There are a couple of options like `lxml`, `html.parser`, or `html5lib`. This parser functions to parse HTML that's previously extracted using `beautifulsoup`. **You only need to install one of these**. In most cases, the parser won't matter too much as long as you're working with good HTML. In our case (Scraping from Steam), they all give the same result. I personally use `html5lib`.

   To install `lxml` parser package

   ```
   pip install lxml
   ```

   To install `html.parser` parser package

   ```
   pip install html-parser
   pip install html.parser
   ```

   To install `html5lib` parser package

   ```
   pip intall html5lib
   ```

3. A python module package for connecting python to MariaDB database, **MariaDB Connector/Python**
   ```
   pip install MariaDB
   ```

## How to use

**Note** : All the scripts are basically normal python script, so you can run it however you want. The followings are the steps to run the python script on `command prompt` or `cmd` on **Windows 10**

### Data scraping

1. Assuming you're in the main directory, change the directory to `Data Scraping/src`

   ```
   cd Data Scraping/src
   ```

2. Run the python script, `SteamScraper.py`

   ```
   python SteamScraper.py
   ```

3. Wait for the process to be done and all the data that's been successfully scraped will be stored in `data` folder in JSON format

Image when running `SteamScraper.py`

![SteamScraper 1](https://github.com/myahyaibrahim/SteamScraper/blob/main/Data%20Scraping/screenshot/SteamScraper%201.png)

![SteamScraper 2](https://github.com/myahyaibrahim/SteamScraper/blob/main/Data%20Scraping/screenshot/SteamScraper%202.png)

### Data Storing

First and foremost, I already made some scripts that'll automatically do all the queries in order to set up the database from creating the database to creating all the tables needed but if you want to do all the queries manually, I also make a text file that contains all the queries

Note : The program will prompt you to check if your `user`, `password`, `host`, `port`, and `database` are correct already. The given data are default data so they'll be fine if you never change anything. Otherwise, you can type **Y** to change the given default value

1. Creating the database and all the tables

   - First method, run an automcatic python script `SettingUpDatabase.py`. Assuming you're still in **Data Scraping/src** directory
     ```
     python SettingUpDatabase.py
     ```
   - Second method. If you want to setting up the database manually, you can run all the queries manually on `command prompt` or `cmd` that you can check in a text file `SQL Query for Setting up Database.txt`

   ![SettingUpDatabase](https://github.com/myahyaibrahim/SteamScraper/blob/main/Data%20Storing/screenshot/SettingUpDatabase.png)

2. Filling up the database with data

   To do this, all you have to do is to run a python script inside `src` folder that I already made. This script will read JSON Files that were already made and then store it to database called _steamscrape_

   ```
   python FillingDatabase.py
   ```

3. After the process is done, you should see a dump database file, `steamscrape.sql` and a database, `steamscrape` in inside `export` folder (**Data storing/export** directory)

   ![FillingDatabase](https://github.com/myahyaibrahim/SteamScraper/blob/main/Data%20Storing/screenshot/FillingDatabase.png)

## JSON Structure

There are 2 JSON Files as a result of the prior scraping process `SteamGame.json` and `SteamGenreDeveloper.json`. The two files are made separately in order to minimize clutter whenever people want to take a look at the JSON file.

1. `SteamGame.json` contains all the data that are associated with game information with the structure as follows

`GamesData` Key is a list of dictionary/object. Each dictionary/object contains several keys: `game_title`, `release_date`, `original_price`, `disc_price`, `gaming_rating`, `game_rating_percentage`, `total_user_reviews`, `win_compatibility`, `mac_compatibility`, `linux_compatibility`, `vr_compatibility`, `vr_only`, `game_URL`, `game_genres`, and `game_developer`

```
{
  "GamesData": [
        {
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
            'game_genres' : [gameGenres],
            'game_developer' : gameDeveloper
        },
        ......
        ......
        {
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
            'game_genres' : [gameGenres],
            'game_developer' : [gameDeveloper]
        }
    ]
}
```

2. `SteamGenreDeveloper.json` contains all the data that are associated with game genre and developers with the structure as follows

`GenreData` Key contains a list of str/String that represents all kinds of genre name. `DeveloperData` Key contains a list of str/String that represents all developer game from all the game titles that have been successufully scraped.

```
{
    "GenreData" : [genreList],
    "DeveloperData" : [gameDevList]
}
```

## Reference

These are some of the references that have been very useful in making this web scraping project

[Python Tutorial: Web Scraping with BeautifulSoup and Requests](https://www.youtube.com/watch?v=ng2o98k983k)

[Python Tutorial: Working with JSON Data using the json Module](https://www.youtube.com/watch?v=9N6a-VLBa2I)

[How to connect Python programs to MariaDB](https://MariaDB.com/resources/blog/how-to-connect-python-programs-to-MariaDB/)

## Online database

Go to [phpmyadmin](http://www.phpmyadmin.co/)

Then you need to insert these following data to log you in

- Host: sql6.freesqldatabase.com

- Database name: sql6426508

- Database password: aNRGg6ZSQH

## Author

Mohammad Yahya Ibrahim
