#RssUpdater.py
# A Program designed to update the Public Service local XML Files for display on Watchfire electronic signs
# Author: Jarod Miller, 2022

from ProgramFiles.StockXMLUpdater import updateStock
from ProgramFiles.NBAXMLUpdater import updateNBA
from ProgramFiles.MLBXMLUpdater import updateMLB
from ProgramFiles.NFLXMLUpdater import updateNFL

print("Begin Stock XML Update...")
try:
    updateStock()
except:
    print("Could not update Stock XML.")
finally:
    print("Begin NBA XML Update...")
    try:
        updateNBA()
    except:
        print("Could not update NBA XML.")
    finally:
        print("Begin MLB XML Update...")
        try:
            updateMLB()
        except:
            print("Could not update MLB XML.")
        finally:
            print("Begin NFL XML Update...")
            try:
                updateNFL()
            except:
                print("Could not update NFL XML.")
            finally:
                print("All updates completed.")