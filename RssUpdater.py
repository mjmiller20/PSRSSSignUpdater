#RssUpdater.py
# A Program designed to update the Public Service local XML Files for display on Watchfire electronic signs
# Author: Jarod Miller, 2022

from ProgramFiles.StockXMLUpdater import updateStock
from ProgramFiles.NBAXMLUpdater import updateNBA
from ProgramFiles.MLBXMLUpdater import updateMLB
from ProgramFiles.NFLXMLUpdater import updateNFL

print("Begin Stock XML Update...")
updateStock()
print("Begin NBA XML Update...")
updateNBA()
print("Begin MLB XML Update...")
updateMLB()
print("Begin NFL XML Update...")
updateNFL()