#!/usr/bin/env python   
#-*- coding: utf-8 -*-

'''
    Use: Simulator for Suzaku Quadrotor
    Module: Simulator Camera
    Author: Legend Lee 
    Date: 2013-04-16
    E-mail: legendlee1314@gmail.com
'''

# try to import

try:
    import pygame, math, ode
    from OpenGL.GL import *
    from OpenGL.GLU import *
except:
    print '=====> import error! please check'

class Camera(object):
    def __init__(self, eye, target, up, rotation, world, space, perspective):
        self.eye = eye
        self.target = target
        self.up = up
        self.world = world
        self.space = space
        self.body = ode.Body(self.world)
        self.body.setGravityMode(True)
        self.body.setPosition(eye)
        self.mass = ode.Mass()
        self.mass.setSphere(1000, 1)
        self.geom = ode.GeomSphere(self.space, .75)
        self.geom.setBody(self.body)
        self.rotation = rotation
        self.perspective = perspective
        self.__last_position = self.body.getPosition()
        print '=====> camera loaded successfully!'

    def move(self, m_x, m_y, m_z):
        z = m_z*math.cos(math.radians(self.rotation[0]))
        x = -m_z*math.sin(math.radians(self.rotation[0]))
        z += m_x*math.sin(math.radians(self.rotation[0]))
        x += m_x*math.cos(math.radians(self.rotation[0]))
        y = m_y
        self.body.addForce((x,y,z))

    def rotate(self, x, y):
        self.rotation[0] -= x
        self.rotation[1] -= y

    def collide(self, args, geom1, geom2):
        contacts = ode.collide(geom1, geom2)
        world,contact_group = args
        for c in contacts:
            c.setBounce(0.0)
            c.setMu(5000)
            j = ode.ContactJoint(world, contact_group, c)
            j.attach(geom1.getBody(), geom2.getBody())

    def is_dirty(self):
        return self.body.getPosition() == self.__last_position

    def get_position(self):
        return self.body.getPosition()

    def __camera_info(self):
        position = self.get_position()
        return [position[0],position[1],position[2],position[0],position[1],position[2]-.1]+self.up

    def dampen(self):
        vel = self.body.getAngularVel()
        nvel = [x*.99 for x in vel]
        self.body.setAngularVel(nvel)

    def update(self):
        if self.rotation[0] > 360: self.rotation[0] -= 360
        if self.rotation[0] < 0: self.rotation[0] += 360
        if self.rotation[1] > 90: self.rotation[1] = 90
        if self.rotation[1] < -90: self.rotation[1] = -90
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(*self.perspective)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotated(self.rotation[0],0,1,0)
        glRotated(self.rotation[1],math.cos(math.radians(self.rotation[0])),0,
                  math.sin(math.radians(self.rotation[0])))
        gluLookAt(*self.__camera_info())
        self.dampen()
        self.last_position = self.body.getPosition()
