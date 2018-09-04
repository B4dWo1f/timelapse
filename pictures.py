#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib.request import urlretrieve
import os

def from_url(name,url, L=20):
   """
     Download picture from a remote url
   """
   b,cont = False,0
   while not b and cont < L:
      a,b = urlretrieve(url, name)
      cont += 1

def webcam(name,dev='/dev/video1',res='1920x1080'):
   """
     Take a picture from video device
     dev: device to take picture from
     name: name of the picture
     res: resolution
   """
   #com = 'avconv -f video4linux2 -loglevel quiet -s %s -i %s '%(res,dev)
   #com += '-ss 0:0:2 -frames 1 %s'%(name)
   com = 'ffmpeg -loglevel quiet -y -f video4linux2 -s %s -i %s'%(res,dev)
   com += ' -ss 0:0:2 -frames 1 %s'%(name)
   os.system(com)


def make_timelapse(name,fps,f_tmp):
   """
     name: of the output video
     fps: frames per second
     f_tmp: file containing all the pictures names (in order)
   """
   com = 'mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o %s '%(name)
   com += '-mf type=jpeg:fps=%s mf://@%s'%(fps,f_tmp)
   os.system(com)
