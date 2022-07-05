from queue import LifoQueue
kordy = [[1, 5], [1, 6], [1, 7], [1, 8], [1, 9], [2, 9], [2, 8], [2, 7], [2, 6], [3, 6], [3, 5], [3, 7], [3, 8], [3, 9],
         [4, 9], [4, 8], [4, 7], [4, 6], [4, 5], [5, 5], [5, 6], [5, 7], [5, 8], [5, 9], [6, 9], [6, 8], [6, 7], [6, 6],
         [6, 5], [7, 5], [7, 6], [7, 7], [7, 8], [7, 9], [7, 10], [7, 11], [6, 11], [5, 11], [4, 11], [3, 11], [8, 5],
         [8, 6], [8, 7], [8, 8], [8, 9], [8, 10], [9, 10], [9, 9], [9, 8], [9, 7], [9, 6], [10, 7], [10, 8], [11, 8],
         [11, 7], [11, 6], [11, 5], [12, 8], [12, 7], [12, 6], [13, 6], [13, 5], [13, 7], [13, 8], [13, 9], [14, 9],
         [14, 8], [14, 7], [14, 6]]
kordy.sort()

def ZnajdzSciezke(kordyMapy, cel):
    # Umieszczanie bieżącego węzła na stosie.
    #obecnePolozenie = [5, 5]
    odwiedzonePola = []
    stos = LifoQueue
    stos.put([5, 5])
    # Kontynuowanie przeszukiwania, dopóki występują węzły na stosie.
    while stos:
        # Ustawianie następnego węzła ze stosu jako bieżącego.
        nastepnyKrok = stos.get()
        # Jeśli bieżący węzeł nie został jeszcze sprawdzony, należy go zbadać.
        if not CzyJestwOdwiedzonych(nastepnyKrok, odwiedzonePola):
            odwiedzonePola.append(nastepnyKrok)
            # Zwracanie ścieżki do bieżącego sąsiada, jeśli jest celem.
            if nastepnyKrok == cel:
                return nastepnyKrok
            else:
                # Dodawanie sąsiadów bieżącego węzła do stosu.
                neighbors = ZnajdzSasiadow(nastepnyKrok, kordyMapy)
                for neighbor in neighbors:
                    rodzic = nastepnyKrok
                    stos.put(rodzic)
    return 'Brak ścieżki do celu.'


# Funkcja określająca, czy punkt został już odwiedzony.
def CzyJestwOdwiedzonych(obecnePolozenie, odwiedzonePola):
    if obecnePolozenie in odwiedzonePola:
        return True
    else:
        return False


def ZnajdzSasiadow(polozenie, dostepneKordy):
    sasiedzi = [[polozenie[0] - 1, polozenie[1]], [polozenie[0] + 1, polozenie[1]],
                [polozenie[0], polozenie[1] - 1], [polozenie[0], polozenie[1] + 1]]
    print(sasiedzi)
    for punkt in sasiedzi:
        if not punkt in dostepneKordy:
            sasiedzi.remove(punkt)
    return sasiedzi


print(ZnajdzSciezke(kordy, [14, 6]))
# print(ZnajdzSasiadow([5, 5], kordy, odwiedzonePola))
