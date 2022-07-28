from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from MargoBot.BotKlasy.bot_e2_class import BotE2, pobierz_czas
from MargoBot.KordyMap.namiot_vari_krugera_module import namiot_vari_krugera


class BotVari(BotE2):

    def atakuj_vari(self, id_e2):
        try:
            if self.driver.find_element(By.ID, id_e2).is_enabled():
                kordyPostaci = self.pobierz_kordy_postaci()
                x = kordyPostaci[0]
                y = kordyPostaci[1]
                if (x in range(9, 14)) and (y in range(1, 5)):
                    self.driver.find_element(By.ID, id_e2).click()
                    sleep(0.5)
                else:
                    self.actions.move_to_element_with_offset(self.driver.find_element(By.ID, id_e2), 95, 85).click().perform()
                    sleep(0.5)
        except:
            pass

    def bij_vari(self, id_e2, czas, kordy, kordy_mapy):
        licznik = 0
        self.czekaj_na_e2.until(expected_conditions.visibility_of_element_located((By.ID, id_e2)))
        print("Start", pobierz_czas())
        while True:
            self.atakuj_vari(id_e2)
            self.usun_komunikat()
            if self.elita_ubita(id_e2):
                sleep(2)
                if self.driver.find_element(By.ID, "battle").is_displayed():
                    licznik += 1
                    print(f"Złapałeś E2 po raz: {licznik}    {pobierz_czas()}")
                    self.przejdz_walke()
                else:
                    print(f"Ktoś ubił: {pobierz_czas()}")
                self.usun_komunikat()
                self.dojdz_na_kordy(kordy, kordy_mapy)
                sleep(czas)
                self.odswiez_gre()
                self.anty_afk()
                self.czekaj_na_e2.until(expected_conditions.visibility_of_element_located((By.ID, id_e2)))


postac = BotE2("", "", "")
postac.bij_e2("npc76767", 480, [8, 8], namiot_vari_krugera)
