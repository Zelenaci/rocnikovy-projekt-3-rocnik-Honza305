import pyglet as pg
from pyglet import gl
from pyglet.window.key import DOWN, UP, W, S
import random

Sirka = 900
Vyska = 700

Vmice = 20 	#velikost míče
Spalky = 10 	#šířka palek
Dpalky = 100 	#délka pálky
Rychlost = 200 
Rpalky = Rychlost * 1.5 	# Rychlost pálky

DPC = 20 	#délka půlící čáry
Vfontu = 40 	#velikost fontu
Otextu = 30 	#odsazení textu

Ppalek = [Vyska // 2, Vyska // 2]  # vertikalni pozice palek
Pmice = [0, 0]  	# souradnice micku 
Rmice = [0, 0]   	#ryhlost mice
Sklavesy = set()  	# sada stisknutych klaves
Skore = [0, -1]  	# skore

#Vykreslení Hrací Plochy

def nakresli_obdelnik(x1, y1, x2, y2):
    gl.glBegin(gl.GL_TRIANGLE_FAN)   # zacni kreslit spojene trojuhelniky
    gl.glVertex2f(int(x1), int(y1))  # vrchol A
    gl.glVertex2f(int(x1), int(y2))  # vrchol B
    gl.glVertex2f(int(x2), int(y2))  # vrchol C, nakresli trojuhelnik ABC
    gl.glVertex2f(int(x2), int(y1))  # vrchol D, nakresli trojuhelnik BCD
    gl.glEnd()  # ukonci kresleni trojuhelniku

#Plocha
def vykresli():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)  # smaz obsah okna
    gl.glColor3f(255, 0, 0)  # nastav barvu kresleni - červenou

#Vykreslení Míčku
    
    nakresli_obdelnik(
            Pmice[0] - Vmice // 2,
            Pmice[1] - Vmice // 2,
            Pmice[0] + Vmice // 2,
            Pmice[1] + Vmice // 2,)
      
#Vykreslení Pálek
    
    for x, y in [(0, Ppalek[0]), (Sirka, Ppalek[1])]:
        nakresli_obdelnik(
                x - Spalky,
                y - Dpalky // 2,
                x + Spalky,
                y + Dpalky // 2,)
        
#Vykreslení Pulici Čáry
    
    for y in range(DPC // 2, Vyska, DPC * 2):
        nakresli_obdelnik(
                Sirka // 2 - 1,
                y,
                Sirka // 2 + 1,
                y + DPC)

#Nakreslení Skóre

    nakresli_text(
        str(Skore[0]),
        x=Otextu,
        y=Vyska - Otextu - Vfontu,
        pozice_x='left')

    nakresli_text(
        str(Skore[1]),
        x=Sirka - Otextu,
        y=Vyska - Otextu - Vfontu,
        pozice_x='right')

#Vykreslení Skóre
        
def nakresli_text(text, x, y, pozice_x):
    napis = pg.text.Label(
            text,
            font_size= Vfontu,
            x=x, y=y, anchor_x= pozice_x)
    napis.draw()
    

#Klavesy
    
def stisk_klavesy(symbol, modifikatory):
    if symbol == W:
        Sklavesy.add(('nahoru', 0))
    if symbol == S:
        Sklavesy.add(('dolu', 0))
    if symbol == UP:
        Sklavesy.add(('nahoru', 1))
    if symbol == DOWN:
        Sklavesy.add(('dolu', 1))

def pusteni_klavesy(symbol, modifikatory):
    if symbol == W:
        Sklavesy.discard(('nahoru', 0))
    if symbol == S:
        Sklavesy.discard(('dolu', 0))
    if symbol == UP:
        Sklavesy.discard(('nahoru', 1))
    if symbol == DOWN:
        Sklavesy.discard(('dolu', 1))

#RMNZ

def reset():
    Pmice[0] = Sirka // 2
    Pmice[1] = Vyska // 2

    if random.randint(0, 1):
        Rmice[0] = Rychlost
    else:
        Rmice[0] = -Rychlost

    Rmice[1] = random.uniform(-1, 1) * Rychlost
        
def obnov_stav(dt):

#Pohyb pálek

    for Cislo_palky in (0, 1):
        if ('nahoru', Cislo_palky) in Sklavesy:    # pohyb podle klaves (viz funkce `stisk_klavesy`)
            Ppalek[Cislo_palky] += Rpalky * dt
        if ('dolu', Cislo_palky) in Sklavesy:
            Ppalek[Cislo_palky] -= Rpalky * dt
	
        if Ppalek[Cislo_palky] < Dpalky / 2:    # dolni zarazka - kdyz je palka prilis dole, nastavime ji na minimum
            Ppalek[Cislo_palky] = Dpalky / 2
        if Ppalek[Cislo_palky] > Vyska - Dpalky / 2:	    # horni zarazka - kdyz je palka prilis nahore, nastavime ji na maximum
            Ppalek[Cislo_palky] = Vyska - Dpalky / 2

# Pohyb/Odraz Míčku
    Pmice[0] += Rmice[0] * dt
    Pmice[1] += Rmice[1] * dt

#Odrážení míčů

# Odraz míčku od stěn
    if Pmice[1] < Vmice // 2:
        Rmice[1] = abs(Rmice[1])
    if Pmice[1] > Vyska - Vmice // 2:
        Rmice[1] = -abs(Rmice[1])

    palka_min = Pmice[1] - Vmice / 2 - Dpalky / 2
    palka_max = Pmice[1] + Vmice / 2 + Dpalky / 2

    # odrazeni vlevo
    if Pmice[0] < Spalky + Vmice / 2:			# palka je na spravnem miste, odrazime micek
        if palka_min < Ppalek[0] < palka_max:		
            Rmice[0] = abs(Rmice[0])
        else:						# palka je jinde nez ma byt, hrac prohral
            Skore[1] += 1
            reset()

    # odrazeni vpravo
    if Pmice[0] > Sirka - (Spalky + Vmice / 2):
        if palka_min < Ppalek[1] < palka_max:
            Rmice[0] = -abs(Rmice[0])
        else:
            Skore[0] += 1
            reset()
pg.clock.schedule(obnov_stav)
window = pg.window.Window(width=Sirka, height=Vyska)
window.push_handlers(
    on_draw=vykresli,  # na vykresleni okna pouzij funkci `vykresli`
    on_key_press=stisk_klavesy,
    on_key_release=pusteni_klavesy)

pg.app.run()
