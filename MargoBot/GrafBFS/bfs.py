from collections import deque


class Punkt:
    def __init__(self, kordy: []):
        self.kordy = kordy
        self.rodzic = None

    def ustaw_rodzica(self, rodzic):
        self.rodzic = rodzic


def znajdz_sasiadow(polozenie, dostepne_kordy, odwiedzone):
    potencjalni_sasiedzi = [[polozenie[0] - 1, polozenie[1]], [polozenie[0], polozenie[1] - 1],
                           [polozenie[0] + 1, polozenie[1]], [polozenie[0], polozenie[1] + 1]]
    sasiedzi = []
    for sasiad in potencjalni_sasiedzi:
        punkt = Punkt(sasiad)
        if (punkt.kordy in dostepne_kordy) and (punkt.kordy not in odwiedzone):
            sasiedzi.append(punkt)
    return sasiedzi


def znajdz_sciezke(start, cel, kordy_mapy):
    kolejka = deque()
    obecny_wezel = Punkt(start)
    odwiedzone_pola = []
    kolejka.append(obecny_wezel)
    odwiedzone_pola.append(obecny_wezel)
    while kolejka:
        obecny_wezel = kolejka.popleft()
        dzieci = znajdz_sasiadow(obecny_wezel.kordy, kordy_mapy, odwiedzone_pola)
        for dziecko in dzieci:
            if dziecko.kordy not in odwiedzone_pola:
                dziecko.ustaw_rodzica(obecny_wezel)
                odwiedzone_pola.append(dziecko.kordy)
                kolejka.append(dziecko)
                if dziecko.kordy == cel:
                    return dziecko
    print("Nie znaleziono ścieżki do celu")
    return None


def zwroc_sciezke(start: [], cel: [], mapa_kordy: []):
    """Zwraca listę kordynatów prowadzących do celu na podanych kordach lub None jeśli nie ma ścieżki do celu"""
    punkt = znajdz_sciezke(start, cel, mapa_kordy)
    if punkt is None:
        return None
    sciezka = []
    aktualny_punkt = punkt
    while aktualny_punkt.rodzic is not None:
        sciezka.append(aktualny_punkt.kordy)
        aktualny_punkt = aktualny_punkt.rodzic
    sciezka.reverse()
    return sciezka
