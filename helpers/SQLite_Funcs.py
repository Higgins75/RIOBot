import os
import sqlite3  
  
db_path = os.path.join(os.path.dirname(__file__), 'data', 'player_data.db')
          
#checks if a user has an existing process on SQLite Database            
def checkUserExists(userID):
    try:
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
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
        print("Failed to locate Python variable into sqlite table:", error)
        

#Returns user database from the Database 
def getUserData(userID):
    try:
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            query = "SELECT * FROM profiles WHERE userID = ? LIMIT 1"
            cursor.execute(query, (userID,))
            result = cursor.fetchone()

    
        if result:
            return result 
        else:
            return None
    except sqlite3.Error as error:
        print(f'An error occured as {error}')
        return None


#adds profile to SQLite Database
def insertProfile(userID, CharName, Region, Realm):
    try:
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            sqlite_insert_with_param = """INSERT INTO profiles
                                        (userID, CharName, Region, Realm) 
                                        VALUES (?, ?, ?, ?);"""
            data_tuple = (userID, CharName, Region, Realm)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            con.commit()
            print("Python Variables inserted successfully into Profiles table")
            return f'User profile created for {CharName}'

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        return "An error occured with inserting the profile"

       
#removes associated profile from the database     
def removeProfile(userID):
    if not checkUserExists(userID):
        return "User not found"
    
    try:
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            delete_query = "DELETE FROM profiles WHERE userID = ?"
            cursor.execute(delete_query, (userID,))
            con.commit()
            print(f'User {userID} deleted')
            return f'Profile for {userID} cleared'
          
    except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
            return "an Error occured"
            
