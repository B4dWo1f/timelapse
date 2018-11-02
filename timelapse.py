#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from tqdm import tqdm
from time import sleep, time
import os
here = os.path.dirname(os.path.realpath(__file__))


import re
def clean(string):
   """ Returns the time in seconds by parsing the string """
   units = {'s':1, 'm':60, 'h':60*60, 'd':24*60*60, 'M':30*24*60*60}
   string = string.replace(' ','')
   p = re.compile('(\d+)\s*(\w+)')
   num, unit = p.match(string).groups()
   num = float(num)
   return num * units[unit]


from configparser import ConfigParser, ExtendedInterpolation
from os.path import expanduser

def get_parameters(ini):
   config = ConfigParser(inline_comment_prefixes='#')
   config._interpolation = ExtendedInterpolation()
   config.read(ini)
   
   pheno = config['capture']['phenomenon']
   duration = config['capture']['duration']
   fps = int(config['capture']['fps'])
   f_tmp = config['capture']['f_tmp']
   v_name = config['capture']['video']
   import pictures as pic
   try:
      url = config['capture']['from_url']
      method = pic.from_url
      inp = url
   except KeyError:
      dev = config['capture']['webcam']
      method = pic.webcam
      inp = dev
   except:
      ## TODO add usage
      print('no method')

   pheno = clean(pheno)
   duration = clean(duration)
   return pheno, duration, fps, method, inp, f_tmp, v_name


import sys
try: ini = sys.argv[1]
except IndexError:
   print('Input file not specified')
   exit()

#ini = 'galayos.ini'
#ini = 'webcam.ini'
pheno, duration, fps, method, inp, f_tmp, video_name = get_parameters(ini)

Nframes = int(duration * fps)
tsleep = pheno/Nframes
print('Taking %s pictures from %s'%(Nframes,inp))
print('waiting %ss between them'%(tsleep))


for i in tqdm(range(Nframes), unit='Frames'):
   fname = here+'/frame_%s.jpg'%(i)
   method(fname,inp)
   with open(f_tmp,'a') as f:
      f.write(fname+'\n')
   f.close()
   twait = 0
   t0 = time()
   exit = False
   while twait < tsleep:
      if os.path.isfile('STOP'):
         exit = True
         break
      twait = time()-t0
   if exit: break

com = 'mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4 -o %s '%(video_name)
com += '-mf type=jpeg:fps=%s mf://@%s'%(fps,f_tmp)
print('Converting to video')
print(com)
os.system(com)
