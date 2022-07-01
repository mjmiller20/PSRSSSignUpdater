#NFLXMLUpdater.py
# A Program designed to update the Public Service local XML File with the latest NFL Scores
# Author: Jarod Miller, 2022

import datetime, dicttoxml, json, os, ssl
import pandas as pd

def getTodCode():
    tod = datetime.datetime.now()
    todCode = tod.strftime("%Y") + "-" + tod.strftime("%m") + "-" + (tod.strftime("%d")[1] if tod.strftime("%d")[0]=='0' else tod.strftime("%d"))
    return todCode

def retrieveNFL(yr):
    ssl._create_default_https_context = ssl._create_unverified_context
    pd.options.mode.chained_assignment = None  # default='warn'
    year = yr
    data = pd.read_csv("https://github.com/guga31bb/nflfastR-data/blob/master/data/play_by_play_"+str(year)+".csv.gz?raw=True", compression='gzip', low_memory=False)
    data.to_csv('ProgramFiles/KeyFiles/.NFL_tmp.csv.gz', compression='gzip', index=False)
    data = pd.read_csv('ProgramFiles/KeyFiles/.NFL_tmp.csv.gz', compression='gzip', low_memory=False)
    finalPlays = data.loc[data.game_seconds_remaining==0]
    finalPlays.sort_values(by=['game_date'], inplace=True)
    finalScores = finalPlays[['home_team','away_team','home_score','away_score']]
    recentFinalScores = finalScores.tail()
    os.remove("ProgramFiles/KeyFiles/.NFL_tmp.csv.gz") #print(recentFinalScores)
    return recentFinalScores

def writeNFLXML(recentFinalScores, datecode, teamCode):
    scoreDict = {
        "Date": datecode,
        "NumGames": len(recentFinalScores),
        "NFL": {}
    }
    if scoreDict["NumGames"]!=0:
        for i in range(scoreDict["NumGames"]):
            game = {"homeCity": recentFinalScores.values[i][0],"homeTeam": teamCode[recentFinalScores.values[i][0]],"homeScore": recentFinalScores.values[i][2],"awayCity": recentFinalScores.values[i][1],"awayTeam": teamCode[recentFinalScores.values[i][1]],"awayScore": recentFinalScores.values[i][3]}
            scoreDict["NFL"].update({"item"+str(i+1):game}) #print(scoreDict)
    scoreXML = dicttoxml.dicttoxml(scoreDict,attr_type=False)
    with open("ExportFiles/NFLScore.xml",'w') as xml:
        xml.write(scoreXML.decode())

def updateNFL():
    recentFinalScores = retrieveNFL(datetime.datetime.today().year if (datetime.datetime.today().month>7) else datetime.datetime.today().year-1)
    with open("ProgramFiles/KeyFiles/nflTeamDict.json") as tc:
        teamCode = json.load(tc)
    datecode = getTodCode()
    writeNFLXML(recentFinalScores,datecode,teamCode)