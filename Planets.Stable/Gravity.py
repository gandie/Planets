#!/usr/bin/env python
# -*- coding: utf-8 -*-

LEFT=1 # left mouse button
MIDDLE=2
RIGHT=3 # ...
WHEELUP=4
WHEELDOWN=5
FPS=120

CENTER_X=750
CENTER_Y=450

SUN={"diameter" : 100,
     "colour" : (100,100,0),
     "pos" : (CENTER_X,CENTER_Y),
     "mass" : 5000,
     "vel_x" : 0,
     "vel_y" : 0,
     "fixed" : True,
     "centrum" : True} # NEVER INSERT TWO BODIES WITH THIS
                       # CAREFUL! UNIVERSE MAY EXPLODE!
                       # LEAVE SUCH BUSINESS TO PLANETHANDLER

EARTH={"diameter" : 30,
       "colour" : (0,0,255),
       "pos" : (300,500),
       "mass" : 1,
       "vel_x" : 0,
       "vel_y" : 21,
       "fixed" : False,
       "centrum" : False}

from itertools import cycle
from lib.planet import *
from lib.tools import *  # tools module by jannik
from math import *

# Pygame-Modul importieren.
import pygame

# Überprüfen, ob die optionalen Text- und Sound-Module geladen werden konnten.
if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')

def main():


    # Initialisieren aller Pygame-Module und    
    # Fenster erstellen (wir bekommen eine Surface, die den Bildschirm repräsentiert).
    pygame.init()

    screen = pygame.display.set_mode((1600, 1000))

    pygame.display.set_caption("3-Körper-Problem")
    pygame.mouse.set_visible(1)

    SCALE=1
    cor_x = 0
    cor_y = 0
    click_vel_y = 25
    click_mass = 1
    clickCount = 2

    # initialize the mighty PlanetHandler
    Planets = PlanetHandler()

    # Add some default bodies
    Planets.append_defbody(SUN)
    Planets.append_defbody(EARTH)

    # wrap this into label class
    pygame.font.init()
    font = pygame.font.Font(None,25)
    font_surface = font.render("",True,(255,255,255))

    # frame limiter
    clock = pygame.time.Clock()

    # start main loop
    running = True
    while running:

        # limit frames
        clock.tick(FPS)

        # aprox center of picture
        CENTER_X=750*SCALE
        CENTER_Y=450*SCALE

        background = pygame.Surface((1600*SCALE,1000*SCALE))
        background.fill((0,0,0))
        background = background.convert()
 
        # temporary surface to draw things to
        display = pygame.Surface((1600*SCALE,1000*SCALE))
        display.fill((0,0,0))
        display = display.convert()

        # this should be wrapped into the label-class too
        font_surface = font.render("{0} {1} {2} {3} {4}".format(len(Planets.get_planets()),
                                                        clickCount,
                                                        ratio(Planets.get_planets(),
                                                              clickCount),
                                                                click_vel_y,
                                                                click_mass),
                                   True,(255,255,255))

        
        display.blit(background, (0,0))

        # let the PlanetHandler do the magic
        Planets.merge_planets()
        Planets.calc_gravity() # put multithreading here
        Planets.calc_positions()
        display = Planets.draw_planets(display)

        # scale display for zooming
        display = pygame.transform.rotozoom(display, 0, 1.0/SCALE)
        display = display.convert()

        # spit scaled picture to screen
        screen.blit(display, (0,0))
        screen.blit(font_surface,(200,200))        

        # look for events
        for event in pygame.event.get():

            # quit game
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:

                x = event.pos[0] * SCALE
                y = event.pos[1] * SCALE

                clickpos = (x,y)
                Clickbody={"diameter" : 20,
                           "colour" : (0,50,50),
                           "pos" : clickpos,
                           "mass" : click_mass,
                           "vel_x" : 0,
                           "vel_y" : click_vel_y,
                           "fixed" : False,
                           "centrum" : False}

                Planets.append_defbody(Clickbody)
                clickCount += 1
                print "You pressed the left mouse button at (%d, %d)" % event.pos            

            # switch focus between objects
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                # two zoom levels for start
                # more zoom is more complicated to realize in one button
                if SCALE == 1:
                    SCALE = 2
                    Planets.move_all(1600/SCALE,800/SCALE)
                elif SCALE == 2:
                    Planets.move_all(-1600/SCALE,-800/SCALE)
                    SCALE = 1
                print "You pressed the left mouse button at (%d, %d)" % event.pos            

            # dunno
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == MIDDLE:
                print "Middle (%d, %d)" % event.pos            

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == WHEELUP:
                click_vel_y -= 1
                print "4 (%d, %d)" % event.pos            

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == WHEELDOWN:
                click_vel_y += 1
                print "5 (%d, %d)" % event.pos            

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_LEFT:
                    Planets.set_nextCentrum(CENTER_X,CENTER_Y)
                    print 'Links wurde gedrückt'

                if event.key == pygame.K_UP:
                    click_mass += 1
                    print 'Links wurde gedrückt'

                if event.key == pygame.K_DOWN:
                    if click_mass > 1:
                        click_mass -= 1
                    print 'Links wurde gedrückt'



        pygame.display.flip()

if __name__ == '__main__':
    # run main programm
    main()
