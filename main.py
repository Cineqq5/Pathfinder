import random, pygame, sys
from pygame.locals import *
boxSize=15
width, height = 900, 600
size = widthW, heightW = width+200, height+200
screen = pygame.display.set_mode(size)
mouseClicked = False
map={}

#0- white, 1- black, 2- red, 3-green
boxstart = pygame.image.load("boxstart.png")
boxstartrect = boxstart.get_rect()
boxend = pygame.image.load("boxend.png")
boxendrect = boxend.get_rect()
box = pygame.image.load("box15.png")
boxrect = box.get_rect()
boxc = pygame.image.load("boxc15.png")
boxcrect = boxc.get_rect()
#4- pink temp, 5- blue path
boxt = pygame.image.load("temp.png")
boxtrect = boxt.get_rect()
boxtt = pygame.image.load("checked.png")
boxttrect = boxtt.get_rect()

kappaX=[boxSize,0,-boxSize,0]
kappaY=[0,boxSize,0,-boxSize]



def drawSolution(x,y,p,sol):
    if p == 0:
        return sol
    for i in range(4):
        if ifXYinBox(x + kappaX[i], y + kappaY[i]) and len(map[x + kappaX[i]][y + kappaY[i]]) > 1 and map[x + kappaX[i]][y + kappaY[i]][1] == p - 1:
            sol.append([x + kappaX[i], y + kappaY[i]])
            return drawSolution(x + kappaX[i], y + kappaY[i], p - 1, sol)

def ifXYinBox(x, y):
    return True if x in map and y in map[x] else False

time=0
def startSimulation():
    for a in range(width // boxSize):
        for b in range(height // boxSize):
            x = a * boxSize + (widthW - width) / 2
            y = b * boxSize + (heightW - height) / 2

            if map[x][y][0] == 2 or map[x][y][0] == 5:
                for i in range(4):
                    xx, yy = x+kappaX[i], y+kappaY[i]
                    if ifXYinBox(xx, yy) and (map[xx][yy][0] == 0 or map[xx][yy][0] == 3): map[xx][yy] = [4, map[x][y][1] + 1]

    for a in range(width // boxSize):
        for b in range(height // boxSize):
            x = a * boxSize + (widthW - width) / 2
            y = b * boxSize + (heightW - height) / 2
            if map[x][y][0] == 4: map[x][y][0] = 5

def draw():
    # draw
    for a in range(width // boxSize):
        for b in range(height // boxSize):
            x = a * boxSize + (widthW - width) / 2
            y = b * boxSize + (heightW - height) / 2
            if map[x][y][0] == 0:
                boxrect.x, boxrect.y = x, y
                screen.blit(box, boxrect)
            elif map[x][y][0] == 1:
                boxcrect.x, boxcrect.y = x, y
                screen.blit(boxc, boxcrect)
            elif map[x][y][0] == 2:
                boxstartrect.x, boxstartrect.y = x, y
                screen.blit(boxstart, boxstartrect)
            elif map[x][y][0] == 3:
                boxendrect.x, boxendrect.y = x, y
                screen.blit(boxend, boxendrect)
            elif map[x][y][0] == 4:
                boxtrect.x, boxtrect.y = x, y
                screen.blit(boxt, boxtrect)
            elif map[x][y][0] == 5:
                boxttrect.x, boxttrect.y = x, y
                screen.blit(boxtt, boxttrect)

def drawMap():
    for a in range(width//boxSize + 1):
        x = a * boxSize + (widthW - width) / 2
        map[x]={}
        for b in range(height//boxSize +1):
            y=b*boxSize+(heightW-height)/2
            map[x][y]=[0]

def instantDraw(boxEndw):
    while not (len(boxEndw) > 0 and len(map[boxEndw[0]][boxEndw[1]]) > 1):
        startSimulation()
    map[boxEndw[0]][boxEndw[1]][0] = 3
    sol = drawSolution(boxEndw[0], boxEndw[1], map[boxEndw[0]][boxEndw[1]][1], [])
    for x in sol:
        if map[x[0]][x[1]][0] != 2:
            map[x[0]][x[1]][0] = 4

def drawText(text, x, y):
    font = pygame.font.SysFont('Arial', 20)
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x,y))

def main():
    pygame.init()
    screen.fill((255, 255, 255))
    drawText('Controls:', width/2 - 150, 100+height+30)
    drawText('Control Points: S - Start point, E - End point', width / 2 + 150, 130 + height)
    drawText('Create obstacles by mouse', width / 2 - 150, 160 + height)
    drawText('Simulation: W - StepByStep, E - Instant', width / 2 + 150, 160 + height)

    solved=False
    mouseClicked = False
    simulation=False

    boxStartw = []
    boxEndw = []

    drawMap()

    mouse_x = 0
    mouse_y = 0
    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    
    for a in range(width // boxSize + 2):
        x = (a - 1) * boxSize + (widthW - width) / 2
        for b in range(height // boxSize + 2):
            y = (b-1) * boxSize + (heightW - height) / 2
            boxcrect.x, boxcrect.y = x, y
            screen.blit(boxc, boxcrect)

    while(1):

        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                mouseClicked = True
            elif event.type == MOUSEBUTTONUP:
                mouseClicked = False

            elif event.type == KEYDOWN and not mouseClicked:
                if event.key == K_s:
                    curr_x = (mouse_x - 100) % 15
                    curr_y = (mouse_y - 100) % 15
                    if boxStartw:
                        map[boxStartw[0]][boxStartw[1]]=[0]
                    x = mouse_x - 100 - curr_x + (widthW - width) / 2
                    y = mouse_y - 100 - curr_y + (heightW - height) / 2
                    boxStartw = [x,y]
                    map[x][y] = [2,0]
                elif event.key == K_d:
                    curr_x = (mouse_x - 100) % 15
                    curr_y = (mouse_y - 100) % 15
                    if boxEndw:
                        map[boxEndw[0]][boxEndw[1]]=[0]
                    x = mouse_x - 100 - curr_x + (widthW - width) / 2
                    y = mouse_y - 100 - curr_y + (heightW - height) / 2
                    boxEndw = [x, y]
                    map[x][y] = [3]
                elif event.key == K_w:
                    simulation = not simulation
                elif event.key == K_r:
                    boxStartw=[]
                    boxEndw=[]
                    drawMap()
                elif event.key == K_e:
                    solved=True
                    map[boxStartw[0]][boxStartw[1]] = [map[boxStartw[0]][boxStartw[1]][0],0]
                    map[boxEndw[0]][boxEndw[1]] = [map[boxEndw[0]][boxEndw[1]][0]]
                    instantDraw(boxEndw)

        if mouseClicked:
            if mouse_x >100 and mouse_x <100+width and mouse_y >100 and mouse_y <100+height:
                curr_x = (mouse_x - 100)%15
                curr_y = (mouse_y - 100) % 15

                x = mouse_x - 100 - curr_x + (widthW - width) / 2
                y = mouse_y - 100 - curr_y + (heightW - height) / 2
                if map[x][y][0]==0 or map[x][y][0]>3:
                    map[x][y][0]=1
            if solved:
                for x in map:
                    for y in map[x]:
                        if map[x][y][0]>3:
                            map[x][y]=[0]

        draw()
        if simulation :
            startSimulation()
            if len(boxEndw)>0 and len(map[boxEndw[0]][boxEndw[1]]) > 1:
                solved=True
                simulation=False
                map[boxEndw[0]][boxEndw[1]][0]=3
                print(map[boxEndw[0]][boxEndw[1]][1])
                sol=[]
                sol=drawSolution(boxEndw[0],boxEndw[1],map[boxEndw[0]][boxEndw[1]][1], sol)
                for x in sol:
                    map[x[0]][ x[1]][0] = 4
                map[boxStartw[0]][boxStartw[1]][0]=2

        pygame.display.flip()



if __name__ == '__main__':
    main()