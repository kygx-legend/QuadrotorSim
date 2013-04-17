#!/usr/bin/env python   
#-*- coding: utf-8 -*-

'''
    Use: Simulator for Suzaku Quadrotor
    Module: Simulator Object
    Author: Legend Lee 
    Date: 2013-04-16
    E-mail: legendlee1314@gmail.com
'''

# try to import

try:
    import pygame, ode
    from OpenGL.GL import *
    from objloader import *
except:
    print '=====> import error! please check'

class OBJ(object):
    """
        obj module to construct one object in a world
    """
    def __init__(self, path, filename, world, space):
        self.world = world
        self.space = space
        self.display_list = OBJloader(path, filename, swapyz=False).getGLlists()
        print '=====> %s loaded successfully!' % filename

    def callList(self):
        glCallList(self.display_list)

if __name__ == '__main__':   
    objtest = OBJ('./model/','suzaku.obj',None,None)

