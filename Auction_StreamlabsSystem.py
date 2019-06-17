import os
import sys
import json
import codecs
import clr


sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

import sqlite3

#script meta info
ScriptName = "Auction"
Website = "https://github.com/e-trp/Auction_Streamlabs"
Description = "streamlabs chatbot auction"
Creator = "Evgeniy etr-p"
Version = "1.0.0"

#global variables and settings
configFile = "config.json"
settings = {}
games=set()

sql={ 
	"create"      : """create table if not exists auction(id integer primary key autoincrement, game text, cost integer)""",
	"insert"      : """insert into auction(game, cost) values (?, ?)""",
	"select_game" : """select game, cost from auction where game=?""",
	"select_all"  : """select id, game, cost from auction order by cost desc""" ,
	"update"      : """update auction set cost=cost+? where game=? """
	 }

def MakeTable(game, cost):
	jd     = list()
	conn   = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'auction.db'))
	cursor = conn.cursor()
	
	cursor.execute(sql['create'])
	cursor.execute(sql['update'],(cost,game)) if game in games else cursor.execute(sql['insert'],(game,cost))
	conn.commit()
	games.add(game)
	
	cursor.execute(sql['select_all'])
	data=cursor.fetchall()
	if data:
		for row in data:
			jd.append([row[0], row[1], row[2]])
	conn.close()
	
	Parent.BroadcastWsEvent("AUCTION_TWITCH", json.dumps(jd))
	return 

	
		

def ScriptToggled(state):
	return

def Init():
	global settings


	with codecs.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),configFile), encoding='utf-8-sig', mode='r') as file:
		settings = json.load(file, encoding='utf-8-sig')	
	
	return


def Execute(data):
	if data.IsChatMessage() and data.GetParam(0).lower() ==settings["command"] and data.GetParamCount()>=3 and ((settings["liveOnly"] and Parent.IsLive()) or (not settings["liveOnly"])):	
		
		#values
		outputMessage = ''
		userid   = data.User
		username = data.UserName
		points   = Parent.GetPoints(userid)
		game     = data.Message[data.Message.find(' ')+1:data.Message.rfind(' ')]
		cost     = int(data.Message[data.Message.rfind(' ')+1:])
			
		#points and games
		if points<cost:
			outputMessage="/me "+settings["responseNotEnoughPoints"]
		else:
			Parent.RemovePoints(userid, username, cost)
			MakeTable(game, cost)
			outputMessage="/me "+str(cost)+" points for game: '"+game+"' from user: " +username
		
		#print message
		Parent.SendStreamMessage(outputMessage)

	return

		

def ReloadSettings(jsonData):
	Init()
	return



def Tick():
	return
	
	
def openHelloWindow():
	viewFile = os.path.join(os.path.dirname(__file__), 'frame', 'index.html')
	os.startfile(viewFile)
	return

