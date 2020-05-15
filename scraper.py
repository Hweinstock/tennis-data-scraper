import requests
from bs4 import BeautifulSoup

class Scraper:

    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.response_soup = BeautifulSoup(self.response.text, "html.parser")

    def check_player_marital_status(self):
        """
        Relies on the fact that wife is consistently used in bio to describe players if they have a wife.
        """
        results = self.response_soup.find(text=lambda text: text and "Wife" in text)

        if results != None:
            return "Yes"
        else:
            return "No"

    def tournament_earnings(self):
        results = self.response_soup.findAll("div", {"class": "stat-value"})

        if len(results) < 4:
            """
            Failsafe for when I don't get the results I am expecting.
            Usually from bad url but cause is currently unknown.
            """
            return 'Unable to Retrieve Information'
        else:

            div_str = results[3].contents[0]
            return ''.join(c for c in div_str if c in [str(d) for d in range(10)])

    def find_basic_info(self):
        data = {}
        results = self.response_soup.findAll("div", {"class": "table-big-value"})
        
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
