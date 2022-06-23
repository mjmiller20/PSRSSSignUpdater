#MLBXMLUpdater.py
# A Program designed to update the Public Service local XML File with the latest MLB Scores
# Author: Jarod Miller, 2022

import datetime, requests, dicttoxml, json

def retrieveDate(tod):
    delt = datetime.timedelta(days = 1)
    yes = tod-delt
    day = yes.strftime("%d")[1] if yes.strftime("%d")[0]=='0' else yes.strftime('%d')
    urlyes = yes.strftime("%Y") + "-" + yes.strftime("%m") + "-" + day
    return urlyes

def retrieveMLB(date):
    url = "https://api-baseball.p.rapidapi.com/games"
    querystring = {
    "date":date}
    with open("ProgramFiles/KeyFiles/RapidAPIKey.txt",'r') as key:
        headers = {"X-RapidAPI-Key":key.read(),"X-RapidAPI-Host":"api-baseball.p.rapidapi.com"}
    MLBResponse = requests.request("GET", url, headers=headers, params=querystring) #print(type(MLBResponse))
    MLBJSON = MLBResponse.json() #print(type(MLBJSON)) #dump = json.dumps(MLBJSON, indent=2) #print(type(dump)) #print(dump) #MLBScore = {} #i=1 #for l in MLBJSON: #    MLBScore["Game " + str(i)] = {"AwayTeam": l["AwayTeam"], "AwayTeamScore": l["AwayTeamRuns"], "HomeTeam": l["HomeTeam"], "HomeTeamScore": l["HomeTeamRuns"]} #    i=i+1
    return MLBJSON

def writeMLBXML(date, res):
    sportDict = {
        "Date": date, 
        "NumGames": 0,
        "MLB": {}
    }
    TotalGames = 0
    for game in res['response']: #print(game)
        if game['league']['id']==1:
            TotalGames+=1
            indGame = {"homeTeam": game['teams']['home']['name'],"awayTeam": game['teams']['away']['name'],"homeScore": game['scores']['home']['total'],"awayScore": game['scores']['away']['total']}
            sportDict['MLB'].update({"item"+str(TotalGames):indGame})
    sportDict.update({"NumGames": TotalGames})
    sportXML = dicttoxml.dicttoxml(sportDict, attr_type=False) #sportDOM = parseString(sportXML); print(sportDOM.toprettyxml())
    with open("ExportFiles/MLBScore.xml", "w") as export:
        export.write(sportXML.decode())

def updateMLB():
    date = retrieveDate(datetime.datetime.now()) #print(date)
    leagueResponse = retrieveMLB(date)
    writeMLBXML(date, leagueResponse)