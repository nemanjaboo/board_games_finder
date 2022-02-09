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

driver.get('https://conflux.rs/Board-Games?limit=2000')
timeout = 7
try:
    element_present = EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product-layout'))
    WebDriverWait(driver, timeout).until(element_present)

    wb = xlwt.Workbook()
    ws = wb.add_sheet("Conflux Board Games")
    driver.maximize_window()

    stock = driver.find_elements(By.CSS_SELECTOR, "div.product-layout:not(.out-of-stock, .swiper-slide)")
    links = [i.find_element(By.CLASS_NAME, "product-img").get_attribute('href') for i in stock]
    stock = [i.text.split("\n") for i in stock]

    for i in range(len(links)):
        if stock[i][0][-1] == "%":
            stock[i] = stock[i][2:-1]
        stock[i].append(links[i])
        stock[i] = stock[i][-3:]
        stock[i].insert(2, 'NA STANJU')

    no_stock = driver.find_elements(By.CSS_SELECTOR, "div.out-of-stock:not(.swiper-slide)")
    links_no_stock = [i.find_element(By.CLASS_NAME, "product-img").get_attribute('href') for i in no_stock]
    no_stock = [i.text.split("\n") for i in no_stock]
    for i in range(len(links_no_stock)):
        no_stock[i].append('NIJE NA STANJU')
        no_stock[i].append(links_no_stock[i])
        no_stock[i] = no_stock[i][-4:]

    conf_games = stock + no_stock
    conf_games.sort()
    for game in conf_games:
        game[0] = game[0].upper()
        game[1] = int(float(game[1][:-3].replace(",", "")))

    for number in range(len(conf_games)):
        ws.write(number, 0, conf_games[number][0])
        ws.write(number, 1, conf_games[number][1])
        ws.write(number, 2, conf_games[number][2])
        ws.write(number, 3, conf_games[number][3])


    wb.save('Conflux.xls')
    print('Conflux.rs has been scraped')

    driver.quit()
    print("time elapsed: {:.2f}s".format(time.time() - start_time))
except TimeoutException:
    print("Timed out waiting for page to load")