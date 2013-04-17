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
    from obj import *
    from camera import *
except:
    print '=====> import error! please check'

FPS = 30

# Simulator App 

class SimulatorApp(object):

    # Init Application

    def __init__(self):	
        self.size = (640,480)
        self.flags = OPENGL|DOUBLEBUF|HWSURFACE
        self.clear_color = (1.,1.,1.,1.)
        self.stop = False
        self.dirty_camera = False
        self.light_pos = [0,3,0,1]
        self.light_ambient = [0,0,0,1]
        self.light_diffuse = [.5,.5,.5,1]
        self.light_specular = [.5,.5,.5,1]
        self.last_mouse_pos = None
        self.clock = pygame.time.Clock()
        self.world = ode.World()
        self.world.setGravity((0,-9.81,0))
        self.world.setERP(0.8)
        self.world.setCFM(1E-5)
        self.space = ode.Space()
        self.contact_group = ode.JointGroup()
        self.floor = ode.GeomPlane(self.space, (0,1,0), 0)
        self.camera = None
        print '=====> Simulator App start...'

    def start(self):
        self.init()
        self.load_camera()
        self.load_obj()
        self.initGL()
        self.set_light()
        self.run()
        self.finish()

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size,self.flags)

    def load_camera(self):
        self.camera = Camera([0,4,0],[0,4,-.1],[0,1,0],[0,0],self.world,
                             self.space, (90, float(self.size[0])/self.size[1], .1,100))

    def load_obj(self):
        self.obj = OBJ('./model/', 'suzaku.obj', None, None)

    def initGL(self):
        glViewport(0,0,640,480)
        self.move_camera()
        glClearColor(*self.clear_color)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glMaterial(GL_FRONT, GL_AMBIENT, (.1,.1,.1,1))
        glMaterial(GL_FRONT, GL_DIFFUSE, (1,1,1,1))
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_POLYGON_SMOOTH)
        glEnable(GL_BLEND)

    def set_light(self):
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, self.camera.get_position())
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.light_specular)

    def call_lists(self):
        self.obj.callList()

    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                self.end()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.last_mouse_pos = pygame.mouse.get_pos()
                    pygame.mouse.set_visible(False)
            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_mouse_pos = None
                    pygame.mouse.set_visible(True)
            if event.type == MOUSEMOTION:
                if self.last_mouse_pos is not None: self.handle_mouse()

    def move_camera(self):
        self.dirty_camera = False
        self.camera.update()
        glLightfv(GL_LIGHT0, GL_POSITION, self.camera.get_position())

    def move(self, m_x, m_y, m_z):
        self.camera.move(m_x,m_y,m_z)

    def handle_keys(self, keys):
        if keys[K_COMMA] or keys[K_a] or \
                keys[K_o] or keys[K_e] or \
                keys[K_SPACE] or keys[K_LSHIFT]:
            self.dirty_camera = True
        if keys[K_w]:
            self.move(0,0,-10)
        if keys[K_a]:
            self.move(-10,0,0)
        if keys[K_d]:
            self.move(10,0,0)
        if keys[K_s]:
            self.move(0,0,10)
        if keys[K_e]:
            self.move(0,-10,0)
        if keys[K_SPACE]:
            self.move(0,50,0)

    def clear_screen(self):
        glClear(GL_DEPTH_BUFFER_BIT|GL_COLOR_BUFFER_BIT)

    def update_screen(self):
        pygame.display.flip()

    def sync(self):
        glFinish()

    def handle_camera(self):
        self.move_camera()

    def handle_world(self):
        self.space.collide((self.world,self.contact_group), self.camera.collide)
        self.world.step(1/60.)
        self.contact_group.empty()

    def handle_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        diff = [(self.last_mouse_pos[x]-mouse_pos[x])/3. for x in range(2)]
        self.camera.rotate(*diff)
        self.dirty_camera = True
        pygame.mouse.set_pos(self.last_mouse_pos)

    def run(self):
        while not self.stop:
            self.clock.tick()
            self.handle_events(pygame.event.get())
            self.handle_keys(pygame.key.get_pressed())
            self.handle_world()
            self.handle_camera()
            self.clear_screen()
            self.call_lists()
            self.update_screen()
            self.sync()

    def end(self):
        self.stop = True

    def finish(self):
        print self.clock.get_fps()
        pygame.quit()



#----mainloop----
if __name__ == '__main__':   

    theApp = SimulatorApp()
    theApp.start()
