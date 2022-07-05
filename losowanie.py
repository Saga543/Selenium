from random import choice


lista = list(range(1, 3001))
print(lista)
ilosc_prob = []
liczba_do_trafienia = []
for x in range(0, 100):
    i = 0
    traf = choice(lista)
    liczba_do_trafienia.append(traf)
    while True:
        i += 1
        los = choice(lista)
        print(los)
        if los == traf:
            print(f"Trafiony po {i} razie")
            ilosc_prob.append(i)
            break

print(f"Lista liczb do trafienia:       {liczba_do_trafienia}")
print(f"Lista ilości prób:              {ilosc_prob}")
suma = 0
for x in ilosc_prob:
    suma += x
srednia = suma / 100
print(f"Średnia ilośc potrzebnych losów: {srednia}")
