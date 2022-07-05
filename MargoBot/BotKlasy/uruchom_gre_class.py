"""Klasa do uruchomienia postaci w grze"""

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class UruchomGre:

    def __init__(self, login, haslo, nick):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get('https://www.margonem.pl/profile/view,5722142#char_1120398,tarhuna')
        self.driver.maximize_window()
        self.actions = webdriver.ActionChains(self.driver)
        self.wait5 = WebDriverWait(self.driver, 5, 0.1)
        self.wait10 = WebDriverWait(self.driver, 10, 0.1)
        self.wait30 = WebDriverWait(self.driver, 30, 0.1)
        self.zaloguj(login, haslo, nick)
        self.zmien_na_stary_interface()
        self.rozwin_chat()
        self.zainstaluj_dodatki()

    def zaloguj(self, login: str, haslo: str, nick: str):
        try:
            self.driver.find_element(By.XPATH, "//*[@id='login-input']").send_keys(login)
            self.driver.find_element(By.ID, "login-password").send_keys(haslo)
            self.driver.find_element(By.ID, "js-login-btn").click()
            self.wait30.until(expected_conditions.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/div[4]/div/div")))
            self.zmien_postac(self.stworz_xpath_z_nickiem(nick))
            self.driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div/div[2]/div[4]/div/div").click()
        except:
            self.driver.refresh()
            self.zaloguj(login, haslo, nick)

    @staticmethod
    def stworz_xpath_z_nickiem(nick: str):
        xpath_postaci = "//div[@data-nick = '" + nick + "']"
        return xpath_postaci

    def zmien_postac(self, xpath_postaci: str):
        self.driver.find_element(By.CLASS_NAME, "select-char").click()
        self.driver.find_element(By.XPATH, xpath_postaci).click()

    def zmien_na_stary_interface(self):
        try:
            self.wait10.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/div")))
            self.wait30.until(expected_conditions.visibility_of_element_located(
                (By.XPATH, "/html/body/div/div[4]/div[7]/div[3]/div[2]/div[10]")))
            self.driver.find_element(By.XPATH, "/html/body/div/div[4]/div[7]/div[3]/div[2]/div[10]").click()
            self.driver.find_element(By.CSS_SELECTOR,
                                     "body > div > div.alerts-layer.layer > div.border-window.ui-draggable.window-on-peak > div.content > div.inner-content > div > div.bottom-bar > div.options-config-buttons.save-card-button > div.button.green.small.change-interface-btn > div.label").click()
            self.wait30.until(expected_conditions.visibility_of_element_located((By.ID, "panel")))
        except:
            pass

    def rozwin_chat(self):
        try:
            self.wait30.until(expected_conditions.visibility_of_element_located((By.ID, 'bchat')))
            self.driver.find_element(By.XPATH, "//*[@id='bchat']").click()
            self.driver.find_element(By.XPATH, "//*[@id='bchat']").click()
            self.driver.find_element(By.XPATH, "//*[@id='bchat']").click()
        except:
            self.rozwin_chat()

    def zainstaluj_dodatki(self):
        dodatki = {"filtr": "//*[@id='addon_114899']/div[2]/h2", "leczenie": "//*[@id='addon_3637']/div[2]/h2",
                   "minutnik": "//*[@id='addon_21993']/div[2]/h2", "auto grupka": "//*[@id='addon_113825']/div[2]/h2"}
        self.driver.find_element(By.ID, "b_addons").click()
        for nazwa_dodatku in dodatki:
            try:
                self.driver.find_element(By.ID, "addon_search").send_keys(nazwa_dodatku)
                self.driver.implicitly_wait(10)
                sleep(1)
                self.driver.find_element(By.XPATH, dodatki.get(nazwa_dodatku)).click()
                self.driver.implicitly_wait(10)
                self.driver.find_element(By.XPATH, "//*[@id='addonDetails']/div/div[2]/div[3]/span[1]").click()
                sleep(1)
                self.driver.find_element(By.XPATH, "//*[@id='addonDetails']/div/div[2]/div[3]/span[2]").click()
                self.driver.find_element(By.ID, "addon_search").clear()
            except:
                continue
        self.driver.refresh()

    def odswiez_gre(self):
        try:
            self.driver.refresh()
            sleep(4)
            if self.driver.find_element(By.ID, "loading").is_displayed():
                self.odswiez_gre()
        except:
            self.odswiez_gre()
