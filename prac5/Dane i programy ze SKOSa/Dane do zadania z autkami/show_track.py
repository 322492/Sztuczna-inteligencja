from char_model3 import State
from collections import defaultdict as dd
from math import pi
from turtle import *
import sys

#####################################################
# turtle graphic
#####################################################
tracer(0,1)

BOK = 10
SX = -400
SY = 0
M = 8


def kwadrat(x, y, kolor):
  fillcolor(kolor)
  pu()
  goto(SX + x * BOK, SY + y * BOK)
  pd()
  begin_fill()
  for i in range(4):
    fd(BOK)
    rt(90)
  end_fill() 

def kolko(x, y, kolor):
  fillcolor(kolor)

  pu()
  goto(SX + x * BOK + BOK/2, SY + y * BOK - BOK)
  pd()
  begin_fill()
  circle(BOK/2)
  end_fill() 


#####################################################

B = []
#task_file = sys.argv[1]

task_file = 'task2.txt'

for x in open(task_file):
    L = list(x.strip())
    B.append(L)

for y in range(len(B)):
    for x in range(len(B[y])):
        f = B[y][x]

        if f == 's':
           start = (x,y)

def show_track(B):
    for y in range(len(B)):
        for x in range(len(B[y])):
            if B[y][x] == '#':
                kwadrat(x,y,'gray')
            elif B[y][x] == 'e':
                kwadrat(x,y,'orange')
            elif B[y][x] == 's':
                kwadrat(x,y,'yellow')    
            else:
                kwadrat(x,y,'green')
                
def show_path(p, start_d):
    tracer(1,1)
    sx,sy = start
    pu()
    goto(SX+BOK*sx, SY+BOK*sy)
    pd()
    D = BOK / 2
    s = State(sx,sy)
    s.d = start_d
    for a in p.split('.'):
        s.update(a)
        x = int(s.x)
        y = int(s.y)
        goto(SX+BOK*s.x+D, SY+BOK*s.y - D)
        if B[y][x] == '.':
            print ('YOU ARE OFF ROAD!')
            break
    
    
    if B[y][x] == 'e':
        print ('CONGRATULATION!')
        print ('LENGTH=', len(p.split('.'))) 
    elif B[y][x] == '#':
        print ("YOU HAVEN'T FINISHED!")
    
           
    
                    
#####################################################

ht()
show_track(B)
show_path(10 * 'r.' + 50 * 'a.' + 12 * '.' + 10 * 'al.' + 50 * 'l.' + 10 * 'a.' + 40 * 'lb.' + 30 * 'a.' + 20 *'la.' + 12 * 'a.' + 14 * 'l.' + 150 * 'lb.' + 80 * 'la.' + 5 * '.' + 60 * 'r.' + 150 * 'rb.' + 60 * 'a.' + 25 * 'r.' + 95 * 'rb.' + 60 * 'a.' + 35 * '.' + 10 * 'lb.' + 120 * 'l.' + 30 * 'al.' + 65 * 'a.' + 20 * 'l.' + 160 * 'lb.' + 40 * 'a.' + 6 * 'ar.' + 80 * 'r.' + 100 * 'rb.' + 35 * 'a.' + 75 * 'ar.' + 10 * '.' + 20 * 'l.' + 28 * 'r.', 8)
input()

#show_path(open('path.txt').read(),8)



