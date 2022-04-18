
#Libraries
import pygame
import math
import sys

#Setup of pygame and necessary constants
HEIGHT = 600
TOTALWIDTH = 800
WIDTH = 600
render = 3
pixelHeight = HEIGHT // render
pixelWidth = WIDTH // render
iterations = 100
count = 0
screen = pygame.display.set_mode([TOTALWIDTH, HEIGHT])
pygame.init()
backToMenu = pygame.Rect(0, 0, 20, 20)
menuButton = pygame.image.load('pil.png')
menuButtonRect = menuButton.get_rect()

#Function: Color
#Input: (int)
#Outputs a color (r, g, b) ranging from red-yellow-green-blue-black depending on the value of the input.
def color(num):
    switch = iterations//5
    if num <= iterations//5:
        red = 255
        green = int(255*num/(iterations//5))
        blue = 0
    elif num <= iterations*2//5:
        num -= iterations//5
        red = int(255*num/(iterations//5))
        green = 255
        blue = 0
    elif num <= iterations*3//5:
        num -= iterations*2//5
        red = 0
        green = 255
        blue = int(255*num/(iterations//5))
    elif num <= iterations*4//5:
        num -= iterations*3//5
        red = 0
        green = int(255*num/(iterations//5))
        blue = 255
    elif num <= iterations:
        num -= iterations*4//5
        red = int(255*num/(iterations//5))
        green = 0
        blue = 255
    else:
        red = 0
        green = 0
        blue = 0
    return (red, green, blue)

#Function: Julia value
#Input: (int, int, int, int)
#Outputs number of iterations before the julia set calculation reaches a value of 2
def julia_value(realBase, imagBase, realConstant, imagConstant):
    constant = complex(realConstant, imagConstant)
    base = complex(realBase, imagBase)
    for i in range(iterations):
        base = base**2 + constant
        distance = base.real**2 + base.imag**2
        if distance >= 4:
            return i
    return 1000

#Function: Draw julia set
#Input: (int, int)
#Draws a pixel of the julia set
def draw_julia_set(realConstant, imagConstant):
    for imagNum in range(pixelHeight):
        for realNum in range(pixelWidth):
            imagBase = (imagNum / pixelHeight)*4 - 2
            realBase = (realNum / pixelWidth)*4 - 2
            untilTooBig = julia_value(realBase, imagBase, realConstant, imagConstant)
            colorValue = color(untilTooBig)
            pixel = pygame.Rect(imagNum*render, realNum*render, render, render)
            pygame.draw.rect(screen, colorValue, pixel)    

#Function: Menu
#Input: -
#Runs a menu screen
def menu():
    global count
    screen.fill((255, 255, 255))
    b0 = button(screen, (200, 200), "Animation", 50, "white on green")
    b1 = button(screen, (200, 300), "Sandbox", 50, "white on green")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if b0.collidepoint(pygame.mouse.get_pos()):
                    circle_animation()
                    screen.fill((255, 255, 255))
                    b0 = button(screen, (200, 200), "Animation", 50, "white on green")
                    b1 = button(screen, (200, 300), "Sandbox", 50, "white on green")
                elif b1.collidepoint(pygame.mouse.get_pos()):
                    sandbox()
                    screen.fill((255, 255, 255))
                    b0 = button(screen, (200, 200), "Animation", 50, "white on green")
                    b1 = button(screen, (200, 300), "Sandbox", 50, "white on green")
        pygame.display.flip()

#Function: Button
#Input(surface, tuple(int, int), string, int, string)
#Renders a button on given surface
def button(screen, position, text, size, colors="white on blue"):
    fg, bg = colors.split(" on ")
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, 1, fg)
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, bg, (x, y, w , h))
    return screen.blit(text_render, (x, y)) 

#Function: Circle animation
#Input: -
#Runs a gamemode that generates julia sets in an animation around a circle
def circle_animation():
    count = 0
    while True:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuButtonRect.collidepoint(pygame.mouse.get_pos()):
                    return 0

        angle = (count/90) * (math.pi * 2)
        y = math.sin(angle)
        x = math.cos(angle)
        draw_julia_set(x, y)
        screen.blit(menuButton, menuButtonRect)
        pygame.draw.circle(screen, (0,255,0), (700, 100), 90, width=2)
        pygame.draw.circle(screen, (255,0,0), (700+y*90, 100+x*90), 3)

        pygame.display.flip()
        count += 1

#Function: Sandbox
#Input: -
#Runs a gamemode that allows the user to render a Julia set with their own starting values
def sandbox():
    #Setup for gamemode
    screen.fill((255, 255, 255))
    count = 0
    x = 1
    y = 1

    #Setup for inputs
    inputX = pygame.Rect(650, 100, 100, 20)
    inputY = pygame.Rect(650, 200, 100, 20)
    pygame.draw.rect(screen, (0, 0, 0), inputX) 
    pygame.draw.rect(screen, (0, 0, 0), inputY) 
    textX = ""
    textY = ""
    input_activeX = False
    input_activeY = False
    font = pygame.font.SysFont(None, 19)

    #Game loop
    while True:

        #All user inputs
        for event in pygame.event.get():
            #Exits the program if quit button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Goes to menu if menu button is pressed
                if menuButtonRect.collidepoint(pygame.mouse.get_pos()):
                    return 0

                #Takes input for x if text field is pressed
                if inputX.collidepoint(pygame.mouse.get_pos()):
                    input_activeX = True
                
                #Takes input for y if text field is pressed
                if inputY.collidepoint(pygame.mouse.get_pos()):
                    input_activeY = True

            #Takes input string for x-value in Julia set    
            elif event.type == pygame.KEYDOWN and input_activeX:
                if event.key == pygame.K_RETURN:
                    input_activeX = False
                    count = 0
                    x = float(textX)
                elif event.key == pygame.K_BACKSPACE:
                    textX =  textX[:-1]
                else:
                    textX += event.unicode
            
            #Takes input string for y-value in Julia set
            elif event.type == pygame.KEYDOWN and input_activeY:
                if event.key == pygame.K_RETURN:
                    input_activeY = False
                    count = 0
                    y = float(textY)
                elif event.key == pygame.K_BACKSPACE:
                    textY =  textY[:-1]
                else:
                    textY += event.unicode
        
        #Renders julia set on the screen
        if count == 0:
            draw_julia_set(float(x), float(y))
        
        #Renders input string for x-value on the screen
        pygame.draw.rect(screen, (0, 0, 0), inputX)  
        text_surfX = font.render(textX, True, (0, 255, 0))
        screen.blit(text_surfX, text_surfX.get_rect(center = inputX.center))

        #Renders input string for y-value on the screen
        pygame.draw.rect(screen, (0, 0, 0), inputY)
        text_surfY = font.render(textY, True, (0, 255, 0))
        screen.blit(text_surfY, text_surfY.get_rect(center = inputY.center))

        #Renders menu button on the screen
        screen.blit(menuButton, menuButtonRect)

        pygame.display.flip()
        count += 1

#Function: Run game
#Input: -
#Runs the program
def run_game():
    menu()

run_game()

