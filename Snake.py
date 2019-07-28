import pygame

def init(username):
    username = username

test = True


def run(self,screen,width,height,display,config,pause,leave,click,activeWindow,gameBar=None):
    print(display)
    if config[3] == "Game Bar":
        gameBar = False
    else: gameBar = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    screen.fill((0,58,58))
    if gameBar != None:
        mouse = pygame.mouse.get_pos()
        if 0+width > mouse[0] > 0 and 0+30 > mouse[1] > 0:
            pygame.draw.rect(screen, (0,0,0), (0,0,width,30))
            pygame.draw.rect(screen, (255,0,0), (width-45,0,45,30)) # QUIT BUTTON
            if gameBar != None:
                pygame.draw.rect(screen, (119,136,153), (width-90,0,45,30))
                if mouse[0] > width-90 and mouse[0] < width-45:
                    if mouse[1] < 30 and click == True:

                        print("tried minimizing")
                        gameBar = True
                        pause = True
                        activeWindow = False
            if mouse[0] > width-45 and mouse[1] < 30:
                if click == True:
                    activeWindow = False
            
    pygame.display.flip()
    if gameBar != None:
        return pause,leave,click,activeWindow,gameBar
    else:
       return pause,leave,click,activeWindow 

##if test == True:
##    screen = pygame.display.set_mode((800,600),pygame.RESIZABLE)
    
    

