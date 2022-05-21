import socket
import pygame

pygame.init()
#=====<Переменные>=====
Window_Caption = "Президенты: Война за снюс"
Window_Width, Window_Height = 1280, 720
Player_Width, Player_Height = 70, 100
Player_Pos_x, Player_Pos_y = 150, 0
Player_Speed = 5
Player_SprintSpeed = 6
Player_Jump_Count = 12
Player_Stamina, Player_Full_Stamina, Player_Stamina_Tratitsa, Player_Stamina_Vostanavlivaetsa = 200, 200, 1, 2
Player_Anim_Count = 0
Player_Looking_Away = 0
FramePerSecond = 60
Music_Played_Count = 0
Player_Movement_x_Zaprescheno, Player_Movement_y_Zaprescheno = 0, 0
cifra = 0
Gravitation = 12
Player_Name = 'Snusoed'
Message_Old = "None"
Player_Jump = False
GameRunned = True
Print_FPS = True
Draw_Collision = False
MultiPlayer = True
LCTRL_pressed = False
Game_Icon = pygame.image.load('icon.ico')
Game_BackGroundImage = pygame.image.load("images/fon.jpg")
#=====<Создание окна игры>=====
Window = pygame.display.set_mode((Window_Width, Window_Height))
pygame.display.set_caption(Window_Caption)
pygame.display.set_icon(Game_Icon)
FPSlimit = pygame.time.Clock()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
font = pygame.font.Font(None, 50)
name_font = pygame.font.Font(None, 25)
#=====<дефайны и классы>=====
class Platform():
    def __init__(self, Position_x, Position_y, Width, Height, Rotate = 0, Collizion = True):
        self.Position_x = Position_x
        self.Position_y = Position_y
        self.Width = Width
        self.Height = Height
        self.Rotate = Rotate
        self.Speed = 5
        self.Move_x = 0
        self.Move_y = 0
        self.Collizion = Collizion
    def Move(self, x,y, speed):
        pass
Platforms = [Platform(1000, 620, 100, 100), Platform(600, 650, 56, 45), Platform(500, 600, 80, 45), Platform(180, 550, 80, 45)]
def Events():#=====<Обработка событий>=====
    global Player_Pos_x, Player_Pos_y, FramePerSecond, Player_Width, Player_Height, cifra
    #=====<Телепортация на другой край окна>=====
    if Player_Pos_x > Window_Width+Player_Width//2: Player_Pos_x = 0-Player_Width//2
    if Player_Pos_x < 0-Player_Width//2: Player_Pos_x = Window_Width+Player_Width//2
    if cifra <= FramePerSecond: cifra += 1
    if cifra > FramePerSecond: cifra = 0
    if not Player_Jump and Player_Pos_y < 610 and Player_Movement_y_Zaprescheno != 1: Player_Pos_y += Gravitation
    if Window_Height+2 <= Player_Pos_y+Player_Height: Player_Pos_y = 100
def Connect_To_Server():#=====<Подключение к серверу>=====
    global client, MultiPlayer
    if MultiPlayer:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            client.connect(("localhost", 8889))
        except:
            MultiPlayer = False
def Files_Load():#=====<Импорт файлов>=====
    global Players_Walk_Left, Players_Walk_Right, Players_Stopped, music1, music2, music3, music4, music5
    #=====<Музыка>=====
    music1 = pygame.mixer.Sound('tracks\music1.mp3')
    music2 = pygame.mixer.Sound('tracks\music2.mp3')
    music3 = pygame.mixer.Sound('tracks\music3.mp3')
    music4 = pygame.mixer.Sound('tracks\music4.mp3')
    music5 = pygame.mixer.Sound('tracks\music5.ogg')
    #=====<Текстуры игроков, настройка их размера>=====
    Players_Walk_Left = [pygame.image.load('images\left_1.png'),
    pygame.image.load('images\left_2.png'), pygame.image.load('images\left_3.png'),
    pygame.image.load('images\left_4.png'), pygame.image.load('images\left_5.png'),
    pygame.image.load('images\left_6.png')]
    Players_Walk_Right = [pygame.image.load('images/right_1.png'),
    pygame.image.load('images/right_2.png'), pygame.image.load('images/right_3.png'),
    pygame.image.load('images/right_4.png'), pygame.image.load('images/right_5.png'),
    pygame.image.load('images/right_6.png')]
    Players_Stopped = pygame.image.load('images/pstoit.png').convert_alpha()#=====<Импорт файлов>=====
def Texture_Obrabotka():
    global Players_Walk_Left, Players_Walk_Right, Players_Stopped
    for i in Players_Walk_Left:
        element_index = Players_Walk_Left.index(i)
        i.convert_alpha()
        if not MultiPlayer:
            i = pygame.transform.scale(i, (Player_Width, Player_Height))
        Players_Walk_Left[element_index] = i
    for i in Players_Walk_Right:
        element_index = Players_Walk_Right.index(i)
        i.convert_alpha()
        if  not MultiPlayer:
            i = pygame.transform.scale(i, (Player_Width, Player_Height))
        Players_Walk_Right[element_index] = i
    if not MultiPlayer:
        Players_Stopped = pygame.transform.scale(Players_Stopped, (Player_Width, Player_Height))
if MultiPlayer:
    def find(s):#=====<Обработка информации с сервера>=====
        start = False
        infa = ''
        res = []
        for i in s:
            if i == "<":
                start = True
                continue
            if start and i != ">":
                infa += i
            if i == ">":
                res.append(infa)
                infa = ""
                start = False
        return res
#=====<>=====
def musicoff():
    try:
        music1.stop()
        music2.stop()
        music3.stop()
        music4.stop()
        music5.stop()
    except NameError:
        print('Ошибка остановки одного из треков!')
def musicplayer():
    if Music_Played_Count == 1:
        music1.play()
    elif Music_Played_Count == 2:
        musicoff()
        music2.play()
    elif Music_Played_Count == 3:
        musicoff()
        music3.play()
    elif Music_Played_Count == 4:
        musicoff()
        music4.play()
    elif Music_Played_Count == 5:
        musicoff()
        music5.play()
def menu():
    pass
def Check_Keys():
    global GameRunned, Player_Stamina, Player_Jump, Player_Pos_x, Player_Pos_y, Player_Jump_Count, Player_Width, Player_Height, Player_Looking_Away, Player_Anim_Count, Player_Stamina_Vostanavlivaetsa, Draw_Collision, Print_FPS
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
                GameRunned = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                if Print_FPS: Print_FPS = False
                else: Print_FPS = True
            elif event.key == pygame.K_c:
                if Draw_Collision: Draw_Collision = False
                else: Draw_Collision = True
            elif event.key == pygame.K_x: Player_Pos_x -= 1
            elif event.key == pygame.K_v: Player_Pos_x += 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                Music_Played_Count -= 1
                musicoff()
                musicplayer()
            elif event.key == pygame.K_RIGHT:
                Music_Played_Count += 1
                musicoff()
                musicplayer()
            elif event.key == pygame.K_DOWN:
                musicoff()
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_d] and Player_Movement_x_Zaprescheno != 1:
        if Keys[pygame.K_LSHIFT] and Player_Stamina > 0:
            Player_Pos_x += Player_SprintSpeed
            Player_Stamina -= Player_Stamina_Tratitsa
        else:
            if Player_Stamina < Player_Full_Stamina:
                Player_Stamina += Player_Stamina_Vostanavlivaetsa/4
        Player_Pos_x += Player_Speed
        Player_Looking_Away = 1
    elif Keys[pygame.K_a] and Player_Movement_x_Zaprescheno != 2:
        if Keys[pygame.K_LSHIFT] and Player_Stamina > 0:
            Player_Pos_x -= Player_SprintSpeed
            Player_Stamina -= Player_Stamina_Tratitsa
        else:
            if Player_Stamina < Player_Full_Stamina:
                Player_Stamina += Player_Stamina_Vostanavlivaetsa/4
        Player_Pos_x -= Player_Speed
        Player_Looking_Away = -1
    else:
        Player_Looking_Away = 0
        if Player_Stamina <= Player_Full_Stamina:
            Player_Stamina += Player_Stamina_Vostanavlivaetsa
    if not(Player_Jump):
        if Keys[pygame.K_SPACE]:
            Player_Jump = True
    else:
        if Player_Jump_Count >= -12 and Player_Movement_y_Zaprescheno != 2:
            if Player_Jump_Count < 0:
                if Player_Movement_y_Zaprescheno != 1:
                    Player_Pos_y += (Player_Jump_Count ** 2) / 5
            else:
                Player_Pos_y -= (Player_Jump_Count ** 2) / 5
            Player_Jump_Count -= 1
        else:
            Player_Jump = False
            Player_Jump_Count = 12
def Draw_In_Window (data):#=====<Отрисовка обьектов в окне игры>=====
    global Player_Anim_Count, Player_Pos_x, Player_Pos_y, Player_Movement_x_Zaprescheno, Player_Movement_y_Zaprescheno
    Window.blit(Game_BackGroundImage, (0,0))
#=====<>=====
    #=====<>=====
    if Draw_Collision:
        pygame.draw.rect(Window, (128, 128, 128), ((Player_Pos_x, Player_Pos_y), (Player_Width, Player_Height)))
    if Player_Anim_Count + 1 >= 30:
        Player_Anim_Count = 0
    if Player_Looking_Away == -1:
        if not MultiPlayer:
            player = Window.blit(Players_Walk_Left[Player_Anim_Count // 5], (Player_Pos_x, Player_Pos_y))
        Player_Anim_Count += 1
    elif Player_Looking_Away == 1:
        if not MultiPlayer:
            player = Window.blit(Players_Walk_Right[Player_Anim_Count // 5], (Player_Pos_x, Player_Pos_y))
        Player_Anim_Count += 1
    else:
        if not MultiPlayer:
            player = Window.blit(Players_Stopped, (Player_Pos_x, Player_Pos_y))
        #=====<>=====
    if not MultiPlayer:
        Player_Movement_x_Zaprescheno = 0
        Player_Movement_y_Zaprescheno = 0
        for i in Platforms:
            new_platform = pygame.draw.rect(Window, (0, 0, 255), ((i.Position_x, i.Position_y), (i.Width, i.Height)))
            if Player_Pos_y+Player_Height-5 >= i.Position_y and Player_Pos_y <= i.Position_y+i.Height:
                if player.collidepoint(new_platform.left, Player_Pos_y):
                    print('left')
                    Player_Movement_x_Zaprescheno = 1
                if player.collidepoint(new_platform.right, Player_Pos_y):
                    print('right')
                    Player_Movement_x_Zaprescheno = 2
            if Player_Pos_y + Player_Width <= i.Position_y+10:
                if new_platform.colliderect(player):
                    print('thtdh')
                    Player_Movement_y_Zaprescheno = 1
                    Player_Pos_y = i.Position_y-Player_Height+1
            else:
                print('')
#=====<>=====
    if MultiPlayer:
        for i in range(len(data)):
            try:
                j=data[i].split(' ')
                x=float(j[0])#=====<Позиция игрока по х>=====
                y=float(j[1])#=====<Позиция игрока по у>=====
                w=float(j[2])#=====<Ширина игрока>=====
                h=float(j[3])#=====<Высота игрока>=====
                a=int(j[4])#=====<Номер анимации игрока>=====
                an=int(j[5])#=====<Сторона в которую смотрит игрок>=====
                n = j[6]#=====<Имя игрока>=====
                if a + 1 >= 30:
                    a = 0
                if an == -1:
                    p = pygame.transform.scale(Players_Walk_Left[a // 5], (w, h))
                    a += 1
                elif an == 1:
                    p = pygame.transform.scale(Players_Walk_Right[a // 5], (w, h))
                    a += 1
                else:
                    p = pygame.transform.scale(Players_Stopped, (w, h))
                Window.blit(p, (x, y))
                text = name_font.render(n, True, (0,0,0))#=====<>=====
                dfg = text.get_rect()
                Window.blit(text, [x-((dfg[2]//2)-(w//2)), y-15])#vivod imeni
            except:
                pass
    Stamina_Color = round(Player_Stamina/Player_Full_Stamina*255)
    Stamina_Procent = round(Player_Stamina/Player_Full_Stamina*100)
    if Stamina_Color > 255: Stamina_Color = 255
    if Stamina_Color < 0: Stamina_Color = 0
    if Stamina_Procent > 100: Stamina_Procent = 100
    if Stamina_Procent < 0: Stamina_Procent = 0
    pygame.draw.rect(Window, (0, 0, 0), ((1177, 3), (100, 30)))
    pygame.draw.rect(Window, (255-Stamina_Color, Stamina_Color, 0), ((1177, 3), (Stamina_Procent, 30)))
    text = font.render(str(Stamina_Procent)+"%", True, (255,255,0))
    text = pygame.transform.scale(text, (100, 30))
    Window.blit(text, (1177, 3))
    if Print_FPS:
        FPStext = font.render(str(round(FPSlimit.get_fps())), True, (0,0,0))
        FPStext = pygame.transform.scale(FPStext, (30, 20))
        Window.blit(FPStext, (3, 3))
#==========
Connect_To_Server()
Files_Load()
Texture_Obrabotka()
while GameRunned:
    FPSlimit.tick(FramePerSecond)
    #=====<Обработка нажатия клавиш>=====
    Check_Keys()
    #=====<Обработка событий>=====
    Events()
    #=====<мультиплеер>=====
    if MultiPlayer:
        Message = "<" + str(Player_Pos_x) + "," + str(round(Player_Pos_y)) + "," + str(Player_Anim_Count) + "," + str(Player_Looking_Away) + "," + Player_Name + ">"
        #=====<Отправка сообщений на сервер>=====
        if Message != Message_Old:
            Message_Old = Message
            client.send(Message.encode())
        #=====<Прием сообщений от сервера>=====
        data=client.recv(1024)
        data=data.decode()
        data = find(data)
#=====<Рисование игроков>=====
    if MultiPlayer and data!=['']:
        Draw_In_Window(data)
    else:
        Draw_In_Window(None)
    pygame.display.update()

pygame.quit()
