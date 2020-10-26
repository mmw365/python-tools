from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import chromedriver_binary

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome('chromedriver', options=options)
driver.get('http://radiko.jp/#!/live/FMJ')
time.sleep(10)
element = driver.find_element_by_class_name('js-policy-accept')
element.click()
element = driver.find_element_by_class_name('play-radio')
element.click()
time.sleep(3600)
driver.quit()
