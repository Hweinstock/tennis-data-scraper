# tennis-data-scraper

A simple scraping script to gather some stats on professional tennis.      
Inspiration and selenium code taken from,    
https://towardsdatascience.com/the-king-of-serving-tennis-web-scraping-with-selenium-ae92ade2f017  

## Purpose

Originally was used for gathering data for a friend's thesis on the effect  
marital status on tournament earnings in professional tennis.

## Setup

`git clone https://github.com/Hweinstock/tennis-data-scraper.git`  
  
`pip3 install -r requirements.txt`  
  
Head to https://chromedriver.chromium.org/downloads  
and download the chrome driver that matches version of your chrome.     
Then move the chrome driver file to be in a directory included in PATH.  
  
`mv /path/to/chromedriver /path/to/somewhere/in/PATH/`  
  
Now try testing to out with the help menu:  
  
`python3 main.py -h`  

## Usage

Here is the help menu for arguments.   
```
usage: main.py [-h] [-y] [-p] [-m] [-s] [-d]

optional arguments:
  -h, --help       show this help message and exit
  -y , --years     argument describing how many years to go back, starting in
                   2019. Has default value of 1.
  -p , --players   argument describing how many players' data to scrape. Has
                   default value of 5.
  -m , --mode      argument describing what information the data collector
                   should scrape in. Has default value of 'basic-info'.
  -s , --singles   argument describing whether it should look at top singles
                   players or doubles players. Has default value of True
  -d , --debug     argument describing whether it should print debugging and
                   progress messages. Has deafult value of False.
```
An example call could look like this,  
`python main.py -d True -y 2 -p 5 -m basic-info`  

## Example Data

There is a large amount of example output files to check results against in the `output/old_output/` directory.  
