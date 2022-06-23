#StockXMLUpdater.py
# A Program designed to update the Public Service local XML File with the latest major stock prices
# Author: Jarod Miller, 2022

import polygon, json, datetime, dicttoxml, time
from polygon import RESTClient
from typing import cast
from urllib3 import HTTPResponse

def retrieveStockPrice(tick):
    try:
        today = datetime.datetime.now()
        fromdelta = datetime.timedelta(days = 4)
        todelta = datetime.timedelta(days = 3)
        with open("ProgramFiles/KeyFiles/StockAPIKey.txt", "r") as key:
            client = RESTClient(key.read())
        aggs = cast(HTTPResponse,client.get_aggs(tick,1,"day",today-fromdelta,today-todelta,raw=True,),) #print(aggs.geturl()); print(aggs.status)
        return json.loads(aggs.data)
    except polygon.exceptions.AuthError:
        print("Bad Stock API Key.")
    except polygon.exceptions.BadResponse:
        print("Non-200 Response from API.")
    except polygon.exceptions.NoResultsError:
        print("Missing results key.")

def writeStockXML(stock, dat):
    Date = datetime.datetime.now()
    serDate = Date.strftime("%Y") + "-" + Date.strftime("%m") + "-" + Date.strftime("%d") + " " + Date.strftime("%H") + ":" + Date.strftime("%M")
    stockDict = {
        "Date": serDate, 
        "StockPrice": {}
    }
    for i in range(len(stock)):
        if dat[i]['resultsCount']==0:
            print("Could not retrieve ", stock[i], " stock information from server.")
        else:
            stockDict["StockPrice"].update({stock[i]:(dat[i]['results'][0]['c'])})
    stockXML = dicttoxml.dicttoxml(stockDict, attr_type=False) 
    
    stockDOM = parseString(stockXML); print(stockDOM.toprettyxml())

    with open("ExportFiles/stockPrice.xml", "w") as export:
        export.write(stockXML.decode())

def updateStock():
    stockTick = []
    with open("ProgramFiles/KeyFiles/stockTickers.dat", "r") as a:
        for line in a:
            stockTick.extend(map(str, line.split()))
            
            print(stockTick)

    stockDat =[]
    for i in range(len(stockTick)):
        if i%5 == 0:
            print("Waiting to update API", end="")
            for i in range(13):
                time.sleep(5)
                print(".",end="")
            print("")
        stockDat.append(retrieveStockPrice(stockTick[i])) 
        print(type(stockDat)); print(stockDat)
    writeStockXML(stockTick, stockDat)

updateStock()