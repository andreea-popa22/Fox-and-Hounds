import time

import pygame, sys

ADANCIME_MAX = 6


def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL else False
    return False


class Joc:
    celuleGrid = None
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    DENIED = '~'
    GOL = '#'

    @classmethod
    def initializeaza(cls, display, NR_COLOANE = 8, dim_celula = 100):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.hounds_img = pygame.image.load('black.png')
        cls.hounds_img = pygame.transform.scale(cls.hounds_img, (dim_celula, dim_celula))
        cls.fox_img = pygame.image.load('red.png')
        cls.fox_img = pygame.transform.scale(cls.fox_img, (dim_celula, dim_celula))
        cls.celuleGrid = []
        for linie in range(NR_COLOANE):
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid.append(patr)

    def deseneaza_grid(self):
        for ind in range(self.__class__.NR_COLOANE**2):
            linie = ind // self.__class__.NR_COLOANE
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
        pygame.display.update()
        pygame.display.flip()


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

    def get_hounds_pos(self):
        pos = []
        for i in range(8):
            for j in range(8):
                if self.matr[i][j] == 'h':
                    pos.append([i,j])
        return pos

    def final(self):
        for i in range(8):
            for j in range(8):
                if self.matr[i][j] == 'f':
                    # verific daca vulpea este capturata
                    p1 = p2 = p3 = p4 = False
                    if i - 1 >= 0:
                        if j - 1 >= 0:
                            if self.matr[i-1][j-1] == 'h':
                                p1 = True
                        else:
                            p1 = True #vulpea e blocata in nord vest de marginea tablei
                        if j + 1 <= 7:
                            if self.matr[i-1][j+1] == 'h':
                                p1 = True
                        else:
                            p3 = True #vulpea e blocata in nord est de marginea tablei
                    else:
                        p1 = p3 = True
                    if i + 1 <= 7:
                        if j - 1 >= 0:
                            if self.matr[i+1][j-1] == 'h':
                                p2 = True
                        else:
                            p2 = True #vulpea e blocata in sud vest de marginea tablei
                        if j + 1 <= 7:
                            if self.matr[i+1][j+1] == 'h':
                                p1 = True
                        else:
                            p4 = True #vulpea e blocata in sud est de marginea tablei
                    else:
                        p2 = p4 = True
                    if p1 == True and p2 == True and p3 == True and p4 == True:
                        return "hounds"

                    #verific daca vulpea a depasit toti cainii
                    positions = self.get_hounds_pos()
                    h1 = True if i <= positions[0][0] else False
                    h2 = True if i <= positions[1][0] else False
                    h3 = True if i <= positions[2][0] else False
                    h4 = True if i <= positions[3][0] else False
                    if h1 == True and h2 == True and h3 == True and h4 == True:
                        return "fox"
        return "no"

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(8):
            for j in range(8):
                if self.matr[i][j] == 'f':
                    if jucator_opus == 'f': #daca trebuie sa mute vulpea
                        matr_tabla_noua = self.matr.copy()
                        matr_tabla_noua[i][j] = self.__class__.GOL #sterg pozitia curenta
                        if i-1 >= 0:
                            if j-1 >= 0: #nord vest
                                matr_tabla_noua[i-1][j-1] = 'f'
                                l_mutari.append(matr_tabla_noua)
                                matr_tabla_noua[i-1][j-1] = '#'
                            if j+1 <= 7: #nord est
                                matr_tabla_noua[i-1][j+1] = 'f'
                                l_mutari.append(matr_tabla_noua)
                                matr_tabla_noua[i-1][j+1] = '#'
                        if i+1 <= 7:
                            if j - 1 >= 0: #sud vest
                                matr_tabla_noua[i+1][j-1] = 'f'
                                l_mutari.append(matr_tabla_noua)
                                matr_tabla_noua[i+1][j-1] = '#'
                            if j + 1 <= 7: #sud est
                                matr_tabla_noua[i+1][j+1] = 'f'
                                l_mutari.append(matr_tabla_noua)
                                matr_tabla_noua[i+1][j+1] = '#'
                        break
                if self.matr[i][j] == 'h':
                    if jucator_opus == 'h': #daca trebuie sa mute cainii
                        matr_tabla_noua = self.matr.copy()
                        matr_tabla_noua[i][j] = self.__class__.GOL  # sterg pozitia curenta
                        if i + 1 >= 7:
                            if j - 1 >= 0:  # sud vest
                                matr_tabla_noua[i][j] = 'h'
                                l_mutari.append(matr_tabla_noua)
                                matr_tabla_noua[i][j] = '#'
                            if j + 1 <= 7:  # sud est
                                matr_tabla_noua[i][j] = 'h'
                                l_mutari.append(matr_tabla_noua)
                                matr_tabla_noua[i][j] = '#'
        return l_mutari

    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
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
                + self.linie_deschisa(self.matr[0:9:4], jucator)
                + self.linie_deschisa(self.matr[2:8:2], jucator))

    def estimeaza_scor(self, adancime, juc):
        if juc == 'f':
            return self.estimeaza_scor_f(adancime)
        return self.estimeaza_scor_h(adancime)

    def estimeaza_scor_f(self, adancime):
        t_final = self.final()
        if t_final == self.JMAX:
            return 100 + adancime
        elif t_final == self.JMIN:
            return -100 - adancime
        else:
            return 1

    def estimeaza_scor_h(self, adancime):
        t_final = self.final()
        if t_final == self.JMAX:
            return 100 + adancime
        elif t_final == self.JMIN:
            return -100 - adancime
        else:
            return 1

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0:7][0]]) + "\n" +
               " ".join([str(x) for x in self.matr[0:7][1]]) + "\n" +
               " ".join([str(x) for x in self.matr[0:7][2]]) + "\n" +
               " ".join([str(x) for x in self.matr[0:7][3]]) + "\n" +
               " ".join([str(x) for x in self.matr[0:7][4]]) + "\n" +
               " ".join([str(x) for x in self.matr[0:7][5]]) + "\n" +
               " ".join([str(x) for x in self.matr[0:7][6]]) + "\n" +
               " ".join([str(x) for x in self.matr[-1][0:8]]) + "\n")
        return sir


class Stare:
    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent
        self.adancime = adancime
        self.estimare = estimare
        self.mutari_posibile = []
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
    if final == "no":
        return False
    if final == "fox":
        print("A castigat vulpea!")
        return True
    if final == "hounds":
        print("Au castigat cainii!")
        return True


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


def deseneaza_alegeri(display, tabla_curenta):
    btn_alg = GrupButoane(
        top=200,
        left=250,
        listaButoane=[
            Buton(display=display, w=120, h=50, text="Minimax", valoare="minimax"),
            Buton(display=display, w=120, h=50, text="Alpha-Beta", valoare="alphabeta")
        ],
        indiceSelectat=1)
    btn_juc = GrupButoane(
        top=300,
        left=250,
        listaButoane=[
            Buton(display=display, w=120, h=50, text="Fox", valoare='f'),
            Buton(display=display, w=120, h=50, text="Hounds", valoare='h')
        ],
        indiceSelectat=0)
    btn_nvl = GrupButoane(
        top=400,
        left=200,
        listaButoane=[
            Buton(display=display, w=120, h=50, text="Usor", valoare="usor"),
            Buton(display=display, w=120, h=50, text="Mediu", valoare="mediu"),
            Buton(display=display, w=120, h=50, text="Avansat", valoare="avansat")
        ],
        indiceSelectat=0)
    ok = Buton(display=display, top=500, left=350, w=80, h=50, text="ok", culoareFundal=(155, 0, 55))
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
                                display.fill((0, 0, 0))
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


def validare(l, c, linie, coloana):
    if (l-1 == linie and c-1 == coloana) or (l-1 == linie and c+1 == coloana) or (l+1 == linie and c-1 == coloana) or (l+1 == linie and c+1 == coloana):
        return True
    return False


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

    Joc.JMAX = 'f' if Joc.JMIN == 'h' else 'h'
    print("Tabla initiala")
    print(str(tabla_curenta))
    stare_curenta = Stare(tabla_curenta, 'f', ADANCIME_MAX)
    tabla_curenta.deseneaza_grid()
    pozitie_anterioara = [['f', 7, 0], ['h', 0, 1]]
    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for np in range(len(Joc.celuleGrid)):
                        if Joc.celuleGrid[np].collidepoint(pos):
                            linie = np // 8
                            coloana = np % 8
                            for x in pozitie_anterioara:
                                if x[0] == Joc.JMIN:
                                    l = x[1]
                                    c = x[2]
                                    if validare(l, c, linie, coloana):
                                        stare_curenta.tabla_joc.matr[l][c] = '#'
                                        x[1] = linie
                                        x[2] = coloana
                                        stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                                        stare_curenta.tabla_joc.deseneaza_grid()
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))
                                        stare_curenta.tabla_joc.deseneaza_grid()
                            if (afis_daca_final(stare_curenta)):
                                break
                            #stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

        # else:
        #     t_inainte = int(round(time.time() * 1000))
        #     if tip_algoritm == "minimax":
        #         stare_actualizata = min_max(stare_curenta)
        #     else:
        #         stare_actualizata = alpha_beta(-500, 500, stare_curenta)
        #     stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
        #     print("Tabla dupa mutarea calculatorului")
        #     print(str(stare_curenta))
        #
        #     stare_curenta.tabla_joc.deseneaza_grid()
        #     t_dupa = int(round(time.time() * 1000))
        #     print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")
        #     if (afis_daca_final(stare_curenta)):
        #         break
        #     stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)

if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()