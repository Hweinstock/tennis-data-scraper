from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tqdm import tqdm

from scraper import Scraper
from url import from_overview_to_bio, from_overview_to_playerActivity
from dates import get_dates_by_year, get_dates



class DataCollector:

    def __init__(self, debug=True):
        self.debug = debug
        self.modes = ["marital_status", "basic-info"]

        self.file_header = {
            "marital_status": "Player" + "," + "Married?" + "," + "Tournament Earnings($)"+","+"Rank" + "," + "Year"+ "\n",
            "basic-info": 'Player' + ',' + 'Turned Pro'+ ',' +'Weight' + ',' + 'Height'+ '\n'
        }

        self.scrape_func = {
            "marital_status": self.collect_earnings_over_time,
            "basic-info" : self.collect_basic_info
        }

        options = Options()
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)



    def generate_filename(self, label, mode):
        """
        Could add number after label if someone wanted to run multiple tests
        """
        return "./output/Tennis_player_details_scrape("+label+")("+mode+").csv"

    def scrape_last_n_years_of_k_players(self, n, k, mode, singOrDubs="singles"):
        last_ten_years = get_dates()
        dates_by_year = get_dates_by_year()

        if not mode in self.modes:
            print("Error: Invalid Mode. Options are "+str(self.modes))
        else:
            filename = self.generate_filename(singOrDubs, mode)
            output_file = open(filename, "w")
            output_file.write(self.file_header[mode])

            searchedPlayers = []
            for year in last_ten_years[:n]:
                str_year = str(year)
                next_url = "https://www.atptour.com/en/rankings/"+singOrDubs+"?rankDate="+str_year+"-12-"+dates_by_year[year]+"&rankRange=0-5000"

                if self.debug: print(year)
                if self.debug: print(next_url)

                self.browser.get(next_url)
                self.scrape_func[mode](k, output_file, next_url, str_year, searchedPlayers)

            output_file.close()
            self.browser.quit()

    def collect_earnings_over_time(self, playerNum, file_obj, default_url, str_year, searchedPlayers):
        for i in tqdm(range(1, playerNum+1)):

            player = WebDriverWait(self.browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='rankingDetailAjaxContainer']/table/tbody/tr["+str(i)+"]/td[4]/a")))
            file_obj.write(player.text + ",")
            WebDriverWait(self.browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='rankingDetailAjaxContainer']/table/tbody/tr["+str(i)+"]/td[4]/a"))).click()
            url = self.browser.current_url
            bio_url = from_overview_to_bio(url)
            playerActivity_url = from_overview_to_playerActivity(url, str_year)

            bio_scraper = Scraper(bio_url)
            playerActivity_scraper = Scraper(playerActivity_url)

            marital_status = bio_scraper.check_player_marital_status()
            file_obj.write(marital_status + ",")

            tournament_earnings_str = playerActivity_scraper.tournament_earnings()
            file_obj.write(tournament_earnings_str + ",")

            file_obj.write(str(i) + ",")
            file_obj.write(str_year + ",")
            file_obj.write("\n")

            self.browser.get(default_url)

    def collect_basic_info(self, playerNum, file_obj, default_url, str_year, searchedPlayers):
        for i in tqdm(range(1, playerNum+1)):

            player = WebDriverWait(self.browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='rankingDetailAjaxContainer']/table/tbody/tr["+str(i)+"]/td[4]/a")))
            player_name = player.text
            if player_name in searchedPlayers:
                self.browser.get(default_url)
            else:
                file_obj.write(player_name + ",")
                WebDriverWait(self.browser, 20).until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@id='rankingDetailAjaxContainer']/table/tbody/tr["+str(i)+"]/td[4]/a"))).click()
                url = self.browser.current_url

                info_scraper = Scraper(url)
                basic_info = info_scraper.find_basic_info()

                file_obj.write(basic_info["turned_pro"] + ",")
                file_obj.write(basic_info["weight"] + ",")
                file_obj.write(basic_info["height"] + ",")

                file_obj.write("\n")
                searchedPlayers.append(str(player_name))
                self.browser.get(default_url)
