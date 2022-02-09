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
driver.get('https://www.drustveneigre.rs/drustvene-igre?limit=2000')
timeout = 7
try:
    element_present = EC.presence_of_element_located((By.CLASS_NAME, 'product-layout'))
    WebDriverWait(driver, timeout).until(element_present)
    wb = xlwt.Workbook()
    ws = wb.add_sheet("Mipl Board Games")

    driver.maximize_window()

    mipl_games = []
    games_ = []
    bad_tags = ["BESTSELER", "NOVO", "Na stanju", "-25 %", "Din", "USKORO", "NA STANJU"]

    if "Došli ste do kraja kataloga" in driver.page_source:
        all_el = driver.find_elements(By.CLASS_NAME, 'product-layout')
        links = [i.find_element(By.CLASS_NAME, "product-img").get_attribute('href') for i in all_el]
        games_ = [i.text.split("\n") for i in all_el]
        for g in games_:
            if g[0] == "NEMA NA STANJU":
                g[0], g[1], g[-1] = g[1], int(float(g[-1][:-3].replace("," ,""))), g[0]
            mipl_games.append([ele for ele in g if ele not in bad_tags])
            for gn in range(len(mipl_games)):
                if mipl_games[gn][0] == "NEMA NA STANJU":
                    mipl_games[gn][0], mipl_games[gn][1], mipl_games[gn][-1] = mipl_games[gn][1], \
                                                                               int(float(mipl_games[gn][-1][:-3].replace(",", ""))), \
                                                                               mipl_games[gn][0]
                if len(mipl_games[gn]) > 2 and mipl_games[gn][-1] != "NEMA NA STANJU":
                    del mipl_games[gn][-1]
                mipl_games[gn].append(links[gn])
        for i in range(len(mipl_games)):
            if mipl_games[i][2] != 'NEMA NA STANJU':
                mipl_games[i].insert(2, 'NA STANJU')
                mipl_games[i][1] = int(float(mipl_games[i][1][:-3].replace(",", "")))

        for number in range(len(mipl_games)):
                ws.write(number, 0, mipl_games[number][0])
                ws.write(number, 1, mipl_games[number][1])
                ws.write(number, 2, mipl_games[number][2])
                ws.write(number, 3, mipl_games[number][3])
        wb.save('mipl.xls')
        driver.quit()
        print("mipl.rs has been scraped.")
        print("time elapsed: {:.2f}s".format(time.time() - start_time))
except TimeoutException:
    print("Timed out waiting for page to load")
