from collections import deque

kordy = [[1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [2, 6], [2, 7], [2, 8], [2, 9], [3, 5], [3, 6], [3, 7], [3, 8],
         [3, 9], [3, 11], [4, 5], [4, 6], [4, 7], [4, 8], [4, 9], [4, 11], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9],
         [5, 11], [6, 5], [6, 6], [6, 7], [6, 8], [6, 9], [6, 11], [7, 5], [7, 6], [7, 7], [7, 8], [7, 9], [7, 10],
         [7, 11], [8, 5], [8, 6], [8, 7], [8, 8], [8, 9], [8, 10], [9, 6], [9, 7], [9, 8], [9, 9], [9, 10], [10, 7],
         [10, 8], [11, 5], [11, 6], [11, 7], [11, 8], [12, 6], [12, 7], [12, 8], [13, 5], [13, 6], [13, 7], [13, 8],
         [13, 9], [14, 6], [14, 7], [14, 8], [14, 9]]
odwiedzone = [[1, 5], [1, 6], [1, 7], [1, 8], [1, 9]]


class Punkt:
    def __init__(self, kordy: []):
        self.kordy = kordy
        self.rodzic = None

    def UstawRodzica(self, rodzic):
        self.rodzic = rodzic


def ZnajdzSasiadow(polozenie, dostepneKordy, odwiedzone):
    potencjalnisasiedzi = [[polozenie[0] - 1, polozenie[1]], [polozenie[0], polozenie[1] - 1],
                           [polozenie[0] + 1, polozenie[1]], [polozenie[0], polozenie[1] + 1]]
    sasiedzi = []
    for sasiad in potencjalnisasiedzi:
        punkt = Punkt(sasiad)
        if (punkt.kordy in dostepneKordy) and (not punkt.kordy in odwiedzone):
            sasiedzi.append(punkt)
    return sasiedzi


def ZnajdzSciezke(kordyMapy, cel):
    kolejka = deque()
    obecnyWezel = Punkt([1, 5])
    odwiedzonePola = []
    kolejka.append(obecnyWezel)
    odwiedzonePola.append(obecnyWezel)
    while kolejka:
        obecnyWezel = kolejka.popleft()
        dzieci = ZnajdzSasiadow(obecnyWezel.kordy, kordyMapy, odwiedzonePola)
        for dziecko in dzieci:
            if not dziecko.kordy in odwiedzonePola:
                dziecko.UstawRodzica(obecnyWezel)
                odwiedzonePola.append(dziecko.kordy)
                kolejka.append(dziecko)
                if dziecko.kordy == cel:
                    return dziecko
    return 'Nie znaleziono ścieżki do celu.'


def get_path(point):
    path = []
    current_point = point
    while current_point.rodzic is not None:
        path.append(current_point.kordy)
        current_point = current_point.rodzic
    return path


sciezka = ZnajdzSciezke(kordy, [14, 9])
print(get_path(sciezka))



