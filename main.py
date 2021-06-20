import random
import pygame
import pygame.freetype
import click
from click import INT

pygame.init()

# Definiowanie kolorów do pozniejszego wykorzystania
czarny = (0, 0, 0)
bialy = (255, 255, 255)
szary = (200, 200, 200)
turkusowy = (0, 231, 205)
losowy_kolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Stworzenie klasy obiektu (pojedynczy "pixel", wykorzystywany pozniej do tworzenia weza, cukierkow oraz kamieni
class Kwadrat:

    def __init__(self, start, kolor=losowy_kolor):
        self.kolor = kolor
        self.pos = start
        self.os_x = 1
        self.os_y = 0

    def ruch(self, os_x, os_y):
        self.os_x = os_x
        self.os_y = os_y
        self.pos = (self.pos[0] + self.os_x, self.pos[1] + self.os_y)

    # funkcja odpowiadajaca za wizualizacje weza
    liczba_boxow_w_rzedzie = 22
    wymiary_planszy_xy = 500

    def rysuj(self, powierzchnia):
        dis = self.wymiary_planszy_xy // self.liczba_boxow_w_rzedzie
        i = self.pos[0]
        j = self.pos[1]
        pygame.draw.rect(powierzchnia, self.kolor, (i*dis, j*dis, dis, dis))


class Snake:
    cialo = []
    zmiana_kierunku = {}

    def __init__(self, kolor, pos):
        self.kolor = kolor
        self.glowa = Kwadrat(pos)
        self.cialo.append(self.glowa)
        self.os_x = 0
        self.os_y = 1

# funkcja sterowania wezem wraz z zabezpieczeniem ruchow przeciwnych, w momenie gdy ostatnim ruchem pyl ruch w prawo, waz nie moze "obrocic sie o 180" stopni w lewo
    def ruch(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            for _ in pygame.key.get_pressed():
                if pygame.key.get_pressed()[pygame.K_UP]:
                    if self.os_x == 0 and self.os_y == -1:
                        pass
                    else :
                        self.os_x = 0
                        self.os_y = -1
                        self.zmiana_kierunku[self.glowa.pos[:]] = [self.os_x, self.os_y]
                elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                    if self.os_x == -1 and self.os_y == 0:
                        pass
                    else:
                        self.os_x = 1
                        self.os_y = 0
                        self.zmiana_kierunku[self.glowa.pos[:]] = [self.os_x, self.os_y]
                elif pygame.key.get_pressed()[pygame.K_DOWN]:
                    if self.os_x == 0 and self.os_y == -1:
                        pass
                    else:
                        self.os_x = 0
                        self.os_y = 1
                        self.zmiana_kierunku[self.glowa.pos[:]] = [self.os_x, self.os_y]
                elif pygame.key.get_pressed()[pygame.K_LEFT]:
                    if self.os_x == 1 and self.os_y == 0:
                        pass
                    else:
                        self.os_x = -1
                        self.os_y = 0
                        self.zmiana_kierunku[self.glowa.pos[:]] = [self.os_x, self.os_y]

        # Fragment dodawnia oraz usuwania boxow weza na ekranie
        for i, c in enumerate(self.cialo):
            p = c.pos[:]
            if p in self.zmiana_kierunku:
                turn = self.zmiana_kierunku[p]
                c.ruch(turn[0], turn[1])
                if i == len(self.cialo) - 1:
                    self.zmiana_kierunku.pop(p)
            else:
                if c.os_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.liczba_boxow_w_rzedzie - 1, c.pos[1])
                elif c.os_x == 1 and c.pos[0] >= c.liczba_boxow_w_rzedzie - 1:
                    c.pos = (0, c.pos[1])
                elif c.os_y == 1 and c.pos[1] >= c.liczba_boxow_w_rzedzie - 1:
                    c.pos = (c.pos[0], 0)
                elif c.os_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.liczba_boxow_w_rzedzie - 1)
                else:
                    c.ruch(c.os_x, c.os_y)

    # Ustalenie pozycji poczatkowej weza
    def poczatek(self, pozycja):
        self.glowa = Kwadrat(pozycja)
        self.cialo = []
        self.cialo.append(self.glowa)
        self.zmiana_kierunku = {}
        self.os_x = 0
        self.os_y = 1

#funkcja dodajaca kwadrat na ogonie weza
    def dodaj_kwadrat(self):
        tail = self.cialo[-1]
        dx, dy = tail.os_x, tail.os_y

        if dx == 1 and dy == 0: self.cialo.append(Kwadrat((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0: self.cialo.append(Kwadrat((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1: self.cialo.append(Kwadrat((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1: self.cialo.append(Kwadrat((tail.pos[0], tail.pos[1] + 1)))

        self.cialo[-1].os_x = dx
        self.cialo[-1].os_y = dy

    def rysuj(self, powierzchnia):
        for i, c in enumerate(self.cialo):
            if i == 0:
                c.rysuj(powierzchnia)
            else:
                c.rysuj(powierzchnia)


# Fragment odpowiadajacy rysowanie ponowne okna gry w przypadku zjedzenia cukierka. nowy cukierek i kamienie (jesli wybrano opcje) musza sie wygenerowac
def rysuj_okno_ponownie(powierzchnia):
    global Snake, cukierek, kamienie
    powierzchnia.fill(bialy)
    Snake.rysuj(powierzchnia)
    cukierek.rysuj(powierzchnia)
    for kamien in kamienie:
        kamien.rysuj(powierzchnia)
    pygame.display.update()

# Fragment odpowiadajacy za losowanie lokalizacji cukierka bedacych pozywieniem dla weza
def losowanie_cukierka(wymiary_planszy_xy, item):
    positions = item.cialo
    x = wymiary_planszy_xy


    while True:
        x = random.randrange(wymiary_planszy_xy)
        y = random.randrange(wymiary_planszy_xy)
        #zabezpieczenie przed wygenerowaniem cukierka "na" wezu
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)

# Fragment odpowiadajacy za losowanie lokalizacji kamieni bedacych przeszkodami dla weza
def losowanie_kamienia(wymiary_planszy_xy, item_k):
    pozycja_kamien = item_k.cialo

    while True:
        x = random.randrange(wymiary_planszy_xy)
        y = random.randrange(wymiary_planszy_xy)
        #zabezpieczenie przed wygenerowaniem kamienia "na" wezu
        if len(list(filter(lambda z: z.pos == (x, y), pozycja_kamien))) > 0:
            continue
        else:
            break

    return (x, y)

# Fragment odpowiadajacy za komunikat pojawiajacy na końcu gry, wskazujacy liczbe zjedzonych cukierkow
def komunikat(wymiary_planszy_xy):
    screen = pygame.display.set_mode((wymiary_planszy_xy, wymiary_planszy_xy))
    GAME_FONT = pygame.freetype.SysFont("monospace", 12)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        screen.fill(szary)
        text_surface, rect = GAME_FONT.render('Koniec gry, osiagnięty wynik to: ' + str(len(Snake.cialo) - 1) + ' cukierki/ow', (0, 0, 0))
        text_surface2, rect = GAME_FONT.render('Uruchom program ponownie by zagrać jeszcze raz', czarny)
        screen.blit(text_surface, (40, 40))
        screen.blit(text_surface2, (40, 80))
        pygame.display.flip()

# Fragment odpowiadajacy za komende zmiany liczby kamieni podczas gry, jest to element eksperymentalny
# Teoretycznie rowniez w tym miejscu, bez komendy, mozna zmienic liczbe generujacych sie kamieni podczas gry
@click.command(
    help="Gra snake"
)
@click.option(
    "--liczba_kamieni_click",
    type=INT,
    default=3,
    help="Liczba kamieni pojawiajacych sie na planszy.",
)


# W funkcji main zdecyduj czy kamienie maja tworzyc sie "co zjedzenie cukierka" czy pozostac przez cala gre w jednym miejscu
# Fodatkowo wybierz szybkosc gry ("tempo_gry") oraz zdefiniuj wielkosc plansy zmienna "wymiary_planszy_xy" tutaj, oraz w klasie "kwadrat"

def main(liczba_kamieni_click, kamienie_dynamiczne=True):
    global Snake, cukierek, kamienie, text_surface, liczba_kamieni
    liczba_kamieni = liczba_kamieni_click
    wymiary_planszy_xy = 500
    liczba_boxow_w_rzedzie = 22
    tempo_gry = 12
    okno = pygame.display.set_mode((wymiary_planszy_xy, wymiary_planszy_xy))
    Snake = Snake(losowy_kolor, (10, 10))
    cukierek = Kwadrat(losowanie_cukierka(liczba_boxow_w_rzedzie, Snake), kolor=turkusowy)
    kamienie = [
        Kwadrat(losowanie_kamienia(liczba_boxow_w_rzedzie, Snake), kolor=czarny)
        for _ in range(liczba_kamieni)
    ]
    gra = True

    zegar = pygame.time.Clock()

    while gra:
        pygame.time.delay(20)
        zegar.tick(tempo_gry)
        Snake.ruch()
        if Snake.cialo[0].pos == cukierek.pos:
            Snake.dodaj_kwadrat()
            cukierek = Kwadrat(losowanie_cukierka(liczba_boxow_w_rzedzie, Snake), kolor=turkusowy)
            if kamienie_dynamiczne==True:
                for kamien in kamienie:
                    kamien.pos = losowanie_kamienia(liczba_boxow_w_rzedzie, Snake)
                else:
                    continue
            print("Twoj aktualny wynik to: " + str(len(Snake.cialo) - 1))

        for x in range(len(Snake.cialo)):
            if Snake.cialo[x].pos in list(map(lambda z: z.pos, Snake.cialo[x + 1:])):
                print("Koniec gry", 'Przegrales/as, zacznij jeszcze raz... osiagnięty wynik to: ' + str(len(Snake.cialo) - 1) + ' cukierki/ow')


                Snake.poczatek((10, 10))
                okno.blit(komunikat(wymiary_planszy_xy), (40, 40))

            elif Snake.cialo[x].pos in (k.pos for k in kamienie):
                print("Koniec gry", 'Wpadles w kamien i przegrales/as, zacznij jeszcze raz... osiagnięty wynik to: ' + str(len(Snake.cialo) - 1) + ' cukierki/ow')


                Snake.poczatek((10, 10))
                okno.blit(komunikat(wymiary_planszy_xy), (40, 40))

                break

        rysuj_okno_ponownie(okno)


if __name__ == '__main__':
    main()


