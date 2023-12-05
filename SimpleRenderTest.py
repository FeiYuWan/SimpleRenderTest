import pygame
import sys
import math
import matplotlib.pyplot as plt
from pygame.locals import *
width=1024
height=768

class camera:
    def __init__(self):
        self.x=0
        self.y=0
        self.z=0
        self.a=math.pi/2
        self.b=math.pi/2
        self.l=int(width/4)
        self.w=width
        self.h=height
class point:
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
def insertpoint(pointlist,n,point1,point2):
    p1=point1
    p2=point2
    x0=p1.x
    y0=p1.y
    z0=p1.z
    dx=(p2.x-p1.x)/(n+1)
    dy=(p2.y-p1.y)/(n+1)
    dz=(p2.z-p1.z)/(n+1)
    for i in range(1,n+1):
        pointlist.append(point(x0+i*dx,y0+i*dy,z0+i*dz))


def trans(camera,point):
    dx=point.x-camera.x
    dy=point.y-camera.y
    dz=point.z-camera.z
    l=(dx**2+dy**2+dz**2)**0.5
    X=math.cos(camera.b)*dx+math.sin(camera.b)*dy
    Y=-math.sin(camera.b)*dx+math.cos(camera.b)*dy
    Z=dz
    X2=math.cos(camera.a)*X-math.sin(camera.a)*Z
    Y2=Y
    Z2=math.sin(camera.a)*X+math.cos(camera.a)*Z
    if Z2>0:
        if X2>=0:
            y=-abs((camera.l/Z2)*X2)
        else:
            y=abs((camera.l/Z2)*X2)
        if Y2>=0:
            x=-abs((camera.l/Z2)*Y2)
        else:
            x=abs((camera.l/Z2)*Y2)
        P=[x,y]
        return P
    else:
        return 0






pygame.init()  # 初始化pygame
size = width, height  # 设置窗口大小
Screen = pygame.display.set_mode(size)  # 显示窗口
fps = 1000
fcclock = pygame.time.Clock()

Camera=camera()
pointlist=[point(1,2,0),point(0,2,0),point(0,3,0),point(1,3,0),point(1,2,1),point(0,2,1),point(0,3,1),point(1,3,1)]
Ninsert=10
Npoint=len(pointlist)
for i in range(Npoint):
    for j in range(i+1,Npoint):
        insertpoint(pointlist,Ninsert,pointlist[i],pointlist[j])

screen=[]
exit=False
tt=1
w_down=0
while (not exit):  # 死循环确保窗口一直显示
    tt+=1
    tt=tt%2
    screen=[]
    Screen.fill((255,255,255))

    for i in range(len(pointlist)):
        T=trans(Camera,pointlist[i])
        if T != 0:
            screen.append(T)
    for j in range(len(screen)):
        pygame.draw.circle(Screen,[0,0,0],[int(screen[j][0]+width*0.5),int(-screen[j][1]+height*0.5)],1,1)




    for event in pygame.event.get():  # 遍历所有事件
        if event.type==KEYDOWN and event.key==K_ESCAPE:#按下
            exit = True
        if pygame.key.get_pressed()[pygame.K_w]:
            Camera.x+=0.01*math.cos(Camera.b)
            Camera.y+=0.01*math.sin(Camera.b)
            Camera.z+=0.01*math.cos(Camera.a)
        if pygame.key.get_pressed()[pygame.K_s]:
            Camera.x-=0.01*math.cos(Camera.b)
            Camera.y-=0.01*math.sin(Camera.b)
            Camera.z-=0.01*math.cos(Camera.a)
        if pygame.key.get_pressed()[pygame.K_a]:
            Camera.x-=0.01*math.sin(Camera.b)
            Camera.y+=0.01*math.cos(Camera.b)
        if pygame.key.get_pressed()[pygame.K_d]:
            Camera.x+=0.01*math.sin(Camera.b)
            Camera.y-=0.01*math.cos(Camera.b)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            Camera.z+=0.01
        if pygame.key.get_pressed()[pygame.K_LSHIFT]:
            Camera.z-=0.01


        if event.type == pygame.MOUSEMOTION:
             mouse_move = event.rel
    xx,yy = pygame.mouse.get_pos()
    if (xx,yy) != (width*0.5,height*0.5):
        #print(xx,yy)
        print(Camera.a,Camera.b)
        Camera.a+=0.005*(yy-height*0.5)
        Camera.b-=0.005*(xx-width*0.5)
    pygame.mouse.set_pos([width*0.5,height*0.5])
    if Camera.a>math.pi:
        Camera.a=0.98*math.pi
    if Camera.a<0:
        Camera.a=0.01
    #Camera.b=Camera.b%(2*math.pi)
    fcclock.tick(fps)
    pygame.display.update()

pygame.quit()  # 退出pygame
