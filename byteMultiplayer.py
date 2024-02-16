import copy
import queue

from tabulate import tabulate


#Ko prvi igra
igraPrvi = 'r'
velicinaTable = 8
naPotezu = 'O' #uvek krece O, X je crni O je beli
brojevi = [] #brojevi od 1 do velicinaTabele
slova = [] #slova od A do A+velicinaTabele
stanje =[]
brojStekovaX = 0
brojStekovaO = 0
gotovaIgra = False


def koPrviIgra():
    global igraPrvi
    while True:
        ulaz = input("Unesite ko prvi igra [c]ovek ili [r]acunar: ")
        if ulaz == 'r' or ulaz == 'c':
            igraPrvi = ulaz
            break
        else:
            print("Neispravan unos!")


def unesiVelicinuTable():
    global velicinaTable
    while True:
        ulaz = int(input("Unesite velicinu table: "))
        if ulaz in [8, 10, 14, 16]: #12 ne moze jer onda borj figura nije deljiv sa 8
            velicinaTable = ulaz
            break
        else:
            print("Dozvoljene velicine table su: 8, 10, 14 i 16.")


def generisiPocetnoStanje():
    global stanje, brojevi, slova
    brojevi = [1 + x for x in range(velicinaTable)]
    slova = [chr(ord('A') + i) for i in range(velicinaTable)]

    for i in range(velicinaTable):
        red = []
        for j in range(velicinaTable):
            if (i + j) % 2 == 1:
                red.append('.') #belo polje
            elif i == 0 or i == velicinaTable-1:
                red.append("") #prazno
            elif i % 2 == 1:
                red.append('X') #X igrac je crni
            else:
                red.append('O') #O igrac je beli
        stanje.append(red)

def prikaziStanje(stanje):
    global brojevi, slova
    prikaz = copy.deepcopy(stanje)

    def insert_column(matrix, column, position): #ukradena funkcija sa sajta
        for row, col_value in zip(matrix, column):
            row.insert(position, col_value)

    for i in range(len(stanje)):
        for j in range(len(stanje)):
            prikaz[i][j] = ''.join(prikaz[i][j])

    # Center-align the header text
    centrirani_brojevi = [f"{header:^6}" for header in brojevi]
    # Row names


    # Zip row names with data for tabulate
    insert_column(prikaz,slova,0)

    # Print table using tabulate with centered headers
    table = tabulate(prikaz, centrirani_brojevi, tablefmt="fancy_grid",colalign=("center", "center", "center"))
    print(table)
    print(f'Rezultat X: {brojStekovaX}  O: {brojStekovaO}\n')

def sledeciPotez():
    global naPotezu
    if naPotezu == 'X':
        naPotezu = 'O'
    else:
        naPotezu = 'X'


def tacanUnosPoteza(ulaz):
    podeljen = ulaz.split()
    if len(podeljen) != 4:
        return False

    red = podeljen[0]
    if not podeljen[1].isnumeric():
        return False
    kolona = int(podeljen[1])
    if not podeljen[2].isdigit():
        return False
    stekI = int(podeljen[2])
    smerI = podeljen[3][0]
    smerJ = podeljen[3][1]
    
    if smerI not in ['G', 'D'] or smerJ not in ['L', 'D']:
        print("Smer nije jedan od cetiri moguca")
        return False
    if red not in slova or kolona not in brojevi:
        print("Zadato polje ne postoji na tabli")
        return False
    red = ord(red) - ord('A')
    kolona -= 1
    if stekI not in range(7) or len(stanje[red][kolona])-1 < stekI:
        print("Nema figura na zadatom mestu u steku")
        return False

    if stanje[red][kolona][stekI] not in ['X', 'O']:
        print("Nema figura na zadatom polju")
        return False
    if stanje[red][kolona][stekI] != naPotezu:
        print("Izabrana figura u steku ne pripada igracu " + naPotezu)
        return False
    if red == 0 and smerI == "G":
        print("Ne može da se premesti gore")
        return False
    if red == velicinaTable-1 and smerI == "D":
        print("Ne moza da se premesti dole")
        return False
    if kolona == 0 and smerJ == "L":
        print("Ne moze da se premesti levo")
        return False
    if kolona == velicinaTable-1 and smerJ == "D":
        print("Ne moze da se premesti desno")
        return False

    return True


def unesiPotez():

    while True:
        ulaz = input(f"Potez {naPotezu} -> ")
        if tacanUnosPoteza(ulaz):
            return formatirajPotez(ulaz)
        else:
            print("Loš format poteza!")
    

def proveraKrajIgre():
    prag = (velicinaTable-2) * velicinaTable // 32 + 1 # u svakoj kolini N * ima (N-2)/2 figura, podeljeno sa 8 je broj stekova, i treba vise od pola za pobedu /2 + 1
    if brojStekovaX >= prag:
        print("**************************Pobednik je X!*********************************")
        zavrsenaIgra = True
        return True
    if brojStekovaO >= prag:
        print("**************************Pobednik je Y!*********************************")
        zavrsenaIgra = True
        return True
    return False


def getSusedna(stanje, i, j):
    susednaPolja = set()
    if i > 0:
        if j > 0:
            susednaPolja.add((i - 1, j - 1))
        if j < len(stanje[0]) - 1:
            susednaPolja.add((i - 1, j + 1))

    if i < len(stanje[0]) - 1:
        if j > 0:
            susednaPolja.add((i + 1, j - 1))
        if j < len(stanje[0]) - 1:
            susednaPolja.add((i + 1, j + 1))

    return susednaPolja


def getSmerZaSusedna(stanje, i, j):
    smerZaSusednaPolja = set()
    if i > 0:
        if j > 0:
            smerZaSusednaPolja.add((- 1, - 1))
        if j < len(stanje[0]) - 1:
            smerZaSusednaPolja.add((- 1, + 1))

    if i < len(stanje[0]) - 1:
        if j > 0:
            smerZaSusednaPolja.add((1,- 1))
        if j < len(stanje[0]) - 1:
            smerZaSusednaPolja.add((+ 1, + 1))

    return smerZaSusednaPolja


def praznaSusedna(stanje, i, j):
    for susedno in getSusedna(stanje, i, j):
         if stanje[susedno[0]][susedno[1]] != "":
            return False
    return True


def formatirajPotez(ulaz):
    podeljen = ulaz.split()

    if podeljen[3][0] == "G":
        i = -1
    else:
        i = 1
    if podeljen[3][1] == "L":
        j = -1
    else:
        j = 1
    return [ord(podeljen[0]) - ord('A'), int(podeljen[1])-1, int(podeljen[2]), i, j]


def udaljenostDoNajblizegBFS(stanje, i, j):
    red = queue.Queue(len(stanje) ** 2)
    visited = set()
    visited.add((i, j))
    red.put((i,j,0))# treca vrednost je dubina

    while not red.empty():
        pozicija = red.get()
        for sused in getSusedna(stanje, pozicija[0], pozicija[1]): #susedne kordinate
            if sused not in visited:
                if stanje[sused[0]][sused[1]] != "":
                    return pozicija[2]+1
                visited.add(sused)
                red.put(sused + (pozicija[2]+1,))


def pomeriStek(stanje, potez):
    stanje[potez[0] + potez[3]][potez[1] + potez[4]] = stanje[potez[0]][potez[1]]
    stanje[potez[0]][potez[1]] = ""
    return stanje


def vratiStek(stanje, potez):
    stanje[potez[0]][potez[1]] = stanje[potez[0] + potez[3]][potez[1] + potez[4]]
    stanje[potez[0] + potez[3]][potez[1] + potez[4]] = ""
    return stanje


def novoStanje(stanje, potez):
    novoS = copy.deepcopy(stanje)

    staroI = potez[0]
    staroJ =potez[1]
    novoI = staroI + potez[3]
    novoJ = staroJ + potez[4]

    novoS[novoI][novoJ] += novoS[staroI][staroJ][potez[2]:]
    novoS[staroI][staroJ] = novoS[staroI][staroJ][:potez[2]]

    return novoS


def premestiNaSusedni(stanje, potez):
    global brojStekovaO, brojStekovaX
    staroI = potez[0]
    staroJ =potez[1]
    novoI = staroI + potez[3]
    novoJ = staroJ + potez[4]
    if stanje[novoI][novoJ] == "":
        print("Stek se mora premestiti na susedni!")
        return False
    
    premesti = stanje[staroI][staroJ][potez[2]:]
    if len(premesti) + len(stanje[novoI][novoJ]) > 8:
        print("Novi stek ne sme da ima vise od 8 tokena")
        return False
    
    if potez[2] > len(stanje[novoI][novoJ]) - 1:
        print("Token se mora premestiti na visi nivo")
        return False
    

    stanje[novoI][novoJ] += premesti
    stanje[staroI][staroJ] = stanje[staroI][staroJ][:potez[2]]

    if len(stanje[novoI][novoJ]) == 8:
        if stanje[novoI][novoJ][7] == 'X':
            brojStekovaX = brojStekovaX + 1
            print("Igrac X je osvojio stek!")
        else:
            brojStekovaO = brojStekovaO + 1
            print("Igrac O je osvojio stek!")
        stanje[novoI][novoJ] = ""

    return True
    

def odigrajPotez(stanje, potez):
    if praznaSusedna(stanje, potez[0], potez[1]):
        if potez[2] != 0:
            print("Ceo stek mora biti pomeren ka najblizem steku!")
            return False
        if vodiDoNajblizeg(stanje, potez):
            pomeriStek(stanje, potez)
            sledeciPotez()
            return True
        else:
            print("Izabrani smer ne vodi do najblizeg steka")
            return False

    elif premestiNaSusedni(stanje, potez):
        sledeciPotez()
        return True
    return False


def vodiDoNajblizeg(stanje, potez):
    #potez je vec formatiran
    temp = stanje[potez[0]][potez[1]]
    stanje[potez[0]][potez[1]] = ""  #uklanjamo stek iz stanja da ne smeta, ali ga vracamo na kraju funkcije
    #prikaziStanje(stanje)
    staro = udaljenostDoNajblizegBFS(stanje, potez[0], potez[1])
    novo = udaljenostDoNajblizegBFS(stanje, potez[0] + potez[3], potez[1] + potez[4])
    stanje[potez[0]][potez[1]] = temp
    return novo < staro


def igraj():
    global naPotezu
    unesiVelicinuTable()
    generisiPocetnoStanje()
    prikaziStanje(stanje)

    while True:
        if not postojiMogucPotez(stanje, naPotezu):
            print(f"Igrac {naPotezu} nema moguc potez za igranje!")
            sledeciPotez()
        if odigrajPotez(stanje, unesiPotez()):
            prikaziStanje(stanje)
            if proveraKrajIgre():
                break


def getSvaNepraznaPolja(stanje):
    polja = []
    for i in range(len(stanje)):
        for j in range(len(stanje)):
            if (i+j) % 2 == 0 and stanje[i][j] != "":
                polja.append((i,j))

    return polja


def mozeNaSusedni(stanje, i, j, naPotezu):
    stari = stanje[i][j]
    for sused in getSusedna(stanje, i, j):
        novi = stanje[sused[0]][sused[1]]
        if novi == "":
            continue
        for ind in range(len(stari)):
            if stari[ind] != naPotezu:
                continue

            if len(stari[ind:]) + len(novi) > 8:
                continue
            
            if ind > len(novi) - 1:
                continue
            
            return True

    return False


def postojiMogucPotez(stanje, naPotezu):

    for polje in getSvaNepraznaPolja(stanje):
        i = polje[0]
        j = polje[1]
        if stanje[i][j][0] == naPotezu and praznaSusedna(stanje, i, j):
            return True
        if mozeNaSusedni(stanje, i, j, naPotezu):
            return True
    return False


def generisiStanja(stanje, potezi):
    stanja = []
    for p in potezi:
        stanja.append(novoStanje(stanje, p))

    return stanja


def generisiSvePoteze(stanje, naPotezu):
    potezi =[]
    for polje in getSvaNepraznaPolja(stanje):
        i = polje[0]
        j = polje[1]
        if stanje[i][j][0] == naPotezu and praznaSusedna(stanje, i, j):  #Nema susednih
            for smer in getSmerZaSusedna(stanje, i, j):
                potencijalniPotez = [i,j,0,smer[0],smer[1]]
                if vodiDoNajblizeg(stanje, potencijalniPotez):
                    potezi.append(potencijalniPotez)
        else:  #Ima susednih
            stari = stanje[i][j]
            for smerS in getSmerZaSusedna(stanje, i, j):
                novi = stanje[i+smerS[0]][j + smerS[1]]
                if novi == "":
                    continue
                for ind in range(len(stari)):
                    if stari[ind] != naPotezu:
                        continue

                    if len(stari[ind:]) + len(novi) > 8:
                        continue
                    
                    if ind > len(novi) - 1:
                        continue
                    
                    potezi.append([i,j,ind,smerS[0],smerS[1]])

    return potezi


def testGenerisiSvaStanja():
    global stanje
    testGenerisiPraznuTablu()
    stanje[1][1] = "OXO"
    stanje[2][2] = "XOXX"
    stanje[7][3] = "O"
    prikaziStanje(stanje)

    #for s in generisiStanja(stanje, generisiSvePoteze(stanje, "O")):
        #prikaziStanje(s)
    
    for p in generisiSvePoteze(stanje, "O"):
        prikaziStanje(novoStanje(stanje, p))
        print(p)
        print("\n")


def testGenerisiSvePoteze():
    global stanje
    testGenerisiPraznuTablu()
    stanje[1][1] = "XOXO"
    stanje[2][2] = "XOXXXXX"
    stanje[7][3] = "O"

    prikaziStanje(stanje)
    print(generisiSvePoteze(stanje, "O"))


def testPremestiNaSusedni():
    global stanje
    global brojStekovaX
    brojStekovaX= 2
    testGenerisiPraznuTablu()
    stanje[1][1] = "X"
    stanje[2][2] = "XOOOOOO"
    stanje[0][0] = "OX"
    stanje[7][3] = "O"
    prikaziStanje(stanje)
    premestiNaSusedni(stanje,[1,1,0,1,1])
    proveraKrajIgre()
    prikaziStanje(stanje)

def testMozeNaSusedni():
    global stanje
    testGenerisiPraznuTablu()
    stanje[1][1] = "XOX"
    stanje[2][2] = "XOOOOOO"
    stanje[0][0] = "OX"
    stanje[7][3] = "O"

    prikaziStanje(stanje)
    print(mozeNaSusedni(stanje, 1, 1, "O"))
        


def testOdigrajPotez():
    global stanje
    testGenerisiPraznuTablu()
    stanje[4][6] = "X"
    stanje[7][1] = "O"
    stanje[7][3] = "O"
    stanje[1][1] = "O"
    prikaziStanje(stanje)
    while True:
        if odigrajPotez(stanje, unesiPotez()):
            prikaziStanje(stanje)
        


def testVodiDoNajblizeg():
    global stanje
    testGenerisiPraznuTablu()
    stanje[4][6] = "X"
    stanje[7][1] = "O"
    stanje[7][3] = "O"
    stanje[1][1] = "O"
    prikaziStanje(stanje)
    while True:
        print(vodiDoNajblizeg(stanje, unesiPotez()))


def testGenerisiPraznuTablu():
    global stanje, brojevi, slova
    brojevi = [1 + x for x in range(velicinaTable)]
    slova = [chr(ord('A') + i) for i in range(velicinaTable)]

    for i in range(velicinaTable):
        red = []
        for j in range(velicinaTable):
            if (i + j) % 2 == 1:
                red.append('.') #belo polje
            elif i == 0 or i == velicinaTable-1:
                red.append("") #prazno
            elif i % 2 == 1:
                red.append("") #X igrac je crni
            else:
                red.append("") #O igrac je beli
        stanje.append(red)


def testSlobodnaSusedna():
    testGenerisiPraznuTablu()
    stanje[1][1] = "X"
    prikaziStanje(stanje)
    for i in range(velicinaTable):
        for j in range(velicinaTable):
            if (i + j) % 2 == 0:
                print("i= " + str(i) + " j= " + str(j), end=" ")
                print(praznaSusedna(stanje, i, j))


def testNajbliziStek():
    global stanje
    testGenerisiPraznuTablu()
    #stanje[4][6] = "XOXOXOXO"
    stanje[7][1] = "OOOOOOOO"
    stanje[7][3] = "XXXXXXXX"

    #stanje[4][6] = ""
    prikaziStanje(stanje)


    for i in range(velicinaTable):
        for j in range(velicinaTable):
            if (i + j) % 2 == 0:
                print("i= " + chr(i + ord("A")) + " j= " + str(j +1) + " udaljenost= ", end=" ")
                print(udaljenostDoNajblizegBFS(stanje, i, j))


if __name__ == '__main__':
    #koPrviIgra()
    
    igraj()
    #testGenerisiSvaStanja()
    

