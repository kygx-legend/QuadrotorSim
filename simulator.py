#!/usr/bin/env python   
#-*- coding: utf-8 -*-

'''
    Use: Simulator for Suzaku Quadrotor
    Module: Simulator Application
    Author: Legend Lee 
    Date: 2013-04-16
    E-mail: legendlee1314@gmail.com
'''

import os, sys

# try to import
try:
    from pygame.locals import *
    from pygame.constants import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from objloader import *
except:
    print '=====> import error! please check'

FPS = 30

# Simulator App 

class SimulatorApp(object):

    # Init Application

    def __init__(self):	
        print '=====> Simulator App start...'
        self._running = True
        self._display_surf = None
        self.viewpoint = (800, 600)
        self.hx, self.hy = self.viewpoint[0] / 2, self.viewpoint[1] / 2

        self.path, self.filename = './model/', 'suzaku.obj'

        self.clock = pygame.time.Clock()
        self.rx, self.ry = (0,0)
        self.tx, self.ty = (0,0)
        self.zpos = 5
        self.rotate = self.move = False

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.viewpoint, OPENGL | DOUBLEBUF)
        self._running = True

        glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

        self.obj = OBJ(self.path, self.filename, swapyz=True)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        width, height = self.viewpoint
        gluPerspective(90.0, width/float(height), 1, 100.0)
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_MODELVIEW)

    def on_event(self, e):
        if e.type == pygame.QUIT:
            self._running = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: self.zpos = max(1, self.zpos-1)
            elif e.button == 5: self.zpos += 1
            elif e.button == 1: self.rotate = True
            elif e.button == 3: self.move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: self.rotate = False
            elif e.button == 3: self.move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if self.rotate:
                self.rx += i
                self.ry += j
            if self.move:
                self.tx += i
                self.ty -= j

    def on_loop(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

    def on_render(self):
        glTranslate(self.tx/20., self.ty/20., - self.zpos)
        glRotate(self.ry, 1, 0, 0)
        glRotate(self.rx, 0, 1, 0)
        glCallList(self.obj.gl_list)
     
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            self.clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
                self.on_loop()
                self.on_render()


#----mainloop----
if __name__ == '__main__':   

    theApp = SimulatorApp()
    theApp.on_execute()
