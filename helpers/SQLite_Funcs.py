import sqlite3  
  
            
#checks if a user has an existing process on SQLite Database            
def checkUserExists(userID):
    try:
        con = sqlite3.connect("player_data.db")
        cursor = con.cursor()
        
        query = "SELECT 1 FROM profiles WHERE userID = ? LIMIT 1"
        cursor.execute(query, (userID,))
        result = cursor.fetchone()
        
        if result:
            print("User Found")
            con.close()
            return True
        else:
            print("User not Found")
            con.close()
            return False
            
    except sqlite3.Error as error:
        print("Failed to locate Python variable into sqlite table", error)
        
    finally:
        if con:
            con.close()

#Returns user database from the Database 
def getUserData(userID):
    con = sqlite3.connect("player_data.db")
    cursor = con.cursor()
    
    query = "SELECT * FROM profiles WHERE userID = ? LIMIT 1"
    cursor.execute(query, (userID,))
    
    result = cursor.fetchone()
    con.close()
    
    if result:
        return result 
    else:
        return None


#adds profile to SQLite Database
def insertProfile(userID, CharName, Region, Realm):
    try:
        con = sqlite3.connect("player_data.db")
        cursor = con.cursor()

        sqlite_insert_with_param = """INSERT INTO profiles
                          (userID, CharName, Region, Realm) 
                          VALUES (?, ?, ?, ?);"""

        data_tuple = (userID, CharName, Region, Realm)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        con.commit()
        print("Python Variables inserted successfully into Profiles table")
        cursor.close()
        con.close()
        return f'User profile created for {CharName}'

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
        
    finally:
        if con:
            con.close()
       
#removes associated profile from the database     
def removeProfile(userID):
    if checkUserExists(userID) == False:
        return "User not found"
    
    else:
        try:
            con = sqlite3.connect("player_data.db")
            cursor = con.cursor()

            delete_query = "DELETE FROM profiles WHERE userID = ?"
            cursor.execute(delete_query, (userID,))
            con.commit()
            
            print(f'User {userID} deleted')
            con.close()
            return f'Profile for {userID} cleared'
        
          
        except sqlite3.Error as error:
            print("Failed to insert Python variable into sqlite table", error)
            return "an Error occured"
            
        finally:
            if con:
                con.close()