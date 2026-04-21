import numpy as np
import random
import time
import matplotlib.pyplot as plt
import os
import pandas as pd

# Nastavenie rozsahu priestoru
X_MIN, X_MAX = -5000, 5000
Y_MIN, Y_MAX = -5000, 5000

# Pocet bodov
POCET_NAHODNYCH_BODOV = 20
POCET_GENEROVANYCH_BODOV = 40000
# POCET_NAHODNYCH_BODOV = 20
# POCET_GENEROVANYCH_BODOV = 2000

MAX_ITERACII = 100
SAVE_RESULTS_TO_FOLDER_PATH = 'C:/Zadanie2'
NAZOV_FIGURE_MEANS_CENTROID = "Figure-means-centroid-"
NAZOV_FIGURE_MEANS_MEDOID = "Figure-means-medoid-"
NAZOV_FIGURE_DIVIZNE_ZHLUKOVANIE = "Figure-divizne-zhlukovanie-"


# Generovanie prvych 20 nahodnych bodov s unikatnymi suradnicami
def generuj_prvych_20_bodov():
    body = []
    # Generovanie nahodnych bodov v pocte 20 kusov, pricom musia byt unikatne
    for i in range(20):
        x = random.randint(X_MIN, X_MAX)
        y = random.randint(Y_MIN, Y_MAX)
        # Tento cyklus zabezpecuje unikatnost, ak sa body nachadzaju medzi vygenerovanymi, tak sa vygeneruju nove
        while [x, y] in body:
            x = random.randint(X_MIN, X_MAX)
            y = random.randint(Y_MIN, Y_MAX)
        body.append([x, y])

    return list(body)


# Generovanie dalsich 40000 bodov podla zadania
def generuj_dalsie_body(povodne_body):
    # Skopirujem 20 bodov do celkoveho zoznamu bodov, vo vysledku bude 40020 bodov
    body = povodne_body.copy()

    # Generovanie nahodnych bodov v pocte 40000 kusov
    for _ in range(POCET_GENEROVANYCH_BODOV):

        # Nahodny vyber existujuceho bodu z doteraz vygenerovanych bodov
        index = random.randint(0, len(body) - 1)

        # Vyber nahodneho bodu - ziskanie suradnic bodu
        x_povodne, y_povodne = body[index]

        # Uprava intervalu offsetu, ak je bod blizko okraju
        x_min_offset = -100
        x_max_offset = 100
        y_min_offset = -100
        y_max_offset = 100

        # Urcenie hranic od bodu, kde sa mozem dostat (kvoli grafu v rosahu -5000, 5000)
        if x_povodne + 100 > X_MAX:
            x_max_offset = X_MAX - x_povodne
        if x_povodne - 100 < X_MIN:
            x_min_offset = X_MIN - x_povodne
        if y_povodne + 100 > Y_MAX:
            y_max_offset = Y_MAX - y_povodne
        if y_povodne - 100 < Y_MIN:
            y_min_offset = Y_MIN - y_povodne

        # Generovanie offsetov vo vypocitanych a urcenych hraniciach
        x_offset = random.randint(int(x_min_offset), int(x_max_offset))
        y_offset = random.randint(int(y_min_offset), int(y_max_offset))

        # Pridanie noveho bodu
        x_novy = x_povodne + x_offset
        y_novy = y_povodne + y_offset

        # Zaradenie bodu do mnoziny vygenerovanych bodov
        body.append((x_novy, y_novy))

    return body


# Funkcia na vypocet euklidovskej vzdialenosti medzi dvoma bodmi
def euklidovska_vzdialenost(bod1, bod2):
    return np.sqrt((bod1[0] - bod2[0]) ** 2 + (bod1[1] - bod2[1]) ** 2)


# Funkcia na vizualizaciu klastrov - vygenerovanie grafu s farebne oznacenymi klastrami
def vizualizuj_klastre(klastre, nazov_figure_file, ulozit_udaje_do_adresara, zobrazovat_priebezne_grafy, centroidy=None,
                       title=''):
    farby = plt.get_cmap('tab20', len(klastre))
    for index, klaster in enumerate(klastre):
        x = [bod[0] for bod in klaster]
        y = [bod[1] for bod in klaster]
        plt.scatter(x, y, color=farby(index), s=1)
    if centroidy:
        x_centroidy = [centroid[0] for centroid in centroidy]
        y_centroidy = [centroid[1] for centroid in centroidy]
        plt.scatter(x_centroidy, y_centroidy, color='black', marker='X', s=100)
        for i, centroid in enumerate(centroidy):
            plt.annotate(f'{i}', (centroid[0], centroid[1]))

    plt.title(title)
    if (zobrazovat_priebezne_grafy == 1):
        plt.show()
    if (ulozit_udaje_do_adresara == 1):
        plt.savefig(SAVE_RESULTS_TO_FOLDER_PATH + "/" + nazov_figure_file, dpi=300)
    plt.clf()


# Funkcia na vygenerovanie grafu na porovnanie uspesnosti jednotlivych behov - centroid
def vizualizuj_uspesnost_centroid(uspesnot_algoritmu_means_centroid):
    beh_index = []
    k_index = []
    uspesnost = []
    k_index_desc = []

    key_means_centroid = list(uspesnot_algoritmu_means_centroid.keys())
    uspesnost = list(uspesnot_algoritmu_means_centroid.values())

    for value in enumerate(key_means_centroid):
        beh_index.append(value[1][0])
        k_index.append(value[1][1])
        k_index_desc.append('k=' + str(value[1][1]))

    df = pd.DataFrame({'beh_index': beh_index,
                       'k_index': k_index,
                       'uspesnost': uspesnost})

    df.pivot(index='beh_index', columns='k_index', values='uspesnost').plot(kind='bar', rot=0)

    plt.title("Percentuálna úspešnosť algoritmu: means centroid")
    plt.xlabel("Číslo testu")
    plt.ylabel("Percentuálna úspešnosť [%]")
    plt.tight_layout()
    if (zobrazovat_priebezne_grafy == 1):
        plt.show()
    if (ulozit_udaje_do_adresara == 1):
        plt.savefig(SAVE_RESULTS_TO_FOLDER_PATH + "/" + NAZOV_FIGURE_MEANS_CENTROID + "uspesnost", dpi=300)
    plt.clf()


# Funkcia na vygenerovanie grafu na porovnanie uspesnosti jednotlivych behov - medoid
def vizualizuj_uspesnost_medoid(uspesnot_algoritmu_means_medoid):
    beh_index = []
    k_index = []
    uspesnost = []
    k_index_desc = []

    key_means_medoid = list(uspesnot_algoritmu_means_medoid.keys())
    uspesnost = list(uspesnot_algoritmu_means_medoid.values())

    for value in enumerate(key_means_medoid):
        beh_index.append(value[1][0])
        k_index.append(value[1][1])
        k_index_desc.append('k=' + str(value[1][1]))

    df = pd.DataFrame({'beh_index': beh_index,
                       'k_index': k_index,
                       'uspesnost': uspesnost})

    df.pivot(index='beh_index', columns='k_index', values='uspesnost').plot(kind='bar', rot=0)

    plt.title("Percentuálna úspešnosť algoritmu: means medoid")
    plt.xlabel("Číslo testu")
    plt.ylabel("Percentuálna úspešnosť [%]")
    plt.tight_layout()
    if (zobrazovat_priebezne_grafy == 1):
        plt.show()
    if (ulozit_udaje_do_adresara == 1):
        plt.savefig(SAVE_RESULTS_TO_FOLDER_PATH + "/" + NAZOV_FIGURE_MEANS_MEDOID + "uspesnost", dpi=300)
    plt.clf()


# Funkcia na vygenerovanie grafu na porovnanie uspesnosti jednotlivych behov - zhlukovanie
def vizualizuj_uspesnost_zhlukovanie(uspesnot_algoritmu_divizne_zhlukovanie):
    beh_index = []
    k_index = []
    uspesnost = []
    k_index_desc = []

    key_means_divizne_zhlukovanie = list(uspesnot_algoritmu_divizne_zhlukovanie.keys())
    uspesnost = list(uspesnot_algoritmu_divizne_zhlukovanie.values())

    for value in enumerate(key_means_divizne_zhlukovanie):
        beh_index.append(value[1][0])
        k_index.append(value[1][1])
        k_index_desc.append('k=' + str(value[1][1]))

    df = pd.DataFrame({'beh_index': beh_index,
                       'k_index': k_index,
                       'uspesnost': uspesnost})

    df.pivot(index='beh_index', columns='k_index', values='uspesnost').plot(kind='bar', rot=0)

    plt.title("Percentuálna úspešnosť algoritmu: divízne zhlukovanie")
    plt.xlabel("Číslo testu")
    plt.ylabel("Percentuálna úspešnosť [%]")
    plt.tight_layout()
    if (zobrazovat_priebezne_grafy == 1):
        plt.show()
    if (ulozit_udaje_do_adresara == 1):
        plt.savefig(SAVE_RESULTS_TO_FOLDER_PATH + "/" + NAZOV_FIGURE_DIVIZNE_ZHLUKOVANIE + "uspesnost", dpi=300)
    plt.clf()


# Implementacia k-means s centroidom ako stredom klastru
def k_means_centroid(body, k, max_iter):
    # Inicializacia centroidov
    centroidy = []

    # Inicializacia - nahodne sa vyberie k-centroidov
    while len(centroidy) < k:
        vygenerovany_bod = random.choice(body)
        # Vybrane body musia byt unikatne (nemozem vybrat rovnaky centroid)
        if vygenerovany_bod not in centroidy:
            centroidy.append(vygenerovany_bod)

    # Iterujem cez zadefinovany maximalny pocet iteracii (bud to skonci na iteraciach alebo ked sa nezmeni centroid)
    for iteracia in range(max_iter):

        klastrovanie = [[] for _ in range(k)]

        # Priradenie bodov k najblizsiemu centroidu cez euklidovsku vzdialenost
        # (kazdemu bodu najde najblizsi centroid a priradi ho)
        vzdialenosti = []
        for bod in body:
            for centroid in centroidy:
                vzdialenosti.append(euklidovska_vzdialenost(bod, centroid))
            index = vzdialenosti.index(min(vzdialenosti))
            klastrovanie[index].append(bod)
            vzdialenosti.clear()

        nove_centroidy = []

        # Aktualizacia centroidov - vypocita tazisko, stred bodov v ramci jedneho klastra
        for skupina in klastrovanie:
            if len(skupina) > 0:
                x_body = []
                y_body = []
                for bod in skupina:
                    x_body.append(bod[0])
                    y_body.append(bod[1])
                x_priemer = np.mean(x_body)
                y_priemer = np.mean(y_body)
                # Do nove_centroidy dam novovypocitany centroid (tazisko bodov v ramci klastra)
                nove_centroidy.append((x_priemer, y_priemer))
            else:
                # Ak je klaster prazdny, zvolim novy nahodny centroid
                nove_centroidy.append(random.choice(body))

        # Kontrola konvergencie - ak vysli rovnake centroidy, centroidy sa nepohli - koncim
        if np.allclose(centroidy, nove_centroidy):
            break
        else:
            # Priradim do centroidy novoziskane centroidy
            centroidy = nove_centroidy

    return klastrovanie, centroidy


# Implementacia k-means s medoidom ako stredom klastru
def k_means_medoid(body, k, max_iter=100):
    # Inicializacia medoidov
    medoidy = []

    # Inicializacia - nahodne sa vyberie k-medoidov
    while len(medoidy) < k:
        vygenerovany_bod = random.choice(body)
        # Vybrane body musia byt unikatne (nemozem vybrat rovnaky medoid)
        if vygenerovany_bod not in medoidy:
            medoidy.append(vygenerovany_bod)

    # Iterujem cez zadefinovany maximalny pocet iteracii (bud to skonci na iteraciach alebo ked sa nezmeni medoid)
    for iteracia in range(max_iter):
        klastrovanie = [[] for _ in range(k)]

        # Priradenie bodov k najblizsiemu medoidu cez euklidovsku vzdialenost
        # (kazdemu bodu najde najblizsi medoid a priradi ho)
        vzdialenosti = []
        for bod in body:
            for medoid in medoidy:
                vzdialenosti.append(euklidovska_vzdialenost(bod, medoid))
            index = vzdialenosti.index(min(vzdialenosti))
            klastrovanie[index].append(bod)
            vzdialenosti.clear()

        nove_medoidy = []
        # Aktualizacia medoidov - vypocita vzajomne vzdialenosti medzi bodmi, ku kazdemu bodu v ramci klastra
        # a ten, co ma najmensiu vzdialenost k ostatnym bodom sa stane novym medoidom
        # medoid je jeden z existujucich bodov z klastra
        for skupina in klastrovanie:
            if len(skupina) > 0:
                suma_vzdialenosti = []
                for kandidat in skupina:
                    suma = sum([euklidovska_vzdialenost(kandidat, bod) for bod in skupina])
                    suma_vzdialenosti.append((suma, kandidat))

                # Vyber medoidu s minimalnou sumou vzdialenosti
                nove_medoidy.append(min(suma_vzdialenosti, key=lambda t: t[0])[1])
            else:
                # Ak je klaster prazdny, zvolim novy nahodny medoid
                nove_medoidy.append(random.choice(body))

        # Kontrola konvergencie - ak vysli rovnake medoidy
        if medoidy == nove_medoidy:
            break
        else:
            # Priradim do medoidy novoziskane medoidy
            medoidy = nove_medoidy

    return klastrovanie, medoidy


# Implementacia divizneho zhlukovania s centroidom
def divizne_zhlukovanie(body, k, prah=500):
    # Inicializacia parametrov
    klastre = [body]
    finalne_klastre = []
    centroidy = []

    # Prechadzanie vsetkych klastrov
    while klastre:
        # Vyberiem prvy klaster v poradi a ten, co som vybrala, vyhodim zo zoznamu
        aktualny_klaster = klastre.pop(0)

        # Vypocet centroidu aktualneho klastra
        x_priemer = np.mean([bod[0] for bod in aktualny_klaster])
        y_priemer = np.mean([bod[1] for bod in aktualny_klaster])
        centroid = (x_priemer, y_priemer)

        # Vypocet priemernej vzdialenosti od centroidu
        avg_dist = np.mean([euklidovska_vzdialenost(bod, centroid) for bod in aktualny_klaster])

        if avg_dist > prah and len(aktualny_klaster) > 1:
            # Mnozenie - Rozdelenie klastra pomocou k-means s k=2
            klastrovanie, _ = k_means_centroid(aktualny_klaster, k, MAX_ITERACII)
            klastre.extend(klastrovanie)
        else:
            centroidy.append(centroid)
            finalne_klastre.append(aktualny_klaster)

    return finalne_klastre, centroidy


def skontrolovat_existenciu_adresara_ulozenia():
    try:
        # Ak adresar, do ktoreho budu vytvarane grafy este neexistuje, tak ho vytvorim
        if not os.path.exists(SAVE_RESULTS_TO_FOLDER_PATH):
            # Vytvorenie pozadovaneho adresara
            os.mkdir(SAVE_RESULTS_TO_FOLDER_PATH)
            print(f"Adresar '{SAVE_RESULTS_TO_FOLDER_PATH}' bol uspesne vytvoreny.")
    except PermissionError:
        print(f"Nedostatocne opravnenia: Nie je mozne vytvorit adresar: '{SAVE_RESULTS_TO_FOLDER_PATH}'.")
    except Exception as e:
        print(f"Nastala neocakavana chyba: {e}")


if __name__ == '__main__':
    # Vyziadanie vstupnych parametrov z konzoly
    # Zadanie poctu opakovani
    pocet_opakovani = int(input("Zadajte cislo poctu opakovani:"))
    # Vyber moznosti ukladania alebo neukladania grafu do suboru
    ulozit_udaje_do_adresara = int(input("Ulozit generovane udaje do adresara (0 - nie, 1 - ano):"))
    # Vyber moznosti zobrazovania alebo nezobrazovania grafu na obrazovke
    zobrazovat_priebezne_grafy = int(input("Zobrazovat priebezne grafy (0 - nie, 1 - ano):"))

    # Vytvorenie adresara pre ulozenie grafov
    skontrolovat_existenciu_adresara_ulozenia()

    # Inicializacia poli pre vyhodnotenie % uspesnosti klastrov v jednotlivych metodach vypoctu
    uspesnot_algoritmu_means_centroid = {}
    uspesnot_algoritmu_means_medoid = {}
    uspesnot_algoritmu_divizne_zhlukovanie = {}

    for beh_id in range(1, pocet_opakovani + 1):

        print(f"**** Beh: {beh_id}")

        # Generovanie bodov
        povodne_body = generuj_prvych_20_bodov()
        vsetky_body = generuj_dalsie_body(povodne_body)

        # Prevedenie na numpy array pre efektivitu
        vsetky_body = np.array(vsetky_body)

        # k-means s centroidom
        print("* k-means s centroidom")
        # k = 20
        pocet_idov = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

        for k in pocet_idov:

            print("* k-means s centroidom - k=" + str(k))

            # Vytvorenie nazvu grafu pre centroid
            nazov_figure = NAZOV_FIGURE_MEANS_CENTROID + str(beh_id) + '-' + str(k) + '.png'

            # Zaciatok merania casu trvania vypoctu metody - k_means_centroid
            start_time = time.time()

            # Spustenie vypoctu, vytvorenie klastrov s centroidmi
            klastrovanie_centroid, centroidy = k_means_centroid(vsetky_body.tolist(), k, MAX_ITERACII)

            # Koniec merania casu trvania vypoctu metody - k_means_centroid
            trvanie_time = time.time() - start_time
            print(f"Riesenie najdene za {trvanie_time:.2f} sekund.")

            # Vyhodnotenie uspesnosti
            uspesny = True

            # Inicializacia poctu neuspesnych centroidov v klastri
            klastrovanie_centroid_neuspesne = 0

            # Prechadzanie centroidov
            for i, klaster in enumerate(klastrovanie_centroid):
                centroid = centroidy[i]

                avg_dist = np.mean([euklidovska_vzdialenost(bod, centroid) for bod in klaster])

                # Ak je priemerna vzdialenost vacsia ako 500, potom je klastrovanie neuspesne
                if avg_dist > 500:
                    uspesny = False

                    # Zvysovanie poctu neuspesnych centroidov v klastri
                    klastrovanie_centroid_neuspesne += 1
                    print(f"Klaster {i} ma priemernu vzdialenost {avg_dist}, co presahuje 500.")

            # Ak su vsetky klastre uspesne, potom k-means s centroidom je uspesny podla definovaneho kriteria
            if uspesny:
                print("k-means s centroidom je uspesny podla definovaneho kriteria.")
            else:
                # Ak je minimalne jeden klaster neuspesny, potom k-means s centroidom nie je uspesny podla definovaneho kriteria
                print("k-means s centroidom nie je uspesny podla definovaneho kriteria.")

            # Vytvorenie nadpisu do grafu, zobrazujem nazov, cas trvania vypoctu metody a pocet uspesnych / celkovych klastrov
            title = f"k-means s centroidom - cas:{trvanie_time:.2f}, {len(klastrovanie_centroid) - klastrovanie_centroid_neuspesne}/{len(klastrovanie_centroid)}"

            # Vizualizacia grafu s farebne oznacenymi klastrami - vytvorenie samotneho grafu
            vizualizuj_klastre(klastrovanie_centroid, nazov_figure, ulozit_udaje_do_adresara,
                               zobrazovat_priebezne_grafy, centroidy, title)

            # Vypocet uspesnosti klastrovania, aby som zobrazila % uspesnosti klastrov v iteracii
            uspesnot_behu = 100 - (klastrovanie_centroid_neuspesne / len(klastrovanie_centroid)) * 100
            uspesnot_algoritmu_means_centroid[beh_id, k] = uspesnot_behu

        # k-means s medoidom
        for k in pocet_idov:

            print("* k-means s medoidom - k=" + str(k))

            # Vytvorenie nazvu grafu pre medoidy
            nazov_figure = NAZOV_FIGURE_MEANS_MEDOID + str(beh_id) + '-' + str(k) + '.png'

            # Zaciatok merania casu trvania vypoctu metody - k_means_medoid
            start_time = time.time()

            # Spustenie vypoctu, vytvorenie klastrov s medoidmi
            klastrovanie_medoid, medoidy = k_means_medoid(vsetky_body.tolist(), k)

            # Koniec merania casu trvania vypoctu metody - k_means_medoid
            trvanie_time = time.time() - start_time
            print(f"Riesenie najdene za {trvanie_time:.2f} sekund.")

            # Vyhodnotenie uspesnosti
            uspesny = True

            # Inicializacia poctu neuspesnych medoidov v klastri
            klastrovanie_medoid_neuspesne = 0

            # Prechadzanie medoidov
            for i, klaster in enumerate(klastrovanie_medoid):
                medoid = medoidy[i]
                avg_dist = np.mean([euklidovska_vzdialenost(bod, medoid) for bod in klaster])

                # Ak je priemerna vzdialenost vacsia ako 500, potom je klastrovanie neuspesne
                if avg_dist > 500:
                    uspesny = False

                    # Zvysovanie poctu neuspesnych medoidov v klastri
                    klastrovanie_medoid_neuspesne += 1
                    print(f"Klaster {i} ma priemernu vzdialenost {avg_dist}, co presahuje 500.")

            # Ak su vsetky klastre uspesne, potom k-means s medoidom je uspesny podla definovaneho kriteria
            if uspesny:
                print("k-means s medoidom je uspesny podla definovaneho kriteria.")
            else:
                # Ak je minimalne jeden klaster neuspesny, potom k-means s medoidom nie je uspesny podla definovaneho kriteria
                print("k-means s medoidom nie je uspesny podla definovaneho kriteria.")

            # Vytvorenie nadpisu do grafu, zobrazujem nazov, cas trvania vypoctu metody a pocet uspesnych / celkovych klastrov
            title = f"k-means s medoidom - cas:{trvanie_time:.2f}, {len(klastrovanie_medoid) - klastrovanie_medoid_neuspesne}/{len(klastrovanie_medoid)}"

            # Vizualizacia grafu s farebne oznacenymi klastrami - vytvorenie samotneho grafu
            vizualizuj_klastre(klastrovanie_medoid, nazov_figure, ulozit_udaje_do_adresara, zobrazovat_priebezne_grafy,
                               medoidy, title)

            # Vypocet uspesnosti klastrovania, aby som zobrazila % uspesnosti klastrov v iteracii
            uspesnot_behu = 100 - (klastrovanie_medoid_neuspesne / len(klastrovanie_medoid)) * 100
            uspesnot_algoritmu_means_medoid[beh_id, k] = uspesnot_behu

        # Divizne zhlukovanie s centroidom
        print("* divizne zhlukovanie s centroidom")

        # Vytvorenie nazvu grafu pre divizne zhlukovanie
        nazov_figure = NAZOV_FIGURE_DIVIZNE_ZHLUKOVANIE + str(beh_id) + '.png'

        # Zaciatok merania casu trvania vypoctu metody - divizne_zhlukovanie
        start_time = time.time()

        # Spustenie vypoctu - divizne_zhlukovanie
        k = 2
        finalne_klastre, centroidy = divizne_zhlukovanie(vsetky_body.tolist(), k)

        # Koniec merania casu trvania vypoctu metody - divizne_zhlukovanie
        trvanie_time = time.time() - start_time
        print(f"Riesenie najdene za {trvanie_time:.2f} sekund.")

        # Vyhodnotenie uspesnosti
        uspesny = True

        # Kontrola uspesnosti
        klastrovanie_divizne_zhlukovanie_neuspesne = 0
        for i, klaster in enumerate(finalne_klastre):
            x_priemer = np.mean([bod[0] for bod in klaster])
            y_priemer = np.mean([bod[1] for bod in klaster])
            centroid = (x_priemer, y_priemer)
            avg_dist = np.mean([euklidovska_vzdialenost(bod, centroid) for bod in klaster])

            # Ak je priemerna vzdialenost vacsia ako 500, potom je klastrovanie neuspesne
            if avg_dist > 500:
                uspesny = False
                klastrovanie_divizne_zhlukovanie_neuspesne += 1
                print(f"Klaster {i} ma priemernu vzdialenost {avg_dist}, co presahuje 500.")

        # Ak su vsetky klastre uspesne, potom divizne zhlukovanie je uspesne podla definovaneho kriteria
        if uspesny:
            print("Divizne zhlukovanie je uspesne podla definovaneho kriteria.")
        else:
            # Ak je minimalne jeden klaster neuspesny, potom divizne zhlukovanie nie je uspesne podla definovaneho kriteria
            # Toto nikdy nenastane
            print("Divizne zhlukovanie nie je uspesne podla definovaneho kriteria.")

        # Vytvorenie nadpisu do grafu, zobrazujem nazov, cas trvania vypoctu metody a pocet uspesnych / celkovych klastrov
        title = f"Divizne zhlukovanie s centroidom - cas:{trvanie_time:.2f}, {len(klastrovanie_centroid) - klastrovanie_centroid_neuspesne}/{len(klastrovanie_centroid)}"

        # Vizualizacia grafu s farebne oznacenymi klastrami - vytvorenie samotneho grafu
        vizualizuj_klastre(finalne_klastre, nazov_figure, ulozit_udaje_do_adresara, zobrazovat_priebezne_grafy,
                           centroidy, title)

        # Vypocet uspesnosti klastrovania, aby som zobrazila % uspesnosti klastrov v iteracii
        # Toto bude vzdy 100%
        uspesnot_behu = 100 - (klastrovanie_divizne_zhlukovanie_neuspesne / len(finalne_klastre)) * 100
        uspesnot_algoritmu_divizne_zhlukovanie[beh_id, k] = uspesnot_behu

    # Vizualizacia uspesnosti do grafu
    vizualizuj_uspesnost_centroid(uspesnot_algoritmu_means_centroid)
    vizualizuj_uspesnost_medoid(uspesnot_algoritmu_means_medoid)
    vizualizuj_uspesnost_zhlukovanie(uspesnot_algoritmu_divizne_zhlukovanie)