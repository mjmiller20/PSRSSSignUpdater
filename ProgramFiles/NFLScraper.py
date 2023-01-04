#NFLScraper.py
#
#

from bs4 import BeautifulSoup
import datetime
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getTodCode():
    tod = datetime.datetime.now()
    todCode = tod.strftime("%Y") + "-" + tod.strftime("%m") + "-" + (tod.strftime("%d")[1] if tod.strftime("%d")[0]=='0' else tod.strftime("%d"))
    return todCode

recentFinalScores=5
scoreDict = {
    "Date": getTodCode(),
    "NumGames": recentFinalScores,
    "NFL": {}
}
GameStat = {
    "WinTeam": "HOME",
    "LoseTeam": "AWAY",
    "WinScore": 0,
    "LoseScore": 0
}

opt=Options()
#opt.headless = True
opt.add_argument("--window-size=1920,1080")
chrome_opt= webdriver.Options()
#chrome_opt.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

driver = webdriver.Chrome('/Users/jarodmiller/chromium/chromedriver', options=opt, chrome_options=chrome_opt)
driver.get('https://www.pro-football-reference.com/years/2022//games.htm')
content = driver.page_source
soup = BeautifulSoup(content)
for a in range(4):
    for b in soup.findAll('tr',href=True, attrs={'data-row':a}):
        wname = b.find('a', attrs={'data-stat':'winner'})
        lname = b.find('a', attrs={'data-stat':'loser'})
        wpts = b.find('a', attrs={'data-set':'pts_win'})
        lpts = b.find('a', attrs={'data-set':'pts_lose'})
        GameStat = {

        }
#test = WebDriverWait(driver=driver, timeout=5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target=directory-first-item]')))
#for i in range(recentFinalScores):
#    matches = driver.find_element_by_xpath('/html/body/div[2]/div[6]/div[2]/div[2]/table/tbody/tr['+str(i)+']')
#    print(matches)


driver.quit()