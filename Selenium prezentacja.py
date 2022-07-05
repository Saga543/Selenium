from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

wait5 = WebDriverWait(driver, 5, 0.5)
wait10 = WebDriverWait(driver, 10, 0.5)
wait30 = WebDriverWait(driver, 30, 0.5)

#Driver metody
driver.get('https://www.youtube.com/')
driver.minimize_window()
driver.maximize_window()
driver.fullscreen_window()
driver.refresh()
driver.close()
driver.quit()
driver.back()
driver.execute_script()
driver.get_screenshot_as_png()
driver.switch_to.alert.accept()
driver.switch_to.alert.dismiss()

#Znajdywanie elementów
driver.find_element(By.ID, "elementID")
driver.find_element(By.XPATH)
driver.find_element(By.CLASS_NAME)
driver.find_element(By.PARTIAL_LINK_TEXT)
driver.find_element(By.CSS_SELECTOR)
driver.find_element(By.NAME)
driver.find_element(By.TAG_NAME)
driver.find_elements(By.ID, "elementID")

#Operacje na elementach
driver.find_element(By.ID, "elementID").click()
driver.find_element(By.ID, "elementID").clear()
driver.find_element(By.ID, "elementID").get_attribute("tag")
driver.find_element(By.ID, "elementID").send_keys("wartosc")
driver.find_element(By.ID, "elementID").send_keys(Keys.ENTER)
driver.find_element(By.ID, "elementID").is_displayed()
driver.find_element(By.ID, "elementID").is_enabled()
driver.find_element(By.ID, "elementID").is_selected()
text = driver.find_element(By.ID, "elementID").text

#Oczekiwanie na elementy
sleep(0.5)
driver.implicitly_wait(0.5)
wait10.until(expected_conditions.visibility_of_element_located((By.ID, "elementID")))

#Inne akcje na elementach
actions = webdriver.ActionChains(driver)
actions.drag_and_drop().perform()
actions.drag_and_drop_by_offset().perform()
actions.move_to_element_with_offset().perform()
actions.move_to_element().perform()
actions.double_click().perform()
actions.context_click().perform()
actions.click_and_hold().perform()
actions.release().perform()
actions.send_keys_to_element().perform()

