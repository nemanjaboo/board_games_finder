import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlwt

start_time = time.time()
DRIVER_PATH = 'C:/Users/KINEZ/PycharmProjects/pythonProject1/chromedriver.exe'
ser = Service(DRIVER_PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
timeout = 6
bgnome_games = []

for nmb in range(1, 1000):
    driver.get('https://www.bottlegnome.com/drustvene-igre?page={}&orderBy=CreatedDate%20desc'.format(str(nmb)))
    driver.maximize_window()
    try:
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.item'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    all_ = driver.find_elements(By.CSS_SELECTOR, 'div.item')
    games = [i.text.split("\n") for i in all_]
    if len(games) < 1:
        print('No more games to scrape.')
        break
    links = []
    h5_element = driver.find_elements(By.CLASS_NAME, "owl_item_title ")
    bnome_games = []
    for h in h5_element:
        a_element = h.find_element(By.TAG_NAME, "a")
        href = a_element.get_attribute(('href'))
        links.append(href)

    for gn in range(len(games)):
        games[gn].append(links[gn])
        if len(games[gn]) == 6:
            if games[gn][1] == 'Nema na stanju':
                games[gn][0], games[gn][1], games[gn][2], games[gn][3], games[gn][4], games[gn][5] = games[gn][2].upper(), int(
                    games[gn][4][:-4]), games[gn][1].upper(), games[gn][5], games[gn][0], games[gn][3]
                games[gn] = games[gn][:-2]
        elif len(games[gn]) == 5:
            if games[gn][1] != 'Nema na stanju':
                games[gn][0] = 'NA STANJU'
                games[gn][0], games[gn][1], games[gn][2], games[gn][3], games[gn][4] = games[gn][1].upper(), int(
                    games[gn][3][:-4]), games[gn][0], games[gn][4], games[gn][2]
                del games[gn][-1]
            else:
                games[gn][0], games[gn][1], games[gn][2], games[gn][3], games[gn][4] = games[gn][2].upper(), int(
                    games[gn][3][:-4]), games[gn][1].upper(), games[gn][4], games[gn][0]
                del games[gn][-1]
        elif len(games[gn]) == 4:
            games[gn][0], games[gn][1], games[gn][2], games[gn][3] = games[gn][1].upper(), int(games[gn][2][:-4]), \
                                                                     games[gn][3], games[gn][0]
            games[gn].insert(2, 'NA STANJU')
            del games[gn][-1]

        bgnome_games.append(games[gn])

driver.quit()
print("time elapsed: {:.2f}s".format(time.time() - start_time))
print('BottleGnome Scrapped')
