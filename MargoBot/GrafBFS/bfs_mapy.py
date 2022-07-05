from collections import deque
from graf_mapy import graf


class Mapa:
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.rodzic = None

    def ustaw_rodzica(self, rodzic):
        self.rodzic = rodzic


def znajdz_sasiadow(aktualny_wezel, odwiedzone_mapy):
    sasiedzi = graf.get(aktualny_wezel)
    return sasiedzi


def znajdz_sciezke(start, cel):
    kolejka = deque()
    obecny_wezel = Mapa(start)
    odwiedzone_mapy = []
    kolejka.append(obecny_wezel)
    odwiedzone_mapy.append(obecny_wezel)
    while kolejka:
        obecny_wezel = kolejka.popleft()
        sasiedzi = graf.get(obecny_wezel)
        for sasiad in sasiedzi:
            if sasiad.nazwa not in odwiedzone_mapy:
                sasiad.ustaw_rodzica(obecny_wezel)
                odwiedzone_mapy.append(sasiad.nazwa)
                kolejka.append(sasiad)
                if sasiad.nazwa == cel:
                    return sasiad
    print("Nie znaleziono ścieżki do celu")
    return None


print(znajdz_sciezke("Ithan", "Orla Grań"))
