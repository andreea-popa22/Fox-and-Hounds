import time

import pygame, sys

ADANCIME_MAX = 6


def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    DENIED = '~'
    GOL = '#'

    @classmethod
    def initializeaza(cls, display, NR_COLOANE=8, dim_celula=100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.hounds_img = pygame.image.load('black.png')
        cls.hounds_img = pygame.transform.scale(cls.hounds_img, (dim_celula, dim_celula))
        cls.fox_img = pygame.image.load('red.png')
        cls.fox_img = pygame.transform.scale(cls.fox_img, (dim_celula, dim_celula))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self):  # tabla de exemplu este ["#","x","#","0",......]

        for ind in range(self.__class__.NR_COLOANE**2):
            linie = ind // self.__class__.NR_COLOANE  # // inseamna div
            coloana = ind % self.__class__.NR_COLOANE

            white = (255, 255, 255)
            black = (0, 0, 0)
            if linie % 2 == 0 and coloana % 2 == 1 or linie % 2 == 1 and coloana % 2 == 0:
                pygame.draw.rect(self.__class__.display, black, self.__class__.celuleGrid[ind])
            else:
                pygame.draw.rect(self.__class__.display, white, self.__class__.celuleGrid[ind])
            if self.matr[linie][coloana] == 'h':
                self.__class__.display.blit(self.__class__.hounds_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
            elif self.matr[linie][coloana] == 'f':
                self.__class__.display.blit(self.__class__.fox_img, (
                coloana * (self.__class__.dim_celula + 1), linie * (self.__class__.dim_celula + 1)))
        pygame.display.flip()  # obligatoriu pentru a actualiza interfata (desenul)

    #pygame.display.update()

    def __init__(self, tabla=None):
        if tabla:
            self.matr = tabla
        else:
            self.matr = [[self.__class__.GOL] * 8 for i in range(8)]

            for linie in range(8):
                for coloana in range(8):
                    if linie == 0 and coloana % 2 == 1:
                        self.matr[linie][coloana] = 'h'
                    elif linie % 2 == 0 and coloana % 2 == 0 or linie % 2 == 1 and coloana % 2 == 1:
                        self.matr[linie][coloana] = self.__class__.DENIED
            self.matr[7][0] = 'f'


    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        rez = (elem_identice(self.matr[0:3])
               or elem_identice(self.matr[3:6])
               or elem_identice(self.matr[6:9])
               or elem_identice(self.matr[0:9:3])
               or elem_identice(self.matr[1:9:3])
               or elem_identice(self.matr[2:9:3])
               or elem_identice(self.matr[0:9:4])
               or elem_identice(self.matr[2:8:2]))
        if (rez):
            return rez
        elif self.__class__.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            if self.matr[i] == self.__class__.GOL:
                matr_tabla_noua = list(self.matr)
                matr_tabla_noua[i] = jucator_opus
                l_mutari.append(Joc(matr_tabla_noua))
        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
        # verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
            return 1
        return 0

    def linii_deschise(self, jucator):
        return (self.linie_deschisa(self.matr[0:3], jucator)
                + self.linie_deschisa(self.matr[3:6], jucator)
                + self.linie_deschisa(self.matr[6:9], jucator)
                + self.linie_deschisa(self.matr[0:9:3], jucator)
                + self.linie_deschisa(self.matr[1:9:3], jucator)
                + self.linie_deschisa(self.matr[2:9:3], jucator)
                + self.linie_deschisa(self.matr[0:9:4], jucator)  # prima diagonala
                + self.linie_deschisa(self.matr[2:8:2], jucator))  # a doua diagonala

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        # if (adancime==0):
        if t_final == self.__class__.JMAX:
            return (99 + adancime)
        elif t_final == self.__class__.JMIN:
            return (-99 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN))

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0:3]]) + "\n" +
               " ".join([str(x) for x in self.matr[3:6]]) + "\n" +
               " ".join([str(x) for x in self.matr[6:9]]) + "\n")

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False

class Buton:
    def __init__(self, display=None, left=0, top=0, w=0, h=0, culoareFundal=(53, 80, 115),
                 culoareFundalSel=(89, 134, 194), text="", font="arial", fontDimensiune=16, culoareText=(255, 255, 255),
                 valoare=""):
        self.display = display
        self.culoareFundal = culoareFundal
        self.culoareFundalSel = culoareFundalSel
        self.text = text
        self.font = font
        self.w = w
        self.h = h
        self.selectat = False
        self.fontDimensiune = fontDimensiune
        self.culoareText = culoareText
        # creez obiectul font
        fontObj = pygame.font.SysFont(self.font, self.fontDimensiune)
        self.textRandat = fontObj.render(self.text, True, self.culoareText)
        self.dreptunghi = pygame.Rect(left, top, w, h)
        # aici centram textul
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)
        self.valoare = valoare

    def selecteaza(self, sel):
        self.selectat = sel
        self.deseneaza()

    def selecteazaDupacoord(self, coord):
        if self.dreptunghi.collidepoint(coord):
            self.selecteaza(True)
            return True
        return False

    def updateDreptunghi(self):
        self.dreptunghi.left = self.left
        self.dreptunghi.top = self.top
        self.dreptunghiText = self.textRandat.get_rect(center=self.dreptunghi.center)

    def deseneaza(self):
        culoareF = self.culoareFundalSel if self.selectat else self.culoareFundal
        pygame.draw.rect(self.display, culoareF, self.dreptunghi)
        self.display.blit(self.textRandat, self.dreptunghiText)


class GrupButoane:
    def __init__(self, listaButoane=[], indiceSelectat=0, spatiuButoane=10, left=0, top=0):
        self.listaButoane = listaButoane
        self.indiceSelectat = indiceSelectat
        self.listaButoane[self.indiceSelectat].selectat = True
        self.top = top
        self.left = left
        leftCurent = self.left
        for b in self.listaButoane:
            b.top = self.top
            b.left = leftCurent
            b.updateDreptunghi()
            leftCurent += (spatiuButoane + b.w)

    def selecteazaDupacoord(self, coord):
        for ib, b in enumerate(self.listaButoane):
            if b.selecteazaDupacoord(coord):
                self.listaButoane[self.indiceSelectat].selecteaza(False)
                self.indiceSelectat = ib
                return True
        return False

    def deseneaza(self):
        # atentie, nu face wrap
        for b in self.listaButoane:
            b.deseneaza()

    def getValoare(self):
        return self.listaButoane[self.indiceSelectat].valoare


############# ecran initial ########################
def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=30,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Minimax", valoare="minimax"),
            Buton(display=display, w=80, h=30, text="Alpha-Beta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=100,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Fox", valoare="fox"),
            Buton(display=display, w=80, h=30, text="Hounds", valoare="hounds")
        ],
        indiceSelectat=0)
    btn_nvl = GrupButoane(
        top=170,
        left=30,
        listaButoane=[
            Buton(display=display, w=80, h=30, text="Usor", valoare="usor"),
            Buton(display=display, w=80, h=30, text="Mediu", valoare="mediu"),
            Buton(display=display, w=80, h=30, text="Avansat", valoare="avansat")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=240, left=30, w=40, h=30, text="ok", culoareFundal=(155, 0, 55))
    btn_alg.deseneaza()
    btn_juc.deseneaza()
    btn_nvl.deseneaza()
    ok.deseneaza()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if not btn_alg.selecteazaDupacoord(pos):
                    if not btn_juc.selecteazaDupacoord(pos):
                        if not btn_nvl.selecteazaDupacoord(pos):
                            if ok.selecteazaDupacoord(pos):
                                display.fill((0, 0, 0))  # stergere ecran
                                tabla_curenta.deseneaza_grid()
                                return btn_juc.getValoare(), btn_alg.getValoare(), btn_nvl.getValoare()
        pygame.display.update()

def calculeaza_adancime(nivel = "usor"):
    if nivel == "usor":
        h = 1
    elif nivel == "mediu":
        h = 2
    else: # nivel == "avansat"
        h = 3
    return h

# def efect_hover(btn_nvl):
#     mouse = pygame.mouse.get_pos()
#     if 170 + 80 > mouse[0] > 170 and  30 + 30 > mouse[1] > 30:
#         btn_nvl.culoareFuundal = (40, 80, 115)

def main():
    pygame.init()
    pygame.display.set_caption("Andreea - Fox and Hounds")
    nc = 8
    w = 100
    ecran = pygame.display.set_mode(size=(nc * (w + 1) - 1, nc * (w + 1) - 1))
    Joc.initializeaza(ecran, nc)


    tabla_curenta = Joc()
    Joc.JMIN, tip_algoritm, nivel = deseneaza_alegeri(ecran, tabla_curenta)
    ADANCIME_MAX = calculeaza_adancime(nivel)
    print(Joc.JMIN, tip_algoritm)

    Joc.JMAX = 'fox' if Joc.JMIN == 'hounds' else 'hounds'

    print("Tabla initiala")
    print(str(tabla_curenta))

    stare_curenta = Stare(tabla_curenta, 'hounds', ADANCIME_MAX)

    tabla_curenta.deseneaza_grid()
    # de_mutat = False
    # while True:
    #
    #     if (stare_curenta.j_curent == Joc.JMIN):
    #         # muta jucatorul
    #         # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
    #         # l=pygame.event.get()
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 pygame.quit()  # inchide fereastra
    #                 sys.exit()
    #             elif event.type == pygame.MOUSEBUTTONDOWN:
    #
    #                 pos = pygame.mouse.get_pos()  # coordonatele clickului
    #
    #                 for np in range(len(Joc.celuleGrid)):
    #
    #                     if Joc.celuleGrid[np].collidepoint(
    #                             pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
    #                         linie = np // 3
    #                         coloana = np % 3
    #                         ###############################
    #                         if stare_curenta.tabla_joc.matr[np] == Joc.JMIN:
    #                             if (de_mutat and linie == de_mutat[0] and coloana == de_mutat[1]):
    #                                 # daca am facut click chiar pe patratica selectata, o deselectez
    #                                 de_mutat = False
    #                                 stare_curenta.tabla_joc.deseneaza_grid()
    #                             else:
    #                                 de_mutat = (linie, coloana)
    #                                 # desenez gridul cu patratelul marcat
    #                                 stare_curenta.tabla_joc.deseneaza_grid(np)
    #                         if stare_curenta.tabla_joc.matr[np] == Joc.GOL:
    #                             if de_mutat:
    #                                 #### eventuale teste legate de mutarea simbolului
    #                                 stare_curenta.tabla_joc.matr[de_mutat[0] * 3 + de_mutat[1]] = Joc.GOL
    #                                 de_mutat = False
    #                             # plasez simbolul pe "tabla de joc"
    #                             stare_curenta.tabla_joc.matr[linie * 3 + coloana] = Joc.JMIN
    #
    #                             # afisarea starii jocului in urma mutarii utilizatorului
    #                             print("\nTabla dupa mutarea jucatorului")
    #                             print(str(stare_curenta))
    #
    #                             stare_curenta.tabla_joc.deseneaza_grid()
    #                             # testez daca jocul a ajuns intr-o stare finala
    #                             # si afisez un mesaj corespunzator in caz ca da
    #                             if (afis_daca_final(stare_curenta)):
    #                                 break
    #
    #                             # S-a realizat o mutare. Schimb jucatorul cu cel opus
    #                             stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
    #
    #
    #     # --------------------------------
    #     else:  # jucatorul e JMAX (calculatorul)
    #         # Mutare calculator
    #
    #         # preiau timpul in milisecunde de dinainte de mutare
    #         t_inainte = int(round(time.time() * 1000))
    #         if tip_algoritm == '1':
    #             stare_actualizata = min_max(stare_curenta)
    #         else:  # tip_algoritm==2
    #             stare_actualizata = alpha_beta(-500, 500, stare_curenta)
    #         stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
    #         print("Tabla dupa mutarea calculatorului")
    #         print(str(stare_curenta))
    #
    #         stare_curenta.tabla_joc.deseneaza_grid()
    #         # preiau timpul in milisecunde de dupa mutare
    #         t_dupa = int(round(time.time() * 1000))
    #         print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
    #
    #         if (afis_daca_final(stare_curenta)):
    #             break
    #
    #         # S-a realizat o mutare. Schimb jucatorul cu cel opus
    #         stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()