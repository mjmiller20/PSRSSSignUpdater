#StockXMLUpdater.py
# A Program designed to update the Public Service local XML File with the latest major stock prices
# Author: Jarod Miller, 2022

import datetime, dicttoxml, time, requests#, json; from xml.dom.minidom import parseString

def retrieveStockPrice(tick, TOL):
    url = "https://api.polygon.io/v2/aggs/ticker/"+tick+"/prev"
    with open("ProgramFiles/KeyFiles/StockAPIKey.txt") as key:
        headers = {"apiKey": key.read(),"adjusted":"true"}
    try:
        response = requests.request("GET",url,params=headers)
        jso = response.json() #print(json.dumps(jso,indent=2))
        return jso
    except requests.exceptions.Timeout:
        if(TOL==0):
            print(tick+": Timeout occurred")
            SystemExit(requests.exceptions.Timeout)
        else:
            time.sleep(60/TOL)
            return retrieveStockPrice(tick,TOL-1)
    except requests.exceptions.TooManyRedirects:
        print(tick+": URL Bad, try a new one.")
    except requests.exceptions.RequestException as e:
        print(tick+": Exception")
        SystemExit(e)

def writeStockXML(stock, dat):
    Date = datetime.datetime.now()
    serDate = Date.strftime("%Y") + "-" + Date.strftime("%m") + "-" + Date.strftime("%d") + " " + Date.strftime("%H") + ":" + Date.strftime("%M")
    stockDict = {
        "Date": serDate, 
        "StockPrice": {}
    }
    for i in range(len(stock)):
        if dat[i]['resultsCount']==0:
            print("Could not retrieve", stock[i], "stock information from server.")
        else:
            stockDict["StockPrice"].update({"item"+str(i+1):{"Ticker":stock[i],"Price":(dat[i]['results'][0]['c'])}})
    stockXML = dicttoxml.dicttoxml(stockDict, attr_type=False) #stockDOM = parseString(stockXML); print(stockDOM.toprettyxml())

    with open("ExportFiles/stockPrice.xml", "w") as export:
        export.write(stockXML.decode())

def updateStock():
    stockTick = []
    with open("ProgramFiles/KeyFiles/stockTickers.dat", "r") as a:
        for line in a:
            stockTick.extend(map(str, line.split())) #print(stockTick)
    stockDat =[]
    for i in range(len(stockTick)):
        if i%5 == 0:
            print("\tWaiting to update API", end="")
            for i in range(13):
                time.sleep(5)
                print(".",end="")
            print("")
        stockDat.append(retrieveStockPrice(stockTick[i],10)) #print(type(stockDat)); print(stockDat)
    writeStockXML(stockTick, stockDat)

updateStock()