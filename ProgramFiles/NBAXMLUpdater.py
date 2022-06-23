#NBAXMLUpdater.py
# A Program designed to update the Public Service local XML File with the latest NBA Scores
# Author: Jarod Miller, 2022

import time, requests, datetime, dicttoxml#, json

def retrieveDateCode():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    yest = today-delta
    datecode = yest.strftime("%Y")+yest.strftime("%m")+yest.strftime("%d")
    return datecode

def retrieveNBADir(date, TOL):
    try:
        NBAJSON = requests.get("http://data.nba.net/prod/v2/"+date+"/scoreboard.json") #print(type(NBAJSON))
        pfile = NBAJSON.json() #print(type(pfile)) #dump = json.dumps(pfile, indent=2) #print(type(dump)) #print(dump)
        return pfile
    except requests.exceptions.Timeout:
        if TOL==0:
            SystemExit(requests.exceptions.Timeout)
        else:
            time.sleep(60/TOL) 
            return retrieveNBADir(TOL-1)
    except requests.exceptions.TooManyRedirects:
        print("URL Bad, try a new one.")
    except requests.exceptions.RequestException as e: 
        SystemExit(e)

def writeNBAScore(Data, Date):
    scoreDict = {
        "Date": Date,
        "NumGames": Data["numGames"],
        "Games": {}
    } #print(Data)
    if scoreDict["NumGames"]!=0:
        for i in range(scoreDict["NumGames"]):
            game = {"homeTeam": Data["games"][i]["hTeam"]["triCode"],"awayTeam": Data["games"][i]["vTeam"]["triCode"],"homeScore": Data["games"][i]["hTeam"]["score"],"awayScore": Data["games"][i]["vTeam"]["score"]}
            scoreDict["Games"].update({"item"+str(i+1):game})
    scoreXML = dicttoxml.dicttoxml(scoreDict,attr_type=False)
    with open("ExportFiles/NBAScore.xml","w") as xml:
        xml.write(scoreXML.decode())

def updateNBA():
    dateCode = retrieveDateCode()
    datDict = retrieveNBADir(dateCode,10) #print(datDict)
    scoreXML = writeNBAScore(datDict,dateCode)
