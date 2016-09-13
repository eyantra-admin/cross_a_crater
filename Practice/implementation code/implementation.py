import cv2
import numpy as np
import random
import os
import serial
import math
from time import sleep
import motion
from imglib import *
from motion import *
grid_line_x = 18
grid_line_y = 12
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
stepper=0
MIN = np.array([152, 79, 88]) #pink color mask, for bot localisation
MAX = np.array([178, 227, 255])
B1x=0
B2x=0
B1y=0
B2y=0

##################

#########################################
cap = cv2.VideoCapture(1)
jay=0
while(True):
	jay=jay+1
	ret, img = cap.read()
	if jay==200:
		break
# img=cv2.imread("demo.jpg")
# rotating image
frame=imgclip(img)
rows,cols,l = frame.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
frame = cv2.warpAffine(frame,M,(cols,rows))

h,k,l=frame.shape
m=480/(grid_line_x-1)
n=320/(grid_line_y-1)
print m,n,h,k
#################
def execute(route_length,route_path):
        stepper=0 
        while(1):
                
                ret, frame = cap.read()
                rows,cols,l = frame.shape
                M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
                frame = cv2.warpAffine(frame,M,(cols,rows))
                img=imgclip(frame)
                ############ processing starts after clipping
                #wap=grid_draw(img,17,17)
                #cv2.imshow("show",wap)
                hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                
                bmask = cv2.inRange(hsv, MIN,MAX)
                
                #bret,bthresh = cv2.threshold(bmask,127,255,1)
                #cv2.imshow('binary',mask)
                #cv2.imwrite("wall.jpg",mask)

                bcontours, bh = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:12] ##bot
                #bcontours,length=areacon(bcontours,500,300)
                #bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:length]
               
                
                #cv2.drawContours(res,contours,-1,(0,255,0),2)
                cv2.drawContours(img,bcontours,-1,(255,255,0),2)
                
                if len(bcontours)!=0:   
                	M = cv2.moments(bcontours[0])
	                B1x = int(M['m10']/M['m00'])
	                B1y = int(M['m01']/M['m00'])
	                # print cx3,cy3
	                M = cv2.moments(bcontours[1])
	                B2x = int(M['m10']/M['m00'])
	                B2y = int(M['m01']/M['m00'])	
			cx3=B1x
			cy3=B1y
			cx4=B2x
			cy4=B2y
			cv2.circle(img,(B1x,B1y), 5, (0,0,255), -1)
			cv2.circle(img,(B2x,B2y), 5, (0,100,100), -1)
                #a,b=gridtopixel(x,y,m,n)
                #print route_path[stepper].y+1,route_path[stepper].x+1
                #print y+1,x+1
                #print getcoor(a,b,m,n)
                #cv2.circle(img,(b,a), 5, (211,200,255), -1)
                
                
                # print cx3,cy3
                bx,by=getcoor(cy3,cx3,m,n)
                
                #print route_path[0].y+1,route_path[0].x+1   [(5,6), (4,6), (3,6), (3,5), (3,4), (3,3)]
                #print "starting point",Y,X
                #print "bot center",bx+1,by+1,"route length",route_length
                #print "other bot",cx4,cy4
                if stepper!=int(route_length):
                        ser.write("9")
                        # print stepper
                        X,Y=gridtopixel(route_path[stepper].x ,route_path[stepper].y,m,n)#X,Y are pixels of next grid coor
                        cv2.circle(img,(Y,X), 5, (255,100,100), -1)
                        #print "hello123"
                        m1= getslope(cx3,cy3,Y,X)
                        d1=dis(cx3,cy3,Y,X)#distance between bot's center and next path coordinates
                        #print "distance between bot's center and next path coordinates", d1
                        m2= getslope(cx3,cy3,cx4,cy4)
                        d2=dis(cx4,cy4,Y,X)#distance between bot's other point and next path coordinates
                        #print "distance between bot's other point and next path coordinates", d2
                        mid1=(cx3+cx4)/2#mid point of bot center and other point
                        mid2=(cy3+cy4)/2#mid point of bot center and other point
                        bx,by=getcoor(cy3,cx3,m,n)
                        # print mid1,mid2
                        if orientmove(m1,m2,by+1,bx+1,route_path[stepper].y+1,route_path[stepper].x+1,d1,d2)==1: #bot reaches next coor
                                      stepper=stepper+1
                                      flag=0
                                      #print "Bot Coor",bx+1,by+1
                                      #print stepper
                                      #ser.write("7")
                                      #z,c=gridtopixel(route_path[stepper].x,route_path[stepper].y,m,n)
          
                else:
                        ser.write("5")
                        #ser.write("9")
                        break
                                
                                
                        
                
                
                
                                 
                         
        ##########################
                        
                #cv2.imshow('maskcontour',bmask)
                cv2.imshow('ori',img)
                if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                        break
        ##############
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
dilation, obs=obstacle(hsv)#obstacle dilated
frame=grid_draw(frame,grid_line_x,grid_line_y)
grid_mapp,obb=markobstacle(obs,frame,grid_line_x,grid_line_y)
# print grid_mapp
<<<<<<< HEAD
print getcoor(40,80,n,m)
print gridtopixel(1,2,n,m)
x,y=gridtopixel(1,2, n,m)
print "grid cell to pixels",x,y
cv2.circle(img,(int(y),int(x)),3,(0,255,0),-11)
start=GridPoint(1,2)
stop=GridPoint(10,6)
length,route=solve(start,stop,img)
print length, route
# dilation=obstacle(hsv)#obstacle dilated
# cv2.imshow("obstacles",dilation)
=======
# print "pixel to grid ",getcoor(409,249,m,n)
# print "grid to pixel",gridtopixel(14,8,m,n)
# x,y=gridtopixel(1,2, m,n)
# print "grid cell to pixels",x,y
# cv2.circle(frame,(int(x),int(ys)),3,(0,255,0),-11)
##################3
# start=GridPoint(12,6)#base point
# stop=GridPoint(13,2)#A point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ######################
# stop=GridPoint(10,2)#dispatch point
# start=GridPoint(13,2)#A point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ###############
# start=GridPoint(10,2)#Dispatch point
# stop=GridPoint(3,2)#destiation hole
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
#########################
# start=GridPoint(3,2)#return
# stop=GridPoint(10,2)
# length,route=solve(start,stop,frame)
# execute(length,route)
# #############
# start=GridPoint(10,2)#base point
# stop=GridPoint(15,2)#B point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ###################3
# stop=GridPoint(10,2)#dispatch point
# start=GridPoint(15,2)#B point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ######################
# while(1):
# 	print ser.read()
start=GridPoint(10,2)#Dispatch point
stop=GridPoint(3,2)#destination hole
length,route=solve(start,stop,frame)
execute(length,route)#starts navigation
ser.write("D")#drop the mic
start=GridPoint(3,2)#return
stop=GridPoint(10,2)
length,route=solve(start,stop,frame)
execute(length,route)
# ################
# start=GridPoint(10,2)#base point
# stop=GridPoint(15,9)#C point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ###################3
# stop=GridPoint(10,2)#dispatch point
# start=GridPoint(15,9)#C point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ###############
# start=GridPoint(10,2)#Dispatch point
# stop=GridPoint(4,2)#destination hole
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# start=GridPoint(4,2)#return
# stop=GridPoint(10,2)
# length,route=solve(start,stop,frame)
# execute(length,route)
# ###################
# start=GridPoint(10,2)#base point
# stop=GridPoint(13,9)#D point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ###################3
# stop=GridPoint(10,2)#dispatch point
# start=GridPoint(13,9)#D point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ####################
# start=GridPoint(10,2)#Dispatch point
# stop=GridPoint(5,2)#destination hole
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# start=GridPoint(5,2)#return
# stop=GridPoint(10,2)
# length,route=solve(start,stop,frame)
# execute(length,route)
# ##################
# start=GridPoint(10,2)#dispatch point
# stop=GridPoint(12,6)#Base point
# length,route=solve(start,stop,frame)
# execute(length,route)#starts navigation
# ser.write("7");

ser.write("A")#handling the control back to the bot
# execute(length,route)
>>>>>>> f111aeab9d67104ae986c3957e67477938192540
cv2.imshow("grid",frame)
#cv2.imshow("res",img)
cv2.waitKey()