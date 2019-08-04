import pygame, random

screen = pygame.display.set_mode((800,600))
width,height = 800,600
clock = pygame.time.Clock()
colour = "red"

apple = pygame.image.load("apple.png")
banana = pygame.image.load("banana.png")
bomb = pygame.image.load("bomb.png")
berry = pygame.image.load("berry.png")

bg = pygame.image.load('snake_BG.jpg')
body = [(0,0)]
pygame.init()

def text(msg, x, y,w,h, colour, font, size,surf=screen):
    font = pygame.font.SysFont(font, size)
    textSurf = font.render(msg, True, colour)
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    surf.blit(textSurf, (textRect))


def button(msg,x,y,w,h,ic,ac,args=None,action=None,surf=screen):
    if surf != screen:
        mouse = pygame.mouse.get_pos()
        mouse = mouse[0]-w,mouse[1]
        click = pygame.mouse.get_pressed()
    else:
        mouse,click = pygame.mouse.get_pos(),pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(surf, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            if args != None:
                action(args)
            else:
                action()
    else:
        pygame.draw.rect(surf, ic, (x,y,w,h))
    text(msg,x,y,w,h,(0,0,0),"Segoe UI", 15,surf)


def Food(body,playerPos,colour,foodPos,foodItem,pause,lost,mode,score,scored=False):
    for z in body:
        if colour == 'red':
            pygame.draw.rect(screen, (255,0,0), (z[0]*32,z[1]*32,32,32))
        if colour == 'blue':
            pygame.draw.rect(screen, (0,0,255), (z[0]*32,z[1]*32,32,32))
        if colour == 'green':
            pygame.draw.rect(screen, (0,255,0), (z[0]*32,z[1]*32,32,32))
        if colour == 'orange':
            pygame.draw.rect(screen, (255,25,0), (z[0]*32,z[1]*32,32,32))
        if pause == False:
            if playerPos[0] == z[0] and playerPos[1] == z[1]:
                pause = True
                lost = True

    if mode != 'Blitz':
        if pause == False:
            body.append(playerPos)
            

            if foodPos[0] == playerPos[0] and foodPos[1] == int(playerPos[1]):
                foodPos = random.randint(0,24),random.randint(0,17)
                colour = random.choice(['red','green','blue','orange'])
                foodItem = random.choice([apple,banana])
                score += 1
            else:
                del body[0]
        screen.blit(foodItem, (foodPos[0]*32,foodPos[1]*32))
    else:
        for pos in list(foodPos):
            food = foodPos.get(pos)
            screen.blit(food, (pos[0]*32,pos[1]*32))
            if playerPos[0] == pos[0] and playerPos[1] == pos[1]:
                del foodPos[pos]
                if food == bomb:
                    pause = True
                    lost = True
                else:
                    foodPos[random.randint(0,24),random.randint(0,18)] = random.choice([apple,banana,bomb,berry])
                    colour = random.choice(['red','green','blue','orange'])
                    scored = True

        
                
                    
    if mode != 'Blitz':
        return foodPos, pause, lost, colour, score, foodItem
    else:
        return foodPos, pause, lost, colour, score, foodItem, scored

            
def game(mode='Normal'):
    x,y = 12,9
    clock = pygame.time.Clock()
    pause = False
    colour = random.choice(['red','green','blue','orange'])
    body = []
    score = 0
    food = random.randint(0,24),random.randint(0,17)
    foodItem = random.choice([apple,banana])
    lostSurf = pygame.Surface((600,600), pygame.SRCALPHA)
    lost = False
    if mode == 'Normal':
        face = None
        food = random.randint(0,24),random.randint(0,17)
    elif mode == 'Hard':
        face = random.choice(['up','down','right','left'])
        food = random.randint(0,24),random.randint(0,17)
    else:
        face = random.choice(['up','down','left','right'])
        food = {}
        for amount in range(4):
            food[random.randint(0,24),random.randint(0,17)] = random.choice([apple,banana,bomb,berry])
        scored = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pause == True:
                        pause = False
                    else:
                        pause = True
                    
        screen.blit(bg, (0,0))
        if pause == False:
            key = pygame.key.get_pressed()
            if key[pygame.K_w] or key[pygame.K_UP]:
                face = 'up'
            elif key[pygame.K_s] or key[pygame.K_DOWN]:
                face = 'down'
            elif key[pygame.K_a] or key[pygame.K_LEFT]:
                face = 'right'
            elif key[pygame.K_d] or key[pygame.K_RIGHT]:
                face = 'left'
            if mode == 'Normal' or mode == 'Blitz':
                if face == 'up':
                    if y > 0:
                        y -= 1
                if face == 'down':
                    if y < 18:
                        y += 1
                if face == 'right':
                    if x > 0:
                        x -= 1
                if face == 'left':
                    if x < 24:
                        x += 1
            else:
                if face == 'up':
                    if y > 0:
                        y -= 1 + score
                if face == 'down':
                    if y < 18:
                        y += 1 + score
                if face == 'right':
                    if x > 0:
                        x -= 1 + score
                if face == 'left':
                    if x < 24:
                        x += 1 + score
        if mode != 'Blitz':
            food, pause, lost, colour,score, foodItem = Food(body,(x,y),colour,food,foodItem,pause,lost,mode,score)
        else:
            food, pause, lost, colour,score, foodItem, scored = Food(body,(x,y),colour,food,foodItem,pause,lost,mode,score,scored)
            if pause == False:
                body.append((x,y))
                if scored == True:
                    score += 1
                    scored = False
                else:
                    del body[0]
        pygame.draw.rect(screen, (0,0,0), (x*32,y*32,32,32))
        text("Score: %s" % score, 5, 5,100,15, (0,0,0), 'Segoe UI', 15)
        if pause == True and lost == True:
            lostSurf.fill((200,0,0,100))
            text('You Died', 250, 30,100,30, (0,0,0), "Segoe UI", 30,lostSurf)
            text('Score: %s' % score, 250,75,100,15, (0,0,0), 'Segoe UI',15,lostSurf)
            button("Restart",250,100,100,50,(0,200,0),(0,255,0),mode,game,lostSurf)
            button("Main Menu",250,180,100,50,(0,200,0),(0,255,0),None,Main,lostSurf)
            screen.blit(lostSurf, (100,0))
        pygame.display.flip()
        clock.tick(20)



pygame.display.set_caption("Worm.ie")
def Main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(bg, (0,0))
        text("Worm.ie", width/2-100, 50,200,50, (0,0,255), 'Segoe UI', 60)
        button("Normal",width/2-50,130,100,50,(0,200,0),(0,255,0),None,game)
        button("Hard",width/2-50,210,100,50,(0,200,0),(0,255,0),'Hard',game)
        button("Blitz",width/2-50,290,100,50,(0,200,0),(0,255,0),'Blitz',game)
        button("Quit",width/2-50,370,100,50,(200,0,0),(255,0,0),None,quit)
        pygame.display.flip()

Main()
