# Script made on Python 3.3
# Packages used are os, selenium and bs4
import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# To hold the proxies that would perform scraping job
proxies = []
# To hold the scraped data
scraped_data = {}


# This function would get top speed proxies from the web to perform the scraping job
# and store it in file proxy.txt
def get_proxies(filename, browser_driver):
    proxy_file = open(filename, 'w')
    proxy_file.close()

    chrome_driver = browser_driver
    os.environ["webdriver.chrome.driver"] = chrome_driver
    driver = webdriver.Chrome(chrome_driver)

    urls = ['http://www.freeproxylists.net/?c=&pt=&pr=&a%5B%5D=0&a%5B%5D=1&a%5B%5D=2&u=97']

    for url in urls:
        driver.get(url)
        assert "Free Proxy Lists - HTTP Proxy Servers (IP Address, Port)" in driver.title
        data = driver.page_source

        soup = BeautifulSoup(data, 'html.parser')
        query = soup.find_all('tbody')

        tulis = query[1]

        soup = BeautifulSoup(str(tulis), 'html.parser')
        query = soup.find_all('tr')
        for t in query:
            td = t.find_all('td')
            if 'IPDecode' in str(td[0]):
                fil = open(filename, 'a')
                fil.write(str(td[0].text.split(')')[1] + ':' + td[1].text + '\n'))
                fil.close()

            driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

    driver.close()
    print("Proxies saved in file proxy.txt\n")


# This function will read proxies from the file proxy.txt, store it in a list
# to start the scraping job
def store_proxies(filename):
    proxy_file = open(filename, "r")
    for line in proxy_file:
        prox = line.replace('\n', '')
        proxies.append(prox)

    print("Proxy Status: " + str(len(proxies)) + " proxies stored\n")
    proxy_file.close()


# This function will scrape data
def scrape_data():
    while True:
        PROXY = proxies[pr_index]

        print("Using " + str(PROXY) + " now")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % PROXY)

        driver = webdriver.Chrome(chrome_options=chrome_options)
        try:
            driver.get("www.google.com")
            soup = BeautifulSoup(driver.page_source, "lxml")

            # Add scraping script

            driver.close()
        except:
            driver.close()

            print("Removing " + str(PROXY) + " now due to lack of speed\n")

            proxies.pop(pr_index)
            pr_index = (pr_index + 1) % len(proxies)

            if len(proxies) == 0:
                print("All proxies have been utilized. Program is ending.")
                break


if "__main__":
    file = "proxy.txt"

    # The address of the 'chromedriver.exe' that needs to be downloaded
    # so selenium can use Chrome Browser. After downloading it
    # Replace the variable browser_driver with its address like in my
    # case its present in C:\Selenium\ChromeDriver
    browser_driver = "C:\Selenium\ChromeDriver\chromedriver"

    if not os.path.isfile(file):
        get_proxies(file, browser_driver)

    store_proxies(file)

    scrape_data()
