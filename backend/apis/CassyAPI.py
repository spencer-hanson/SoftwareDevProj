from cassandra.cluster import Cluster
import sys

class cassyAPI():
    #Connects to cluster, creates "cadence" keyspace if it doens't exist already.
    def __init__(self):
        global session
        global cluster
        DBname = 'cadence'
        cluster = Cluster() #Put IP address as argument here, otherqise runs locally on 127.0.0.1
        session = cluster.connect()
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = {'class':'SimpleStrategy', 'replication_factor':'2'};
            """ %DBname)
        session.set_keyspace(DBname)
        createTables()

        self.database = DBname

	#Add user to users list
    def addUser(self, username, spotifyID):
        addToTable('users',username,'spotify',spotifyID)

	#Edit the input username, change input column value to newValue
    def updateUser(self, username, columnToUpdate, newValue):
        updateRow('users',username,columnToUpdate,newValue)

    #Returns a list for input username
    def getUserInfo(self, username):
        userInfo = []
        line = readLine('users',username)
        tempLine = line[0]
        for i in range(len(tempLine)):
            userInfo.append(tempLine[i])
        return userInfo

	#Adds songs to songlist. Checks if the song exists first: updates if true, adds new song if not
	def addSong(self, artistName, songTitle, spotifyURI, previewURI, recData):
        exists = checkArtist(artistName)
        if(exists):
            input = "update songs set songdata = songdata + ['{0}', '{1}', '{2}', '{3}'] where artistname = '{4}';".format(songTitle, spotifyURI, previewURI, recData, artistName)
            session.execute(input)
        else:
            input = "insert into songs(artistname, songdata) values ('{0}', ['{1}', '{2}', '{3}', '{4}']);".format(artistName, songTitle, spotifyURI, previewURI, recData)
            session.execute(input)

	#Add related artists to artist entry. Reads from list of artists.
    def addRelatedArtists(self, artistList, artistName): #returns list of the names of the related artists
        input = "update songs set (relatedartists) = ["
        for artist in artistList[:-1]:
            input += "'" + artist + "'"
        input += "'" + artistList[-1] + "'] where artistname = " + artistName + ";"
        session.execute(input)

	#Retreives a list of dictionary items: {title, prevURI, spotURI, recData}
    def getSongs(artistName):
        return makeSongsList(artistName)

#To help retreive the info on input username
def getUserInfo(username):
    userInfo = []
    line = readLine('users',username)
    tempLine = line[0]
    for i in range(len(tempLine)):
        userInfo.append(tempLine[i])
    return userInfo


#arguments in form (tableName, newUsername, column1, value1, ...)
#To add a new row to the table
def addToTable(*argv):
    userCheck = checkUserInTable(argv[0], argv[1])
    if(userCheck >= 1):
        print("Entry already exists in table")
        return

    if(argv[0] == "users"):
        input = ('INSERT INTO %s (uid, username) VALUES (now(), \'%s\')' %(argv[0], argv[1]))
        session.execute(input)
        if (len(argv) >= 2):
            for i in range(2,len(argv),2):
                userID = fetchID(argv[1])
                input = ('UPDATE %s SET %s=\'%s\' WHERE uid=%s' %(argv[0], argv[i], argv[i+1], userID))
                session.execute(input)

    elif(argv[0] == "songs"):
        print argv[3]
        input = ('INSERT INTO %s (username, songtitle, artistname, albumname) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')' %(argv[0], argv[1], argv[3], argv[5], argv[7]))
        session.execute(input)


#Arguments in form (tableName, column1, column2, ...)
#Will display all the input information from input table
def dispTables(*argv):
    if (len(argv) == 1):
        input = "SELECT * FROM {0}" .format(argv[0])
        tables = session.execute(input)
        for row in tables:
            print row
    else:
        input = 'SELECT '
        for i in range(len(argv)-2):
            input += (argv[i+1] + ', ')
        input += argv[len(argv)-1]
        input += ' FROM ' + argv[0]
        print(input)
        tables = session.execute(input)

#To help with updating rows
def updateRow(tableName, username, column, value):
    userID = fetchID(username)
    input = "UPDATE {0} SET {1} = \'{2}\' WHERE uid = {3}".format(tableName, column, value, userID)
    session.execute(input)

#Reads the entire line from input table corresponding to input username
def readLine(tableName, username):
    userID = fetchID(username)
    input = ('SELECT * FROM {0} WHERE uid = {0} LIMIT 1' %(tableName, userID))
    row = session.execute(input)
    return row

#Helper to add input columnName to input tableName
def addColumn(tableName, columnName, dataType):
    input = "ALTER TABLE {0} ADD {1} {2}".format(tableName, columnName, dataType)
    session.execute(input)

#Args: (tableName, columnName1, dataType1, columnName2, dataType2, ...)
#Necessary to have at least tableName, columnName1, dataType1.
#Will default to the first column being the primary key
def addTable(*argv):
    input = "CREATE TABLE {0}({1} {2} PRIMARY KEY".format(argv[0], argv[1], argv[2])
    if len(argv)>=3:
        for i in range(3, len(argv), 2):
            input += (', ' + argv[i] + ' ' + argv[i+1])
    input += ');'
    print(input)
    session.execute(input)

#Deletes row from table. songs table has two primary keys, so has to check for input table.
def deleteRow(table, username, songName):
    userID = fetchID(argv[1])
    if(table == "songs"):
        input = "DELETE FROM {0} WHERE uid = {1} AND songtitle = '{2}'".format(table, userID, songName)
        session.execute(input)
        return
    input = ('DELETE FROM {0} WHERE uid = {1}' %(table, userID))
    session.execute(input)

#Gets the UID for the input username
def fetchID(username):
    input = ('SELECT uid FROM users WHERE username = \'%s\'' %username)
    rawID = session.execute(input)
    return rawID[0].uid

#Returns true if user exists in table, false otherwise
def checkUserInTable(username):
    testInput = "SELECT count(*) FROM users WHERE username = '{0}'".format(username)
    instanceCount = session.execute(testInput)
    return instanceCount[0].count

#Checks if artist ecists in table
def checkArtist(artistName):
    testInput = "SELECT count(*) FROM songs WHERE artistname = '{0}'".format(artistName)
    instanceCount = session.execute(testInput)
    return instanceCount[0].count

#Creates a list of songs that exists in the song table with given artist.
def makeSongsList(artistName):
    songList = []
    dataInput = "select songdata from songs where artistname = '{0}'".format(artistName)
    songData = session.execute(dataInput)
    listLen = len(songData[0].songdata)
    for i in range(0, listLen, 4):
        song = {'title':songData[0].songdata[i], 'spotURI':songData[0].songdata[i+1], 'prevURI':songData[0].songdata[i+2], 'recData':songData[0].songdata[i+3]}
        songList.append(song)
    return songList

#Used for testing, creates simple users table and songs table
def createTables():
    session.execute('''
        CREATE TABLE IF NOT EXISTS users (
        username text,
        uid uuid,
        lastfm text,
        spotify text,
        PRIMARY KEY (uid)
        );''')
    session.execute('CREATE INDEX IF NOT EXISTS rusername  on users(username);')
    session.execute('''
        CREATE TABLE IF NOT EXISTS songs (
        artistName text PRIMARY KEY,
        songData list<text>,
        relatedArtists list<text>
        );''')

#Populates test tables with dummy users
def testUserPopulate():
    for i in range(5):
        inputUser = 'username' + `i`
        inputSpotify = 'testSpotify' + `i`
        addUser(inputUser, inputSpotify)

#Returns list of table names
def checkTables():
    tablesList = []
    input = ("SELECT table_name FROM system_schema.tables;")
    tables = session.execute(input)

    return tables

#Testing things...
def tests():
    test = cassyAPI()
    tables =  checkTables()
    print tables

    print("Running tests")
    createTables()
    testUserPopulate()
    print("Made and filled tables.")
    getUserInfo('username0')
    print("Ended tests")
    
def main():
    return 0

if __name__ == "__main__": main()

