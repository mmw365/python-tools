from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.get('http://radiko.jp/#!/live/FMJ')
time.sleep(5)
element = driver.find_element(By.CLASS_NAME, 'js-policy-accept')
element.click()
time.sleep(1)
element = driver.find_element(By.CLASS_NAME, 'play-radio')
element.click()
time.sleep(3600)
driver.quit()
