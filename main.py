# Imports
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json
import time

# URL to scan
url = "https://stats.nba.com/players/traditional/?PerMode=Totals&Season=2019-20&SeasonType=Regular%20Season&sort=PLAYER_NAME&dir=-1"

top10ranking = {}
rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def buildrank(type):
    field = rankings[type]['field']
    label = rankings[type]['label']

    driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()
    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Generate data frame
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', label]]
    df.columns = ['pos', 'player', 'team', 'total']

    return df.to_dict('records')


option = Options()
option.headless = True
# You can set options=option inside webdriver.Firefox() to hide firefox
driver = webdriver.Firefox()
driver.get(url)

# Speeps 7 sec to load accept button
time.sleep(7)

driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()

# Speeps 10 sec to click all elements
time.sleep(10)

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# Generate json file
js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()