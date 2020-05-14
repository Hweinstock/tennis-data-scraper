import requests
#import urllib.request
import time
import re
from bs4 import BeautifulSoup
import urllib2

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm

options = Options()
options.add_argument("--headless")

# service = Service('chromedriver')
# service.start()
# browser = webdriver.Remote(service.service_url)

browser = webdriver.Chrome(options=options)

browser.get('https://www.atptour.com/en/rankings/singles')

Tennis_data_collection = open('Tennis_player_details_scrape.csv', 'w')

Tennis_data_collection.write('Player' + ',' + 'Career_length'+ ',' +  'Aces' + ',' + 'Double_faults' + ',' + 'First_serve' + ',' + '1st_Serve_Points_Won'
                             + ',' + '2nd_Serve_Points_Won' + ',' + 'Break_Points_Faced' + ',' + 'Break_Points_Saved' + ',' + 'Service_Games_Played' + ',' +
                             'Service_Games_Won' + ',' + 'Total_Service_Points_Won' + ',' + '\n')

# for i in tqdm(range(1, 21)):
#
#     player = WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a')))
#     Tennis_data_collection.write(player.text + ',')
#     WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a'))).click()
#     turned_pro = WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="playerProfileHero"]/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div[2]'))).text
#     career_length = 2019 - int(turned_pro)
#     Tennis_data_collection.write(str(career_length) + ',')
#
#     WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="profileTabs"]/ul/li[6]/a'))).click()
#     WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div[id="playerMatchFactsContainer"]')))

for i in tqdm(range(1, 21)):

    player = WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a')))
    Tennis_data_collection.write(player.text + ',')
    WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a'))).click()
    turned_pro = WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="playerProfileHero"]/div[2]/div[2]/div/table/tbody/tr[1]/td[2]/div/div[2]'))).text
    career_length = 2019 - int(turned_pro)
    Tennis_data_collection.write(str(career_length) + ',')

    WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="profileTabs"]/ul/li[6]/a'))).click()
    WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, 'div[id="playerMatchFactsContainer"]')))
    for y in range(1, 11):
        player_data = browser.find_element_by_xpath('//*[@id="playerMatchFactsContainer"]/table[1]/tbody/tr['+str(y)+']/td[2]')
        data = player_data.text.replace(',', '').replace('%', '')
        Tennis_data_collection.write(data + ',')

    Tennis_data_collection.write('\n')

    browser.get('https://www.atptour.com/en/rankings/singles')

Tennis_data_collection.close()
#


# def check_player(url):
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     results = soup.find(text=lambda text: text and "Wife" in text)
#     if results != None:
#         return True
#     else:
#         return False
#
#
#
# print(check_player("Rafael Nadal"))
