import sqlite3  
  
            
#checks if a user has an existing process on SQLite Database            
def checkUserExists(userID):
    try:
        con = sqlite3.connect("player_data.db")
        cursor = con.cursor()
        print("Connected to SQLite")
        
        query = "SELECT 1 FROM profiles WHERE userID = ? LIMIT 1"
        cursor.execute(query, (userID,))
        result = cursor.fetchone()
        
        if result:
            print("User Found")
            return True
        else:
            print("User not Found")
            return False
            
    except sqlite3.Error as error:
        print("Failed to locate Python variable into sqlite table", error)
        
    finally:
        if con:
            con.close()
            print("The SQLite connection is closed")

#adds profile to SQLite Database
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
            
def removeProfile(userID):
    if checkUserExists(userID) == False:
        return "User not found"
    
    else:
        try:
            con = sqlite3.connect("player_data.db")
            cursor = con.cursor()
            print("Connected to SQLite")
            delete_query = "DELETE FROM profiles WHERE userID = ?"
            cursor.execute(delete_query, (userID,))
            con.commit()
            print(f'User {userID} deleted')
            return "User Deleted"
        
          
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
            return "an Error occured"
            
        finally:
            if con:
                con.close()
                print("The SQLite connection is closed")