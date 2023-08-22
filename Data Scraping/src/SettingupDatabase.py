import mariadb

def settingUpTables(user, password, host, port):
    print("######### Creating tables #########")
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database="steamscrape")
        # initiating Cursor
        cur = conn.cursor()

        # Creating table for the steamscrape database
        # Query for creating new table
        createTableQuery = ''' CREATE TABLE IF NOT EXISTS game_information (
                            id_game INT,
                            game_name VARCHAR(255) NOT NULL,
                            release_date DATE,
                            game_URL VARCHAR(255),
                            PRIMARY KEY (id_game)
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS rating (
                            id_game INT,
                            game_rating VARCHAR(255),
                            rating_percentage INT,
                            total_review INT,
                            PRIMARY KEY (id_game),
                            CONSTRAINT FK_rating_gameinformation
                            FOREIGN KEY (id_game) REFERENCES game_information(id_game)
                            ON UPDATE CASCADE ON DELETE CASCADE
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS price (
                            id_game INT,
                            original_price INT,
                            discount_price INT,
                            PRIMARY KEY (id_game),
                            CONSTRAINT FK_price_gameinformation
                            FOREIGN KEY (id_game) REFERENCES game_information(id_game)
                            ON UPDATE CASCADE ON DELETE CASCADE
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS genre (
                            id_genre VARCHAR(100),
                            genre_name VARCHAR(255) NOT NULL,
                            PRIMARY KEY (id_genre)
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS game_genre (
                            id_game INT,
                            id_genre VARCHAR(100),
                            PRIMARY KEY (id_game, id_genre),
                            CONSTRAINT FK_gamegenre_genre
                            FOREIGN KEY (id_genre) REFERENCES genre(id_genre)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                            CONSTRAINT FK_gamegenre_gameinformation
                            FOREIGN KEY (id_game) REFERENCES game_information(id_game)
                            ON UPDATE CASCADE ON DELETE CASCADE
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS compatibility (
                            id_compatibility VARCHAR(100),
                            platform_name VARCHAR(255) NOT NULL,
                            PRIMARY KEY (id_compatibility)
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS game_compatibility (
                            id_game INT,
                            id_compatibility VARCHAR(199),
                            PRIMARY KEY (id_game, id_compatibility),
                            CONSTRAINT FK_gamecompatibility_compatibility
                            FOREIGN KEY (id_compatibility) REFERENCES compatibility(id_compatibility)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                            CONSTRAINT FK_gamecompatibility_gameinformation
                            FOREIGN KEY (id_game) REFERENCES game_information(id_game)
                            ON UPDATE CASCADE ON DELETE CASCADE
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS developer (
                            id_developer VARCHAR (100),
                            developer_name  VARCHAR(255),
                            PRIMARY KEY (id_developer)
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        createTableQuery = ''' CREATE TABLE IF NOT EXISTS game_developer (
                            id_game INT,
                            id_developer VARCHAR (100),
                            PRIMARY KEY (id_game, id_developer),
                            CONSTRAINT FK_gamedeveloper_developer
                            FOREIGN KEY (id_developer) REFERENCES developer(id_developer)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
                            CONSTRAINT FK_gamedeveloper_gameinformation
                            FOREIGN KEY (id_game) REFERENCES game_information(id_game)
                            ON UPDATE CASCADE ON DELETE CASCADE
                            ) ;
                            '''
        cur.execute(createTableQuery)
        conn.commit()

        # To avoid error when trying to insert 4 bytes unicode character into a table
        # Change the encoding from utf8 to utf8mb4
        # Useful when there's VARACHAR with Korean or Chinese words that need to be inserted
        encodingQuery = '''ALTER TABLE developer MODIFY COLUMN developer_name VARCHAR(255)  
                        CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL'''
        cur.execute (encodingQuery)
        conn.commit()

        encodingQuery = '''ALTER TABLE game_information MODIFY COLUMN game_name VARCHAR(255)  
                            CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL;'''
        cur.execute (encodingQuery)
        conn.commit()

        conn.close()
        print("Creating Table is Done")
    except mariadb.Error as e: 
        print(f"Error connecting to MariaDB Platform: {e}")

def settingUpDatabase(user, password, host, port):
    print("######### Setting Up Database #########")
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=port)
        # initiating Cursor
        cur = conn.cursor()
        # Creating database
        # Query for creating database
        dbName = "steamscrape"
        createQuery = "CREATE DATABASE steamscrape"
        cur.execute(createQuery)

        # Checking if the new database has been successfully created
        # Iterarte through list of database name that are availabe
        cur.execute("SHOW DATABASES")
        print("List of databases :")
        for db in cur:
            print(db)

        conn.commit()
        conn.close()
        print("Creating Database is Done")
    except mariadb.Error as e: 
        print(f"Error connecting to MariaDB Platform: {e}")

user="root"
password=""
host="localhost"
port=3306

print("These are MariaDB settings that's currently set, do you want to reconfigure it?(Y/N)")
print("user:", user)
print("password:", password)
print("host", host)
print("port:", port)
respone = str(input("Y/N :"))
if (respone == "Y"):
    print("Configuring settings :")
    user=str(input("user:"))
    password=str(input("password:"))
    host=str(input("host:"))
    port=int(input("port:"))
    settingUpDatabase(user, password, host, port)
    settingUpTables(user, password, host, port)
elif(respone == "N"):
    print("configuration is retained")
    settingUpDatabase(user, password, host, port)
    settingUpTables(user, password, host, port)
else:
    print("Response is not recognizable, will pass with the existance configuration")
    settingUpDatabase(user, password, host, port)
    settingUpTables(user, password, host, port)