#!/usr/bin/python

import MySQLdb 
import time

X_SIZE = 50
Y_SIZE = 50
gHost = "localhost"
gUser = "root"
gPasswd = "picklerick"
gDb = "CS3750P03"


# Returns a two dimensional array
def getCurrentGrid():

	# 102x52 grid for the game board (extra two cols and rows for the invisible edge)
	gameMap = [[0 for y in range(Y_SIZE + 2)] for x in range(X_SIZE + 2)]

	# create connection to db
	db = MySQLdb.connect(host=gHost,
						user=gUser,
						passwd=gPasswd,
						db=gDb)

	# Query the GameMap, populate the table
	cur = db.cursor()
	cur.execute("SELECT * FROM GameMap;")
	for row in cur.fetchall():
		if (row[1] < 0) or (row[1] > X_SIZE+1) or (row[2] < 0) or (row[2] > Y_SIZE+1):
			# input("Index out of bounds: ({},{})".format(row[1], row[2]))
			continue
		else:
			gameMap[row[1]][row[2]] = ord(row[3])

	# Close cursor and connection
	cur.close()
	db.close()

	return gameMap


# A step in the game of life.
#	Params: 
# 		- gameMap: The game grid as it currently stands
#	Returns: 
#		The next iteration of the game map.
def iterateGameOfLife(gameMap):	
	newMap = [[0 for y in range(Y_SIZE + 2)] for x in range(X_SIZE + 2)]

	#Work through all cells except border cells
	for x in range(1, X_SIZE+1):
		for y in range(1, Y_SIZE+1):
			#if live cell
			if gameMap[x][y] == 1:

				#add up live cells
				numLiveCells = -1		#don't count the cell under consideration
				for i in range(x-1, x+2):
					for j in range(y-1, y+2):
						numLiveCells += gameMap[i][j]

				#fill out new map using Conway's rules for populated cells
				if numLiveCells in (2,3):	#stable population
					newMap[x][y] = 1
				#else under or over populated

			#if dead cell
			elif gameMap[x][y] == 0:

				#add up live cells
				numLiveCells = 0
				for i in range(x-1, x+2):
					for j in range(y-1, y+2):
						numLiveCells += gameMap[i][j]

				#fill out new map using Conway's rule for unpopulated cells
				if numLiveCells == 3:
					newMap[x][y] = 1

			#Should never happen
			else:
				print "Error! Panic!"

	return newMap


# Print map to console (for testing)
def printMap(gameMap):
	for y in range(1, Y_SIZE+1):
		row = ''
		for x in range(1, X_SIZE+1):
			row += str(gameMap[x][y])
		print row


def writeMapToDB(gameMap):
	# create connection to db
	conn = MySQLdb.connect(host=gHost,
						user=gUser,
						passwd=gPasswd,
						db=gDb)
	# create cursor
	cur = conn.cursor()

	#sql = 'DELETE FROM GameMap;'
	#cur.execute(sql)
	#conn.commit()

	updateAlive = "UPDATE GameMap SET CellAlive = 1 WHERE (1 = 0)"
	updateDead = "UPDATE GameMap SET CellAlive = 0 WHERE (1 = 0)"

	for x in range(1, X_SIZE+1):
		for y in range(1, Y_SIZE+1):
			#sql = 'INSERT INTO GameMap (xCord, yCord, cellAlive) VALUES ({}, {}, {});'.format(x, y, gameMap[x][y])
			if(gameMap[x][y] == 0):
				updateDead = updateDead + " OR (xCord = {} AND yCord = {})".format(x,y)
			else:
				updateAlive = updateAlive + " OR (xCord = {} AND yCord = {})".format(x,y)
 
			#sql = 'UPDATE GameMap set cellAlive = {} WHERE xCord = {} and yCord = {};'.format(gameMap[x][y], x, y )
			
	cur.execute(updateAlive + ";")# + updateDead + ";")
	cur.execute(updateDead + ";")# + updateDead + ";")
	conn.commit()

	# Close cursor and connection
	cur.close()
	conn.close()


def initializeTable(gameMap):
	# create connection to db
	conn = MySQLdb.connect(host=gHost,
						user=gUser,
						passwd=gPasswd,
						db=gDb)
	# create cursor
	cur = conn.cursor()

	gameMap[2][1] = 1
	gameMap[2][2] = 1
	gameMap[2][3] = 1

	for x in range(X_SIZE+2):
		for y in range(Y_SIZE+2):
			sql = 'INSERT INTO GameMap (xCord, yCord, cellAlive) VALUES ({}, {}, {});'.format(x, y, gameMap[x][y])
			cur.execute(sql)
			conn.commit()


def applyChangeQueue(gameMap):
	# create connection to db
	db = MySQLdb.connect(host=gHost,
						user=gUser,
						passwd=gPasswd,
						db=gDb)

	# Query the change queue
	usedQueueIDs = []
	cur = db.cursor()
	cur.execute("SELECT * FROM CommitQueue;")
	for row in cur.fetchall():
		if (row[1] < 0) or (row[1] > X_SIZE+1) or (row[2] < 0) or (row[2] > Y_SIZE+1):
			print "Index out of bounds: ({},{})".format(row[1], row[2])
			continue
		else:
			gameMap[row[1]][row[2]] = (gameMap[row[1]][row[2]] + 1) % 2
			usedQueueIDs.append(row[0])

	# Delete changes from queue
	if usedQueueIDs:
		usedQueueIDs = ','.join(map(str, usedQueueIDs))
		sql = 'DELETE FROM CommitQueue WHERE Id in ({});'.format(usedQueueIDs)
		cur.execute(sql)
		db.commit()

	# Close cursor and connection
	cur.close()
	db.close()

	return gameMap


newmap = getCurrentGrid()
timer = time.time()
while True:
	newmap = applyChangeQueue(newmap)
	writeMapToDB(newmap)

	if time.time() > timer + 3:
		newmap = iterateGameOfLife(newmap)
		timer = time.time()
