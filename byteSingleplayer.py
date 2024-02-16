import copy
import queue

from tabulate import tabulate



velicinaTable = 8
naPotezu = 'O' #uvek krece O, X je crni O je beli
brojevi = [] #brojevi od 1 do velicinaTabele
slova = [] #slova od A do A+velicinaTabele
brojStekovaX = 0
brojStekovaO = 0
gotovaIgra = False


def koPrviIgra():
    global igraPrvi
    while True:
        ulaz = input("Unesite ko prvi igra [c]ovek ili [r]acunar: ")
        if ulaz in ['r','R','c','C']:
            igraPrvi = ulaz
            return ulaz
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
    global brojevi, slova
    stanje = []
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
    return stanje


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
    naPotezu = 'O' if naPotezu == 'X' else 'X'
    '''
    if naPotezu == 'X':
        naPotezu = 'O'
    else:
        naPotezu = 'X'
    '''


def tacanUnosPoteza(stanje, ulaz):
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


def unesiPotez(stanje):
    while True:
        ulaz = input(f"Potez {naPotezu} -> ")
        if tacanUnosPoteza(stanje, ulaz):
            formatiranPotez = formatirajPotez(ulaz)
            if ispravanPotez(stanje, formatiranPotez):
                return formatiranPotez
        else:
            print("Loš format poteza!")
    

def proveraKrajIgre(brojStekovaX, brojStekovaO):
    prag = (velicinaTable-2) * velicinaTable // 32 + 1 # u svakoj kolini N * ima (N-2)/2 figura, podeljeno sa 8 je broj stekova, i treba vise od pola za pobedu /2 + 1
    if brojStekovaX >= prag:
        return True
    if brojStekovaO >= prag:
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

def formatPotezaZaPrikaz(potez):
    return f"{chr(potez[0] + ord('A'))} {potez[1] + 1} {potez[2]} {'G' if potez[3] == -1 else 'D'}{'L' if potez[4] == -1 else 'D'}"


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
    

def ispravanPotez(stanje, potez):
    if praznaSusedna(stanje, potez[0], potez[1]):
        if potez[2] != 0:
            print("Ceo stek mora biti pomeren ka najblizem steku!")
            return False
        if vodiDoNajblizeg(stanje, potez):
            return True
        else:
            print("Izabrani smer ne vodi do najblizeg steka")
            return False
    else:
        staroI = potez[0]
        staroJ = potez[1]
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
        
        return True
    

def odigrajPotezBezProvere(stanje, potez):
    global brojStekovaO, brojStekovaX
    if praznaSusedna(stanje, potez[0], potez[1]):  #premesta na susedno prazno polje ceo stek
        stanje[potez[0] + potez[3]][potez[1] + potez[4]] = stanje[potez[0]][potez[1]]
        stanje[potez[0]][potez[1]] = ""
        
    else:  
        staroI = potez[0]
        staroJ =potez[1]
        novoI = staroI + potez[3]
        novoJ = staroJ + potez[4]
        
        premesti = stanje[staroI][staroJ][potez[2]:]
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
    sledeciPotez()


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
    global naPotezu, brojStekovaX, brojStekovaO
    unesiVelicinuTable()
    trenutnoStanje = generisiPocetnoStanje()
    prikaziStanje(trenutnoStanje)

    while True:
        if not postojiMogucPotez(trenutnoStanje, naPotezu):
            print(f"Igrac {naPotezu} nema moguc potez za igranje!")
            sledeciPotez()
        odigrajPotezBezProvere(trenutnoStanje, unesiPotez(trenutnoStanje))
        prikaziStanje(trenutnoStanje)
        if proveraKrajIgre(brojStekovaX, brojStekovaO):
            if brojStekovaX > brojStekovaO:
                print("**************************Pobednik je X!*********************************")
            else:
                print("**************************Pobednik je O!*********************************")
            break


maxIgrac = "O"


def igrajRacunar():
    global naPotezu, brojStekovaX, brojStekovaO, maxIgrac
    unesiVelicinuTable()
    if koPrviIgra() in ['r', 'R']:
        maxIgrac = "O"
    else:
        maxIgrac = "X"
    trenutnoS = generisiPocetnoStanje()
    prikaziStanje(trenutnoS)

    while True:
        if not postojiMogucPotez(trenutnoS, naPotezu):
            print(f"Igrac {naPotezu} nema moguc potez za igranje!")
            sledeciPotez()
            continue
        if naPotezu == maxIgrac:    
            print("Racunar na potezu...")
            potezi = generisiSvePoteze(trenutnoS, naPotezu)
            print(f"Broj poteza: {len(potezi)}")
            noviPotez = max_value((trenutnoS, brojStekovaX, brojStekovaO))[0][3]
        else:
            noviPotez = unesiPotez(trenutnoS)
        #print(noviPotez[0][3])
        
        porukaOdigranPotez = f"Igrac {naPotezu} je odigrao: {formatPotezaZaPrikaz(noviPotez)} \n"
        odigrajPotezBezProvere(trenutnoS, noviPotez)
        prikaziStanje(trenutnoS)
        print(porukaOdigranPotez)

        if proveraKrajIgre(brojStekovaX, brojStekovaO):
            if brojStekovaX > brojStekovaO:
                print("**************************Pobednik je X!*********************************")
            else:
                print("**************************Pobednik je O!*********************************")
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
        novoS = novoStanje(stanje[0], p)

        brX = stanje[1]
        brY = stanje[2]
        staroI = p[0]
        staroJ =p[1]
        novoI = staroI + p[3]
        novoJ = staroJ + p[4]

        if len(novoS[novoI][novoJ]) == 8:
            if novoS[novoI][novoJ][7] == 'X':
                brX = brX + 1
            else:
                brY = brY + 1

            novoS[novoI][novoJ] = ""

        stanja.append((novoS, brX, brY, p))

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


def testProcenaStanje():
    global maxIgrac
    maxIgrac = "O"
    stanje = testGenerisiPraznuTablu()
    stanje[1][1] = "OXO"
    stanje[2][2] = "XOXX"
    stanje[7][3] = "O"
    prikaziStanje(stanje)

    #for s in generisiStanja(stanje, generisiSvePoteze(stanje, "O")):
        #prikaziStanje(s)
    
    for p in generisiSvePoteze(stanje, "O"):
        novoS = novoStanje(stanje, p)
        prikaziStanje(novoS)
        print(p)
        print(f"Procena stanja za {maxIgrac}: {oceni_stanje((novoS, 0, 0))}")
        print("\n")


def testGenerisiSvaStanja():
    
    stanje = generisiPocetnoStanje()

    prikaziStanje(stanje)

    #for s in generisiStanja(stanje, generisiSvePoteze(stanje, "O")):
        #prikaziStanje(s)
    
    for p in generisiSvePoteze(stanje, "O"):
        prikaziStanje(novoStanje(stanje, p))
        print(p)
        print("\n")


def testGenerisiSvePoteze():

    stanje = testGenerisiPraznuTablu()
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
    stanje = testGenerisiPraznuTablu()
    stanje[4][6] = "X"
    stanje[7][1] = "O"
    stanje[7][3] = "O"
    stanje[1][1] = "O"
    prikaziStanje(stanje)
    while True:
        if odigrajPotez(stanje, unesiPotez(stanje)):
            prikaziStanje(stanje)
        


def testVodiDoNajblizeg():

    stanje = testGenerisiPraznuTablu()
    stanje[4][6] = "X"
    stanje[7][1] = "O"
    stanje[7][3] = "O"
    stanje[1][1] = "O"
    prikaziStanje(stanje)
    while True:
        print(vodiDoNajblizeg(stanje, unesiPotez(stanje)))


def testGenerisiPraznuTablu():
    global brojevi, slova
    stanje = []
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
    return stanje


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


def oceni_stanje(stanje, maxIgrac):
    
    minIgrac = 'X' if maxIgrac == 'O' else 'O'
    val = 0
    if maxIgrac == "X":

        if proveraKrajIgre(stanje[1], stanje[2]):
            if stanje[1] > stanje[2]:
                val += 10000
            else:
                val += -10000
        
        val+=100*(stanje[1]-stanje[2])
    else:
        if proveraKrajIgre(stanje[1], stanje[2]):
            if stanje[1] < stanje[2]:
                val += 10000
            else:
                val += -10000
        val+=100*(stanje[2]-stanje[1])
        
    for i in range(len(stanje[0][0])):
        for j in range(len(stanje[0][0])):
            #if stanje[0][i][j] != "" and stanje[0][i][j][0] == maxIgrac:  #na dnu je moj
                #val += 1
            #elif stanje[0][i][j] != "" and stanje[0][i][j][0] == minIgrac:
                #val -= 1
            if len(stanje[0][i][j]) > 1:
                if stanje[0][i][j][0] == maxIgrac and stanje[0][i][j][-1] == maxIgrac: #na vrhu je moj i na dnju
                    val += len(stanje[0][i][j]) * 2 + stanje[0][i][j].count(maxIgrac)
                elif stanje[0][i][j][0] == minIgrac and stanje[0][i][j][-1] == minIgrac:
                    val -= len(stanje[0][i][j]) * 2 + stanje[0][i][j].count(minIgrac)

    return val



def max_value(stanje, dubina= None, alpha = (None, -1000000), beta= (None, 1000000), potez = None):  #stanje je touple (tabla, brojStekovaX, brojStekovaY)
    
    if proveraKrajIgre(stanje[1], stanje[2]):
        return (potez, oceni_stanje(stanje, naPotezu))
    
    if dubina == 0:
        return (potez, oceni_stanje(stanje, naPotezu))
    

    potezi = generisiSvePoteze(stanje[0], naPotezu)

    if dubina is None:
        brPoteza = len(potezi)

        if brPoteza > 100:
            dubina = 2
        elif brPoteza > 25:
            dubina = 3
        elif brPoteza > 15:
            dubina = 4
        elif brPoteza > 8:
            dubina = 5
        elif brPoteza > 6:
            dubina = 6
        else:
            dubina = 7
    

    if potezi is None or len(potezi) == 0:
        return (potez, oceni_stanje(stanje, naPotezu))
    
    lista_novih_stanja = generisiStanja(stanje, potezi)
    for s in lista_novih_stanja:
        alpha = max(alpha, min_value(s, dubina - 1, alpha, beta, s if potez is None else potez), key = lambda x: x[1])
    if alpha[1] >= beta[1]:
        return beta
    return alpha


def min_value(stanje, dubina = None, alpha = (None, -1000000), beta= (None, 1000000), potez = None):

    if proveraKrajIgre(stanje[1], stanje[2]) or dubina == 0:
        return (potez, oceni_stanje(stanje, naPotezu))
    
    potezi = generisiSvePoteze(stanje[0], "X" if naPotezu == "O" else "O" )

    if potezi is None or len(potezi) == 0:
        return (potez, oceni_stanje(stanje, naPotezu))


    lista_novih_stanja = generisiStanja(stanje, potezi)
    for s in lista_novih_stanja:
        beta = min(beta, max_value(s, dubina - 1, alpha, beta, s if potez is None else potez), key = lambda x: x[1])
    if beta[1] <= alpha[1]:
        return alpha
    return beta


if __name__ == '__main__':
    while True:
        igramSam = input("Unesite da li igrate sa [r]acunarom ili [c]ovekom: ")
        if igramSam in ['r','c', 'R', 'C']:
            break
        else:
            print("Pogresan ulaz")
    if igramSam in ['c', 'C']:
        igraj()
    else:          
        igrajRacunar()
    #testProcenaStanje()
    

