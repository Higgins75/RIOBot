import sqlite3  
  
    
def insertProfile(userID, CharName, Region, Realm):
    try:
        con = sqlite3.connect("player_data.db")
        cursor = con.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO profiles
                          (userID, CharName, Region, Realm) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (userID, CharName, Region, Realm)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        print("Python Variables inserted successfully into Profiles table")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")
            