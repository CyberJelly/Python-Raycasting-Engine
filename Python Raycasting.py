"""
Copyright (c) 2020 Connor Stevens aka CyberJelly

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
#This software was made with Python 3.7 64 bit and Pygame 1.9.6, by Connor Stevens during April 2020, and is released under the MIT license 
#I used this guide with this project and it was a great help. https://permadi.com/1996/05/ray-casting-tutorial-table-of-contents/
"""
CONTROLS

W = Forward
S = Backward
A = Strafe Left
D = Strafe Right

Left Arrow = Turn Left
Right Arrow = Turn Right

ESC = Close

The standard arrow keys must be used, not the ones on the number pad. If this still does not work, try toggling numlock or changing the controls for yourself.

"""
import math
import time
try:
    import pygame
    from pygame.locals import *
    from pygame import Color, Rect, Surface
except ImportError:
    print ("Sorry, it looks like Pygame is not installed for this version of Python.\nYou can install it at https://www.pygame.org/")
    raise ImportError
keys=[False]*324
worldX = 16
worldY = 16
worldS = 64
world = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
         [1,1,1,1,0,0,0,0,0,0,1,0,1,1,0,1],
         [1,1,1,0,0,0,0,0,0,1,1,0,1,1,0,1],
         [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1],
         [1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
         [1,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1],
         [1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1],
         [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
         [1,0,0,0,1,1,1,0,0,0,1,0,0,0,0,1],
         [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
         [1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
         [1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1],
         [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
def darken(r,g,b,amount):
    if r-amount>30:
        r-=amount
    else:
        r=30
    if g-amount>30:
        g-=amount
    else:
        g=30
    if b-amount>30:
        b-=amount
    else:
        b=30
    return(r,g,b)
def rayLength(ax,ay,bx,by,a):#This function should return the length of the ray.
    length = (math.sqrt(((bx-ax)**2)+((by-ay)**2)))
    return length
def drawRays(screen,pa,px,py,FOV):#The primary function for casting the rays and finding the intersections.
    #Initialise variables
    r=0#Loop counter
    mx=0#X Position the ray strikes on the map
    my=0#y Position the ray strikes on the map
    rx=0#End of Ray X position
    ry=0#End of Ray Y position
    #x and y offset
    xo = 0
    yo = 0
    #ra = ray angle in degrees
    ra=pa
    ra-=30
    #Set bounds of ray angle
    if ra<0:
        ra+=360
    if ra>360:
        ra-=360
    ######################Check Horizontal Line Intersection
    while r <= FOV*4:
        #dof = depth of field
        dof = 0
        straightH=False
        lenH = 100000000
        hx=px
        hy=py
        #i couldnt think of a concise name for this variable, but it is meant to be the negative inversie of the tangent of rar. inv= inverse, tan= tangent, rar = ray angle in radians
        inv_tan_ra = -1/math.tan(math.radians(ra)+0.000000001)
        if ra>180:#looking up
            #lots of maths
            ry = ((py//64)*64)-0.0001#I would use bit shifting normally as 64 is a power of two, however for some reason I cannot get it to work in this version of python. If you can get it to work, I would love to know.
            rx = (py-ry)*inv_tan_ra+px
            yo = -64
            xo = -yo*inv_tan_ra
        elif ra<180:#looking down
            #lots of maths
            ry = ((py//64)*64) +64
            rx = (py-ry)*inv_tan_ra+px
            yo = 64
            xo = -yo*inv_tan_ra
        elif ra == 0 or ra ==180:#looking straight left or right
            rx=px
            ry=py
            dof=8
            straightH=True
        while dof<16:
            #mx and my are the map x and y
            mx=int(rx//64)
            my=int(ry//64)
            if mx>worldX-1 or mx<0 or my>worldY-1 or my<0:
                break
            if world[my][mx]>0:#if there is wall
                dof = 16
                hx=rx
                hy=ry
                lenH = rayLength(px,py,hx,hy,ra)
            else:#If there is not a wall, we can add the x and y offset and check again for wall. This is so efficient as we only have to check once per cell, not once per pixel like other engines
                rx+=xo
                ry+=yo
                dof+=1
    ######################Check Vertical Line Intersection
        #dof = depth of field
        dof = 0
        lenV = 100000000
        vx=px
        vy=py
        #negative tangent of ray angle
        n_tan_ra = -math.tan(math.radians(ra))
        straight = False
        if ra>90 and ra<270:#looking left
            #lots of maths
            rx = ((int(px)//64)*64)-0.0001#I would use bit shifting normally as 64 is a power of two, however for some reason I cannot get it to work in this version of python. If you can get it to work, I would love to know.
            ry = (px-rx)*n_tan_ra+py
            xo = -64
            yo = -xo*n_tan_ra
        elif ra<90 or ra>270:#looking right
            #lots of maths
            rx = ((px//64)*64) +64
            ry = (px-rx)*n_tan_ra+py
            xo = 64
            yo = -xo*n_tan_ra
        elif ra == 0 or ra ==180:#looking straight up or down
            rx=px
            ry=py
            dof=8
            straight = True
        while dof<16:
            #mx and my are the map x and y
            mx=int(rx//64)
            my=int(ry//64)
            if mx>worldX-1 or mx<0 or my>worldY-1 or my<0:
                break
            if world[my][mx]>0:#if there is wall
                dof = 16
                vx=rx
                vy=ry
                lenV = rayLength(px,py,vx,vy,ra)
            else:#If there is not a wall, we can add the x and y offset and check again for wall. This is so efficient as we only have to check once per cell, not once per pixel like other engines
                rx+=xo
                ry+=yo
                dof+=1
        if lenH<lenV and straight == False:
            rx=hx
            ry=hy
            length = lenH
            colour = (255,255,255)
        elif straight == False:
            rx=vx
            ry=vy
            length = lenV
            colour = (225,225,225)
        else:
            rx=vx
            ry=vy
            length = lenV
            colour = (255,255,255)
        if straightH==True:
            colour=(225,225,225)
        pygame.draw.line(screen, (0,255,0),(px/2,py/2),(rx/2,ry/2),2)
        ra+=0.25
        #Set bounds of ray angle
        if ra<0:
            ra+=360
        if ra>360:
            ra-=360
        ###################### Draw 3D Walls :)
        #Fisheye Correction
        colour = darken(colour[0],colour[1],colour[2],round(length/3.5))#This line is to darken the wall the further from the player it is
        # Counterract Fisheye Effect
        ca=pa-ra
        if ca<0:
            ca+=360
        if ca>360:
            ca-=360
        length = length*(math.cos(math.radians(ca)))
        #Line Height and Offset
        lineH = worldS*320/length
        if lineH > 320:#Set max line height to 320
            lineH = 320
        lineO =160-lineH/2
        #Draw Line
        try:
            pygame.draw.line(screen,(colour[0],colour[1],colour[2]),(r*2+515,lineO),(r*2+515,lineO+lineH),2)
        except:
            #Sometimes te above line of code springs an error if the ray happens to go out of the grid at some point, so this is just a safety net in case that happens.
            pygame.draw.line(screen,(0,0,0),(r*8+521,lineO),(r*8+515,lineO+lineH),8)
        r+=1#Increment loop variable
def drawPlayer(screen,x,y,a):#Draw player onto screen
    pygame.draw.rect(screen, (255,255,0), (x/2-4,y/2-4,8,8), 0)
    axy = angleXY(a,x/2,y/2,15)
    pygame.draw.line(screen, (255,255,0),(x/2,y/2),axy,3)
def angleXY(a,x,y,length): #Simple function to convert an angle and length into its x and y counterparts. This simplifies things greatly, as without it dealing with angles is very difficult.
    ax = x + math.cos(math.radians(a)) * length
    ay = y + math.sin(math.radians(a)) * length
    return (ax,ay)
def drawMap(screen):#Function to draw the 2D world map
    cellX = 0
    cellY = 0
    #loop through the array "world". current cell is a 1 (wall), create white square. if it is a 0 (empty), create black square. the outlines come from the squares being spaced apart slightly and the background being a different colour.
    for y in range(worldY):
        for x in range(worldX):
            if world[y][x] == 1:
                pygame.draw.rect(screen, (255,255,255), (cellX,cellY,worldS/2-2,worldS/2-2),0)
            else:
                pygame.draw.rect(screen, (0,0,0), (cellX,cellY,worldS/2-2,worldS/2-2),0)
            cellX+= 32
        cellY+= 32
        cellX =0
    pygame.draw.rect(screen, (0,0,0), (512,0,508,330),0)
    pygame.draw.rect(screen, (20,20,20), (516,0,500,326),2)
def leave():#close window when escape is pressed
    pygame.display.quit()
    pygame.quit()
def main():
    #player position
    px = 300.0
    py = 300.0
    #player angle
    pa = 0
    pygame.init()#Initialise the pygame module
    WIDTH = 1024
    HEIGHT = 512
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    #FOV = Field of View
    FOV = 90#Although python uses radians not degrees for angles, degrees are significantly easier to work with.
            #If performance is an issue, one way to optimise this would be to use radians for all your variables, then you would not need to do any converting.
    while True:
        screen.fill((50,50,50))
        drawMap(screen)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                keys[event.key] = True
            elif event.type == KEYUP:
                keys[event.key] = False   
        #if ESC pressed exit
        if keys[K_ESCAPE]:
            leave()
            return
        #Movement
        if keys[K_a]:#LEFT
            speed = 1
            paTEMP=pa-90
            if paTEMP<0:
                paTEMP+=360
            new_pXY = angleXY(paTEMP,px,py,speed)
            mx=int(new_pXY[0]//64)
            my=int(new_pXY[1]//64)
            if world[my][mx] ==0:#Collision
                px = new_pXY[0]
                py = new_pXY[1]
        if keys[K_d]:#RIGHT
            speed = 1
            paTEMP=pa+90
            if paTEMP<0:
                paTEMP+=360
            new_pXY = angleXY(paTEMP,px,py,speed)
            mx=int(new_pXY[0]//64)
            my=int(new_pXY[1]//64)
            if world[my][mx] ==0:#Collision
                px = new_pXY[0]
                py = new_pXY[1]
        if keys[K_w]:#FORWARD
            speed = 1
            new_pXY = angleXY(pa,px,py,speed)
            mx=int(new_pXY[0]//64)
            my=int(new_pXY[1]//64)
            if world[my][mx] ==0:#Collision
                px = new_pXY[0]
                py = new_pXY[1]
        if keys[K_s]:#BACK
            speed = -1
            #calculate new position after movement
            new_pXY = angleXY(pa,px,py,speed)
            mx=int(new_pXY[0]//64)
            my=int(new_pXY[1]//64)
            if world[my][mx] ==0:#Collision
                px = new_pXY[0]
                py = new_pXY[1]
        if keys[K_LEFT]:#TURN LEFT
            pa -= 1.1#It is 1.1 not 1 because for some reason whenever it is 1 there is a really odd lighting glitch, this was the only reliable fix I could find.
            if pa < 0:
                pa = 359
        if keys[K_RIGHT]:#TURN RIGHT
            pa += 1.1#It is 1.1 not 1 because for some reason whenever it is 1 there is a really odd lighting glitch, this was the only reliable fix I could find.
            if pa > 359:
                pa = 0
        drawRays(screen,pa,px,py,FOV)#Function to draw 2D and 3D rays onto screen
        drawPlayer(screen,px,py,pa)#Function to draw player
        pygame.display.flip()#Refresh screen
main()
#Without comments, this would be under 300 lines :)
