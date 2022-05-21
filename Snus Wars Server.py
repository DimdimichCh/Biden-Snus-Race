import socket
import time
import pygame
import random
pygame.init()
#=====<Переменные>=====
Window_Width = 1280
Window_Height = 720
Window_Decrease = 3
FramePerSecond = 60
ServerRunned = True
players = []
image_fon = pygame.image.load("images/fon.jpg")
image_fon = pygame.transform.scale(image_fon, (Window_Width, Window_Height))
#=====<Создание и настройка сервера>=====
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
server.bind(("localhost", 8889))
server.setblocking(0)#
server.listen(5)
#=====<Создание и настройка пайгейм>=====
Window = pygame.display.set_mode((Window_Width//Window_Decrease, Window_Height//Window_Decrease))
FPSlimit = pygame.time.Clock()
#=====<Классы и дефайны>=====
def find (s):
    otcr = None
    for i in range(len(s)):
        if s[i] == "<":
            otcr=i
        if s[i] == ">" and otcr != None:
            zacr=i
            res = s[otcr+1:zacr]
            res = list(map(str, res.split(",")))
            return res
    return ""
class Player ():
    def __init__(self, connection, address, pos_x, pos_y, width, height, AnimCount, Looking_Away, name):
        self.connection = connection
        self.address = address
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.AnimCount = AnimCount
        self.Looking_Away = Looking_Away
        self.name = name
        self.errors = 0
    def update(self,data):
        self.pos_x = float(data[0])
        self.pos_y = float(data[1])
        self.AnimCount = int(data[2])
        self.Looking_Away = int(data[3])
        self.name = data[4]
#==========
print("Сервер запущен!")
#=====<Цикл сервера>=====
while ServerRunned:
    FPSlimit.tick(FramePerSecond)
    Window.fill((0,0,0))
#=====<Добавление клиента в список>=====
    try:
        new_socket, addr=server.accept()
        print(f"Игрок {addr} подключился")
        new_socket.setblocking(0)
        new_player = Player(new_socket, addr, -100, -100, 70, 100, 0, 0, 'None')
        players.append(new_player)
    except:
        pass
#=====<Получение информации от клиента>=====
    for player in players:
        try:
            data=player.connection.recv(1024)
            data=data.decode()
            data=find(data)
            player.update(data)
        except:
            pass
    player_data = [[] for i in range(len(players))]#=====<Создание списка в котором хранятся списки с информацией игроков>=====
    #=====<Формирование ответа игроку>=====
    otvets=['' for i in range(len(players))]
    for i in range(len(players)):
        player_x = str(players[i].pos_x)
        player_y = str(players[i].pos_y)
        player_width = str(players[i].width)
        player_height = str(players[i].height)
        player_Anim_Count = str(players[i].AnimCount)
        player_Looking_Away = str(players[i].Looking_Away)
        player_name = str(players[i].name)
        player_data[i]= [player_x+' '+player_y+' '+player_width+' '+player_height+' '+player_Anim_Count+' '+player_Looking_Away+' '+player_name] + player_data[i]
        otvets[i]=(f"<{','.join(player_data[i])}>")
#=====<Отправка информации на клиент>=====
    for i in range(len(players)):
        try:
            players[i].connection.send(str(otvets).encode())
            players[i].errors = 0
        except:
            try:#=====<Отключение игрока от сервера если клинт не отвечает>=====
                players[i].errors += 1
                if players[i].errors == 250:
                    print(f"Игрок {players[i].name}{players[i].address} отключился")
                    players[i].connection.close()
                    players.remove(players[i])
            except:
                pass
#=====<Отображение игроков>=====
    for player in players:
        x=round(player.pos_x//Window_Decrease)
        y=round(player.pos_y//Window_Decrease)
        pygame.draw.rect(Window, (255, 255, 0), ((x, y), (player.width//Window_Decrease, player.height//Window_Decrease)))
#=====<Обработка нажатия клавиш>=====
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
                ServerRunned = False

#=====<Обновление окна игры>=====
    pygame.display.update()
pygame.quit()
server.close()
