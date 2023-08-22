import mariadb
import json
import os

def insertComp(cur, conn):
    # Query for inserting kinds of platform compatibility
    print("##### Inserting Compatibility #####")
    sqlQuery = '''INSERT INTO compatibility
                VALUES
                    ('C1','Windows'),
                    ('C2','Mac'),
                    ('C3','Linux'),
                    ('C4','VR Compatibility'),
                    ('C5','VR Only');'''
    cur.execute(sqlQuery)
    conn.commit()

def insertGenre(cur, conn, GenreDeveloper):
    # Getting all kinds of game genres (Genre value)
    print("##### Inserting Genres #####")
    idx = 1
    for genre in GenreDeveloper['GenreData']:  # Loop through all the genres availabe that a specific game has
        # id_genre (curID) in format : GXXX
        # E.g G001, G002, etc
        curID = f'G{idx:03d}' 
        print(curID, genre)
        # Query for inserting kinds of game genre
        sqlQuery = "INSERT INTO genre (id_genre, genre_name) VALUES (%s, %s)"
        insertVal = (curID, genre)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
        idx+=1

def insertDeveloper(cur, conn, GenreDeveloper):
    # Getting all game developers (game developer value)
    print("##### Inserting Developers #####")
    idx = 1
    for dev in GenreDeveloper['DeveloperData']: # Loop through all the developers availabe that a specific game has
        # id_developer (curID) in format : DXXX
        # E.g D001, D002, etc
        curID = f'D{idx:03d}'
        print(curID, dev)
        # Query for inserting kinds of game genre
        sqlQuery = "INSERT INTO developer (id_developer, developer_name) VALUES (%s, %s)"
        insertVal = (curID, dev)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
        idx+=1

def insertGameRating(curID, cur, conn, game):
    print("##### GAME RATING #####")
    # Query for inserting game rating values of a game
    # Game rating values include :
    # 1. Rating summary for a game : game['gaming_rating']
    # 2. Percentage of the rating summary : game['game_rating_percentage']
    # 3. Total reviews from users associated with the game : game['total_user_reviews']
    sqlQuery = "INSERT INTO rating (id_game, game_rating, rating_percentage, total_review) VALUES (%s, %s, %s, %s)"
    insertVal = (curID, game['gaming_rating'], int(game['game_rating_percentage']), int(game['total_user_reviews']))
    print(insertVal)
    cur.execute(sqlQuery, insertVal)
    conn.commit()

def insertGamePrice(curID, cur, conn, game):
    print("##### GAME PRICE #####")
    # Query for inserting game price values of a game
    # Game price values include :
    # 1. Original price :  (game['original_price'])
    # 2. Final price after all discounts are applied : (game['disc_price'])
    sqlQuery = "INSERT INTO price (id_game, original_price, discount_price) VALUES (%s, %s, %s)"
    insertVal = (curID, int(game['original_price']), int(game['disc_price']))
    print(insertVal)
    cur.execute(sqlQuery, insertVal)
    conn.commit()

def insertGameCompatibility(curID, cur, conn, game):
    print("##### GAME COMPATIBILITY #####")
    # Query for inserting game compatibility of a game
    # Checking for Windows Compatibility
    if (game['win_compatibility']):
        sqlQuery = "INSERT INTO game_compatibility (id_game, id_compatibility) VALUES (%s, %s)"
        insertVal = (curID, 'C1')
        print("Windows", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
    # Checking for MAC Compatibility   
    if (game['mac_compatibility']):
        sqlQuery = "INSERT INTO game_compatibility (id_game, id_compatibility) VALUES (%s, %s)"
        insertVal = (curID, 'C2')
        print("Mac", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
    # Checking for Linux Compatibility
    if (game['linux_compatibility']):
        sqlQuery = "INSERT INTO game_compatibility (id_game, id_compatibility) VALUES (%s, %s)"
        insertVal = (curID, 'C3')
        print("Linux", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
    # Checking for VR Compatibility
    if (game['vr_compatibility']):
        sqlQuery = "INSERT INTO game_compatibility (id_game, id_compatibility) VALUES (%s, %s)"
        insertVal = (curID, 'C4')
        print("VR comp", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
    # Checking for VR ONLY
    if (game['vr_only']):
        sqlQuery = "INSERT INTO game_compatibility (id_game, id_compatibility) VALUES (%s, %s)"
        insertVal = (curID, 'C5')
        print("VR only", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()

def idGenreFinder(cur, genreName):
    # Function that takes genre name and returns the id_genre 
    # Query which looks for id of a genre (id_genre) given a genre name (genre_name)
    sqlQuery = "SELECT id_genre, genre_name FROM genre WHERE genre_name = ?"
    insertVal = (genreName)
    cur.execute(sqlQuery, (insertVal,))
    # result = []
    # for id_genre, genre_name in cur:
    #     result.append(f"{id_genre}")
    result = cur.fetchone()
    return result[0]

def insertGameGenre(curID, cur, conn, game):
    print("##### GAME GENRE #####")
    # Query for inserting game genre
    for genre in game['game_genres']:
        sqlQuery = "INSERT INTO game_genre (id_game, id_genre) VALUES (%s, %s)"
        insertVal = (curID, idGenreFinder(cur, genre))
        print("insert game genre", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()

def idDeveloperFinder(cur, devName):
    # Function that takes developer name (developer_name) and returns the developer id (id_developer) 
    # Query which looks for id of a developer (id_developer) given a developer name (developer_name)
    sqlQuery = "SELECT id_developer, developer_name FROM developer WHERE developer_name = ?"
    insertVal = (devName)
    cur.execute(sqlQuery, (insertVal,))
    result = cur.fetchone()
    return result[0]

def insertGameDeveloper(curID, cur, conn, game):
    print("##### GAME Developer #####")
    # Query for inserting game developer
    for devoper in game['game_developer']:
        sqlQuery = "INSERT INTO game_developer (id_game, id_developer) VALUES (%s, %s)"
        insertVal = (curID, idDeveloperFinder(cur, devoper))
        print("insert game developer", insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()

def insertGameInformation(cur, conn, games):
    # Getting game information
    curID = 1
    for game in games['GamesData']: # Loop through a list of all the games availabe
        # Query for inserting game information
        print("##### GAME INFORMATION #####")
        sqlQuery = "INSERT INTO game_information (id_game, game_name, release_date, game_URL) VALUES (%s, %s, %s, %s)"
        insertVal = (curID, game['game_title'], game['release_date'], game['game_URL'])
        print(insertVal)
        cur.execute(sqlQuery, insertVal)
        conn.commit()
        # Insert game compatibility
        insertGameCompatibility(curID, cur, conn, game)
        # Checking if rating value is availabe and needs to be inserted
        if (game['gaming_rating'] != None and game['game_rating_percentage'] != None and game['total_user_reviews'] != None) :
            insertGameRating(curID, cur, conn, game)
        # Checking if pricing value is available needs to be inserted
        if (game['original_price'] != None and game['disc_price'] != None) :
            insertGamePrice(curID, cur, conn, game)
        insertGameGenre(curID, cur, conn, game)
        insertGameDeveloper(curID, cur, conn, game)
        curID+=1
        print()


def fillingDatabase(user, password, host, port, database):
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database)
        # initiating Cursor
        cur = conn.cursor()
        
        # Insert query for compatibility table
        insertComp(cur, conn)

        # Working with SteamGenreDeveloper.json
        with open(os.path.dirname(__file__) + '/../data/SteamGenreDeveloper.json') as f:
            GenreDeveloper = json.load(f)
        ## Insert query for Genre
        insertGenre(cur, conn, GenreDeveloper)
        ## Insert query for developer
        insertDeveloper(cur, conn, GenreDeveloper)

        # Working with SteamGame.json
        with open(os.path.dirname(__file__) + '/../data/SteamGame.json') as f:
            games = json.load(f)
        # Insert query for game informatian
        insertGameInformation(cur, conn, games)

        conn.commit()
        conn.close()
        print("Done")
    except mariadb.Error as e: 
        print(f"Error connecting to MariaDB Platform: {e}")
    
def dumpDatabase(user, password):
    print("########## Dumping database ##########")
    curDirectory = os.getcwd()
    curDirectory = os.path.dirname(curDirectory)
    curDirectory = os.path.dirname(curDirectory)
    try:
        # Change the current working Directory  
        os.chdir(curDirectory + '\Data Storing\export')
        try:
            # Dumping database
            if (password==""):
                command = f'cmd /k "mysqldump -c -u {user} --databases steamscrape > steamscrape.sql"'
                os.system(command)
            else:
                command = f'cmd /k "mysqldump -c -u {user} -p {password} --databases steamscrape > steamscrape.sql"'
                os.system(command)
            print("Dumping database has been successfully done")
        except:
            print("Failed to dump the database")
    except OSError:
        print("Can't change the Current Working Directory")


user="root"
password=""
host="localhost"
port=3306
database="steamscrape"

print("These are MariaDB settings that's currently set, do you want to reconfigure it?(Y/N)")
print("user:", user)
print("password:", password)
print("host", host)
print("port:", port)
print("database:", database)
respone = str(input("Y/N :"))
if (respone == "Y"):
    print("Configuring settings :")
    user=str(input("user:"))
    password=str(input("password:"))
    host=str(input("host:"))
    port=int(input("port:"))
    database=str(input("database:"))
    fillingDatabase(user, password, host, port, database)
    dumpDatabase(user, password)
elif(respone == "N"):
    print("Config is retained")
    fillingDatabase(user, password, host, port, database)
    dumpDatabase(user, password)
else:
    print("Response is not recognizable, will pass with the existance configuration")
    fillingDatabase(user, password, host, port, database)
    dumpDatabase(user, password)