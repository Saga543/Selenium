from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from MargoBot.BotKlasy.postac_class import Postac
from MargoBot.Expowiska.demony_sciezka import demony_mapy


class ExpBot(Postac):

    def __init__(self, login, haslo, nick):
        super().__init__(login, haslo, nick)

    def exp(self, sciezka: {}):
        for potwor in sciezka:
            try:
                cel = self.driver.find_element(By.ID, potwor)
            except NoSuchElementException:
                print("Ubity")
                continue
            self.dojdz_na_kordy(sciezka.get(potwor), demony_mapy.get(self.pobierz_mape()))
            self.actions.context_click(cel).perform()
            sleep(1)
            if self.driver.find_element(By.ID, "battle").is_displayed():
                self.wcisnij_auto()
                self.wait5.until(expected_conditions.invisibility_of_element_located((By.ID, "battle")))


bot = ExpBot("kuba92800", "b0l0ssec0m", "Rithuru")
# bot.exp(demony_sciezka)

