import requests
import time
import re
from bs4 import BeautifulSoup
try:
    import urllib.request as urllib2
except ImportError:
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
browser = webdriver.Chrome(options=options)

def check_player_marital_status(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.find(text=lambda text: text and "Wife" in text)
    if results != None:
        return "Yes"
    else:
        return "No"

def tournament_earnings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.findAll("div", {"class": "stat-value"})

    if len(results) < 4: #Failsafe for when I don't get the results I am expecting. Usually from bad url but cause is currently unknown.
        #print("Error: length of results for tournament_earnings does not match expected. Results were length "+len(results))
        return 'Unable to Retrieve Information'

    div_str = results[3].contents[0]
    return ''.join(c for c in div_str if c in [str(d) for d in range(10)])

def from_overview_to_bio(url):
    return from_overview_to_extension(url, "bio")

def from_overview_to_playerActivity(url, year):
    return from_overview_to_extension(url, "player-activity?year="+year)

def from_overview_to_extension(url, extension):
    if url[len(url)-1] == "/":
        return url+extension
    else:
        return from_overview_to_extension(url[:len(url)-1], extension)

def find_basic_info(url):
    data = {}
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    results = soup.findAll("div", {"class": "table-big-value"})
    try:
        data["turned_pro"] = str(int(str(results[1].contents[0])))
    except:
        data["turned_pro"] = "?"

    try:
        data["weight"] = str(int(str(results[2].contents[1])[70:73]))
    except:
        data["weight"] = "?"

    try:
        data["height"] = str(results[3].contents[1])[68:71]
    except:
        data["height"] = "?"

    return data

def scrape_data_player_data(playerNum, file_obj, default_url, str_year, searchedPlayers):

    for i in tqdm(range(1, playerNum+1)):

        player = WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a')))
        player_name = player.text
        if player_name in searchedPlayers:
            browser.get(default_url)
        else:
            file_obj.write(player_name + ',')
            WebDriverWait(browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="rankingDetailAjaxContainer"]/table/tbody/tr['+str(i)+']/td[4]/a'))).click()
            url = browser.current_url
            basic_info = find_basic_info(url)
            file_obj.write(basic_info['turned_pro'] + ',')
            file_obj.write(basic_info['weight'] + ',')
            file_obj.write(basic_info['height'] + ',')
            file_obj.write('\n')
            searchedPlayers.append(str(player_name))
            browser.get(default_url)

def scrape_last_n_years_of_k_players(n, k, singOrDubs="singles", uuid=""):
#    browser.get("https://www.atptour.com/en/rankings/"+singOrDubs+"?rankDate=2019-12-16&rankRange=0-100")

    last_ten_years = [2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]

    dates_by_year = {
        2019 : "16",
        2018 : "31",
        2017 : "25",
        2016 : "26",
        2015 : "21",
        2014 : "29",
        2013 : "30",
        2012 : "31",
        2011 : "26",
        2010 : "27"
    }

    output_file = output_file = open('./output/Tennis_player_details_scrape'+uuid+'.csv', 'w')
    output_file.write('Player' + ',' + 'Turned Pro'+ ',' +'Weight' + ',' + 'Height'+ '\n')
    searchedPlayers = []
    for year in last_ten_years[:n]:
        print(year)
        str_year = str(year)
        url = "https://www.atptour.com/en/rankings/"+singOrDubs+"?rankDate="+str_year+"-12-"+dates_by_year[year]+"&rankRange=0-5000"
        print(url)
        browser.get(url)
        scrape_data_player_data(k, output_file, url, str_year, searchedPlayers)

    browser.quit()

def append_to_scrape(year, k, singOrDubs="singles", uuid = ""):
    dates_by_year = {
        2019 : "16",
        2018 : "31",
        2017 : "25",
        2016 : "26",
        2015 : "21",
        2014 : "29",
        2013 : "30",
        2012 : "31",
        2011 : "26",
        2010 : "27"
    }
    output_file = open('./output/Tennis_player_details_scrape'+uuid+'.csv', 'a')
    print(year)
    str_year = str(year)
    url = "https://www.atptour.com/en/rankings/"+singOrDubs+"?rankDate="+str_year+"-12-"+dates_by_year[year]+"&rankRange=0-5000"
    print(url)
    browser.get(url)
    scrape_data_player_data(k, output_file, url, str_year)

searchedPlayers = []
#scrape_last_n_years_of_k_players(10, 200, "singles", "(bio-info-singles)")
scrape_last_n_years_of_k_players(5, 10, "singles", "(bio-info-singles)")
