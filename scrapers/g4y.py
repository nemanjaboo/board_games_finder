import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import xlwt

start_time = time.time()
wb = xlwt.Workbook()
ws = wb.add_sheet("gamesforyou")


DRIVER_PATH = 'C:/Users/KINEZ/PycharmProjects/pythonProject1/chromedriver.exe'
ser = Service(DRIVER_PATH)
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)


driver.get('https://games4you.rs/shop/drustvene-igre')
driver.maximize_window()

select = Select(driver.find_element(By.ID, 'edit-items-per-page'))
select.select_by_visible_text('- All -')

button_all_games = driver.find_element(By.CSS_SELECTOR, 'div.views-submit-button')
b = button_all_games.find_element(By.TAG_NAME, 'input')
b.click()
time.sleep(10)

elements = driver.find_elements(By.CSS_SELECTOR, 'li.views-row')
g4y_games = [i.text.split("\n") for i in elements]
links = []
span = driver.find_elements(By.CSS_SELECTOR, 'div.views-field-title')
for el in span:
    sp = el.find_element(By.TAG_NAME, 'span')
    lnk = sp.find_element(By.TAG_NAME, 'a')
    href = lnk.get_attribute(('href'))
    links.append(href)

if len(g4y_games) == len(links):
    for gn in range(len(g4y_games)):
        g4y_games[gn].append(links[gn])
        g4y_games[gn][0] = g4y_games[gn][0].upper()
        if int(g4y_games[gn][2][-1]) > 0:
            g4y_games[gn][2] = 'NA STANJU'
        else:
            g4y_games[gn][2] = 'NEMA NA STANJU'
        if ',' in g4y_games[gn][1]:
            price_fix = re.findall('[0-9],[0-9]+', g4y_games[gn][1])
            for p in price_fix:
                g4y_games[gn][1] = int(p.replace(",", ""))
        else:
            price_fix = re.findall('[0-9]+', g4y_games[gn][1])
            for price in price_fix:
                g4y_games[gn][1] = int(price)

for number in range(len(g4y_games)):
    ws.write(number, 0, g4y_games[number][0])
    ws.write(number, 1, g4y_games[number][1])
    ws.write(number, 2, g4y_games[number][2])
    ws.write(number, 3, g4y_games[number][3])

wb.save('g4you.xls')
driver.quit()
print("time elapsed: {:.2f}s".format(time.time() - start_time))
print('Games4You Scrapped')
