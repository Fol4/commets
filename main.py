import pygame
import random

pygame.init()

'constant'

game_run = True
start_constant = False
restart_constant = 0
delay = 80

#window
win_width , win_height= 1600 , 900
pygame.display.init()
window = pygame.display.set_mode((win_width,win_height))
window.fill((46, 125, 50))

#text
enter_game = ''
pygame.font.init()
font = pygame.font.Font(None , 100)
text = font.render(enter_game , True , (0,0,0))
text_width = win_width // 2.9
text_height = win_height // 2.4

#time
time = pygame.time.Clock()

#hp
hp_constant = 10
hp_constant_restart = 10
hp_pack = []

#score
clear_score = False
final_score = 'Final Score : '
score_text = font.render('', True, (0, 0, 0))
score = 0
score_text_width , score_text_height = 0 , 0

#menu
menu_constant = 0
menu_data = []
x_menu , y_menu =win_width//2.3 , 200
menu_name = ['START' , 'SETTINGS' , 'ABOUT']
menu_spawn_constant = len(menu_name)
menu_spawn = True
menu_draw = True
menu_info = False
difficult = ['EASY' , 'MEDIUM' , 'HARD']
difficult_constant = 0

#arrow
x_arrow , y_arrow = win_width // 1.8 , 307
arrow_width , arrow_height = 15 , 15

#comet
comet_data = []
comet_speed = 2000
comet_constant = 0
# comets_image = pygame.image.load('image/comets.png')

#missile
missile_data = []
missile_speed = 5000

#rocket
x,y = win_width // 2 , win_height // 2
x_restart , y_restart = win_width // 2 , win_height // 2
width , height = 10 , 10
speed = 4
rocket = pygame.Surface((width,height))
rocket.fill((78, 52, 46))


def calcAngel(missile_x, missile_y, x, y):
    dx = missile_x - x
    dy = missile_y - y
    length = ( dx**2 + dy**2 )**1/2
    if length == 0:
        cos_alpha = 1
        sin_alpha = 0
    else:
        cos_alpha = dx/length
        sin_alpha = dy/length
    return cos_alpha, sin_alpha

def spawnMissile(self, missile_x, missile_y, x, y):
    missile = pygame.draw.rect(self , (255,255,255) , (x , y , 5 , 5))
    cos_alpha , sin_alpha = calcAngel(missile_x, missile_y, x, y)
    info = {'object': missile,
            'type': 'missile',
            'size': [5,5],
            'color': (255,255,255),
            'target': [missile_x,missile_y],
            'pos': [x,y],
            'cos': cos_alpha,
            'sin': sin_alpha}
    missile_data.append(info)

def spawnComet(self , number , width , height , win_width = None , win_height = None , x1 = None , y1 = None , x2 = None , y2 = None ):
    if number == 1:
        const = random.randint(1,2)
        if const == 1:
            x1, y1 = random.randint(1, win_width), 0
            const = random.randint(1, 3)
            if const == 1:
                x2, y2 = 0, random.randint(1, win_height)
            elif const == 2:
                x2, y2 = random.randint(1, win_width), win_height
            else:
                x2, y2 = win_width, random.randint(1, win_height)
        else:
            x1, y1 = 0, random.randint(1, win_height)
            const = random.randint(1, 3)
            if const == 1:
                x2, y2 = 0, random.randint(1, win_height)
            elif const == 2:
                x2, y2 = random.randint(1, win_width), win_height
            else:
                x2, y2 = win_width, random.randint(1, win_height)
        comet = pygame.draw.rect(self , (0,0,0) , (x1 , y1 , width , height))
        cos_alpha, sin_alpha = calcAngel(x2 , y2 , x1 , y1)
    else:
        comet = pygame.draw.rect(self, (0, 0, 0), (x1, y1, width, height))
        cos_alpha, sin_alpha = calcAngel(x2, y2, x1, y1)
    info = {'object': comet,
            'type' : 'comet',
            'size': [width , height],
            'color' : (0,0,0),
            'target': [x2, y2],
            'start_pos': [x1,y1],
            'pos': [x1, y1],
            'sin': sin_alpha,
            'cos': cos_alpha ,
            'status' : number}
    comet_data.append(info)

def flightObject(self, speed, data):
    for info in data:
        target = info['target']
        pos = info['pos']
        cos_alpha = info['cos']
        sin_alpha = info['sin']
        if abs(target[0] - pos[0]) > 4 and abs(target[1] - pos[1]) > 4:
            info['pos'][0] += speed*cos_alpha
            info['pos'][1] += speed*sin_alpha
            object = pygame.draw.rect(self, info['color'] , (pos[0], pos[1], info['size'][0], info['size'][1]))
            info['object'] = object
        else:
            data.remove(info)

def destroyObject(self ,target_data , destroyer_data):
    for target in target_data:
        target_pos = target['pos']
        object1 = target['object']
        x1,y1 = target_pos[0] , target_pos[1]
        x3,y3 = target['target'][0] , target['target'][1]
        for destroyer in destroyer_data:
            object2 = destroyer['object']
            destroyer_pos = destroyer['pos']
            if abs(target_pos[0] - destroyer_pos[0]) <= 20 and abs(target_pos[1] - destroyer_pos[1]) <= 20 and object1 != object2:
                if target['type'] == destroyer['type']:
                    x2, y2 = destroyer['target'][0], destroyer['target'][1]
                    if target['status'] !=3 and destroyer['status'] != 3:
                        spawnComet(self , target['status'] + 1 , target['size'][0] - 5 , target['size'][1] - 5 , x1 = x1+21 , y1 = y1+21 ,
                                   x2 = x2  , y2 = y2)
                        spawnComet(self , destroyer['status'] + 1, destroyer['size'][0] - 5 , destroyer['size'][1] - 5 , x1 = x1 , y1 = y1 ,
                                   x2 = x3 , y2 = y3)
                        target_data.remove(target)
                        destroyer_data.remove(destroyer)
                    elif target['status'] == 3 and destroyer['status'] != 3:
                        spawnComet(self, destroyer['status'] + 1, destroyer['size'][0] - 5, destroyer['size'][1] - 5,x1=x1, y1=y1,
                                   x2=x2, y2=y2)
                        target_data.remove(target)
                        destroyer_data.remove(destroyer)
                    elif target['status'] != 3 and destroyer['status'] == 3:
                        spawnComet(self, target['status'] + 1, target['size'][0] - 5, target['size'][1] - 5, x1=x1,y1=y1,
                                   x2=x3, y2=y3)
                        target_data.remove(target)
                        destroyer_data.remove(destroyer)
                    else:
                        target_data.remove(target)
                        destroyer_data.remove(destroyer)
                elif target['status'] != 3:
                    spawnComet(self, target['status'] + 1, target['size'][0] - 5, target['size'][1] - 5, x1=x1, y1=y1,
                               x2=x3, y2=y3)
                    target_data.remove(target)
                    destroyer_data.remove(destroyer)
                else:
                    target_data.remove(target)
                    destroyer_data.remove(destroyer)
                break

def launchComet():
    global comet_constant
    comet_constant += 1
    if comet_constant == 3-difficult_constant:
        comet_constant = 0
        spawnComet(window , 1 , 20 , 20  , win_width = win_width, win_height = win_height)

def lifeRocket(x , y , data ):
    global  restart_constant ,hp_constant
    for info in data:
        pos = info['pos']
        if abs(x-pos[0]) <= 20 and abs(y-pos[1]) <= 20 and hp_constant != 0:
            hp_constant -= 1
            data.remove(info)
        elif hp_constant == 0:
            restart_constant = True

def restartGame():
    global  comet_data , missile_data , hp_constant , x , y
    x = x_restart
    y = y_restart
    hp_constant = hp_constant_restart
    comet_data.clear()
    missile_data.clear()

def spawnStatusBar(self , hp_constant , score):
    font = pygame.font.Font(None , 31)
    hp_text = font.render('HP' ,True , (0,0,0))
    self.blit(hp_text , (10 ,win_height - 100))
    x , y = 22 , win_height - 96
    for info in range(hp_constant):
        x+= 20
        hp = pygame.draw.rect(self , (255 , 0 ,0 ) , (x , y ,12 , 12 ))
    score_text = font.render('Score', True, (0, 0, 0))
    self.blit(score_text , (10, 50))
    score_display = int(score//10)
    const = 4 - score_display // 10
    display_score_text = font.render('0'*const+str(score_display) , True , (0,0,0))
    self.blit(display_score_text , (80 , 50))

def spawnHP(self , x_rocket , y_rocket ):
    global hp_constant
    const = random.randint(1 , 1000)
    if const == 50:
        x = random.randint(100 , win_width - 100)
        y = random.randint(100 , win_height - 100)
        hp = pygame.draw.rect(self , (255,0,0) , (x , y , 20 , 20))
        info = {'object': hp ,
                'pos' : [x,y]}
        hp_pack.append(info)
    for const in hp_pack:
        pos = const['pos']
        hp = pygame.draw.rect(self, (255, 0, 0), (pos[0], pos[1], 20 , 20))
        const['object'] = hp
        if abs(x_rocket - pos[0]) <=20 and abs(y_rocket - pos[1]) <=30 :
            if hp_constant < 10:
                hp_constant += 1
            hp_pack.remove(const)

def drawArrow(self , arrow_x , arraw_y , arrow_width , arrow_height):
    pygame.draw.rect(self , (0,0,0) , (arrow_x , arraw_y , arrow_width , arrow_height))

def swapMenu(arrow_pos , menu_data):
    i = 0
    for info in menu_data:
        if i == arrow_pos :
            pos = info['pos']
        i+=1
    return pos[0]+200 , pos[1]+7

def spawnMenu(self):
    global x_menu , y_menu , menu_spawn_constant
    for spawned in range(menu_spawn_constant):
        y_menu += 100
        x,y = x_menu , y_menu
        font = pygame.font.Font(None , 50)
        text = font.render(str(menu_name[spawned]) , True , (0,0,0) )
        self.blit(text , (x,y))
        info = {'text' : text,
                'pos' : [x,y]}
        menu_data.append(info)

def drawMenu(self):
    for info in menu_data:
        window.blit(info['text'] , (info['pos'][0] , info['pos'][1]))

def drawAbout(self , x ,y):
    font = pygame.font.Font(None , (50))
    text = font.render('In this game you need destroy enemy comets' , True , (0,0,0))
    self.blit(text , (x , y))
    text = font.render('You have 10 HP . You can see them in the bottom left.' , True , (0,0,0))
    self.blit(text, (x, y+60))
    text = font.render('You can also see a red square if you pick it up you add yourself HP' , True , (0,0,0))
    self.blit(text , (x , y+120))

def drawSettings(self , x , y):
    font = pygame.font.Font(None , 50)
    text = font.render(('Difficult :           ' + difficult[difficult_constant ]) , True , (0,0,0))
    self .blit(text , (x , y))


'main loop'

while game_run:
    window.blit(text, (text_width, text_height ))
    window.blit(score_text, (score_text_width , score_text_height))
    pygame.time.delay(delay)
    pygame.display.update()
    window.fill((46, 125, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            missile_x, missile_y = pygame.mouse.get_pos()
            missile_x, missile_y = int(missile_x) , int(missile_y)
            spawnMissile(window, missile_x, missile_y, x, y)


    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] and x < win_width - 2*width:
        x += speed
    if keys[pygame.K_a] and x > width:
        x -= speed
    if keys[pygame.K_w] and y > height:
        y -= speed
    if keys[pygame.K_s] and y < win_height - 2*height:
        y += speed
    if keys[pygame.K_SPACE]:
        if clear_score:
            final_score = ''
            score_text = font.render(final_score, True, (0, 0, 0))
        if menu_constant == 0:
            start_constant = True
        if menu_constant == 1:
            menu_info = True
        if menu_constant == 2:
            menu_info = True
        enter_game = ''
        text = font.render(enter_game, True, (0, 0, 0))
        menu_draw = False
        time.tick()
    if keys[pygame.K_ESCAPE]:
        menu_draw = True
        menu_info = False
        start_constant = False
        delay = 80
    if keys[pygame.K_RIGHT] and menu_info:
        difficult_constant+=1
        if difficult_constant == 3:
            difficult_constant = 0
    if keys[pygame.K_LEFT] and menu_info:
        difficult_constant-=1
        if difficult_constant == -1:
            difficult_constant = 2
    if keys[pygame.K_DOWN]:
        menu_constant += 1
        print(menu_constant)
        if menu_constant == 3:
            menu_constant = 0
        x_arrow , y_arrow = swapMenu(menu_constant,menu_data)
    if keys[pygame.K_UP]:
        menu_constant -= 1
        if menu_constant == -1:
            menu_constant = 2
        x_arrow , y_arrow = swapMenu(menu_constant,menu_data)
    if menu_spawn:
        spawnMenu(window)
        menu_spawn = False
    if menu_draw:
        drawMenu(window)
        drawArrow(window, x_arrow, y_arrow, arrow_width, arrow_height)
    if start_constant:
        launchComet()
        spawnStatusBar(window, hp_constant , score)
        spawnHP(window , x , y )
        score += time.get_time() / 1000
        flightObject(window, missile_speed, missile_data)
        flightObject(window, comet_speed, comet_data)
        destroyObject(window, comet_data, missile_data)
        destroyObject(window, comet_data, comet_data)
        lifeRocket(x, y, comet_data)
        window.blit(rocket, (x, y))
        delay = 20
    if restart_constant:
        time.tick()
        restartGame()
        restart_constant = False
        clear_score = True
        start_constant = 0
        text = font.render('Press Space for restart game' , True , (0,0,0))
        text_width , text_height = win_width // 4.5 ,win_height // 2.6
        score_text = font.render(final_score + str(int(score//10)) , True , (0,0,0))
        score_text_width , score_text_height = win_width//2 - 225 , win_height//2

    if  menu_info:
        if menu_constant == 1:
            drawSettings(window , 300 , 200 )
        if menu_constant == 2:
            drawAbout(window , 400 , 300 )

