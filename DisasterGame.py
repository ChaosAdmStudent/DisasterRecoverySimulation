import pygame 
from pygame import display 
from time import sleep 
import os
import bankSystem
import Disaster
import pymysql 

from pygame.constants import MOUSEBUTTONDOWN 

pygame.font.init() 

# Global Variables 
WIDTH,HEIGHT = 900, 500 
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
COLOR = (250, 95, 85)
FPS = 60 
SV_IMG_WIDTH, SV_IMG_HEIGHT = (100,195)
BACKUP_SERVER_IMAGE = pygame.image.load(os.path.join('images', 'alt_backup.png'))
BACKUP_SERVER_IMAGE = pygame.transform.scale(BACKUP_SERVER_IMAGE, (SV_IMG_WIDTH,SV_IMG_HEIGHT))
MAIN_SERVER_IMAGE = pygame.image.load(os.path.join('images', 'alt_main.png'))
MAIN_SERVER_IMAGE = pygame.transform.scale(MAIN_SERVER_IMAGE, (SV_IMG_WIDTH,SV_IMG_HEIGHT))
TRUCK_IMAGE = pygame.image.load(os.path.join('images','truck.png'))
TRUCK_IMAGE = pygame.transform.scale(TRUCK_IMAGE, (100,100))

TRUCK_START = (250, 250) 
TRUCK_END = (500,250)
TRUCK_DIM = (100,100) 
TRUCK_CURRENT = (250,250)

TEXT_FONT = pygame.font.SysFont('comicsans', 20)
DB_FONT = pygame.font.SysFont('comicsans', 14) 
WHITE = (255,255,255)
BLACK = (0,0,0)
HOVER_COLOR = () 
CLICK_COLOR = () 

pygame.display.set_caption('DRP Simulation for Timestamping') 

class Box(pygame.sprite.Sprite): 

    def __init__(self,x,y): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface((125,50)) 
        self.image.fill(BLACK) 
        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
    
    def update(self): 
        self.image.fill(BLACK)

class DBBox(pygame.sprite.Sprite): 

    def __init__(self,x,y): 
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.Surface((75,50)) 
        self.image.fill(BLACK) 
        self.rect = self.image.get_rect() 
        self.rect.x = x 
        self.rect.y = y 
    
    def update(self): 
        self.image.fill(BLACK)

def draw_window(truck): 
    WIN.fill(COLOR) 
    WIN.blit(BACKUP_SERVER_IMAGE, (150, 150)) 
    WIN.blit(MAIN_SERVER_IMAGE, (600, 150)) 
    WIN.blit(TRUCK_IMAGE, (truck.x, truck.y)) 

def draw_text(): 

    backup_text = TEXT_FONT.render('Backup Data', 1, WHITE) 
    recover_text = TEXT_FONT.render('Recover Data', 1, WHITE) 
    db_text = TEXT_FONT.render('Show Databases', 1, WHITE)  

    main_text = TEXT_FONT.render('Main Server', 1, WHITE) 
    alt_text = TEXT_FONT.render('Backup Server', 1, WHITE)  

    earthquake_text = TEXT_FONT.render('Earthquake', 1, WHITE) 
    info_breach_text = TEXT_FONT.render('Info Breach', 1, WHITE) 

    WIN.blit(backup_text, (140,380)) 
    WIN.blit(recover_text, (590, 380))
    WIN.blit(db_text, (350, 380))
    WIN.blit(main_text, (140,100)) 
    WIN.blit(alt_text, (590, 100))
    WIN.blit(earthquake_text, (5,5)) 
    WIN.blit(info_breach_text, (WIDTH-120, 5))

def draw_boxes(): 
    boxes = pygame.sprite.Group() 
    box1 = Box(140,380) 
    box2 = Box(590,380) 
    box3 = Box(350, 380)
    box4 = Box(5,5) 
    box5 = Box(WIDTH -120, 5)

    boxes.add(box1) 
    boxes.add(box2)
    boxes.add(box3)
    boxes.add(box4) 
    boxes.add(box5)
    
    return boxes  

def draw_dbboxes(): 
    boxes = pygame.sprite.Group()
    box1 = Box(WIDTH - 150, 40) 
    boxes.add(box1) 

    return boxes

def draw_dbtext(): 
    back_text = TEXT_FONT.render('BACK', 1, WHITE)  
    WIN.blit(back_text, (WIDTH-150,50)) 

    main_server = TEXT_FONT.render('MAIN SERVER', 1, WHITE)  
    WIN.blit(main_server, (150,150)) 

    backup_server = TEXT_FONT.render('BACKUP SERVER', 1, WHITE)  
    WIN.blit(backup_server, (550,150)) 


def draw_servers(): 
    conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='db')
    cursor1 = conn1.cursor()  
    conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb') 
    cursor2 = conn2.cursor() 

    bankClient = bankSystem.Bank(conn1, cursor1, 'mainbank')
    backupClient = bankSystem.Bank(conn2, cursor2, 'backupbank')

    main_server_text = bankClient.get_database().split('\n')
    backup_server_text = backupClient.get_database().split('\n') 

    for i,line in enumerate(main_server_text): 
        main_server_db = DB_FONT.render(line, 1, WHITE)  
        WIN.blit(main_server_db, (100,200 + 20*i)) 

    for i,line in enumerate(backup_server_text):
        backup_server_db = DB_FONT.render(line, 1, WHITE)  
        WIN.blit(backup_server_db, (500,200 + 20*i)) 
    
    conn1.close() 
    conn2.close()

def draw_dbbackground(): 
    WIN.fill(COLOR)

def truck_backup(truck): 
        conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='db')
        cursor1 = conn1.cursor()  
        conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb') 
        cursor2 = conn2.cursor() 

        
        status = 'backup'
        if truck.x != TRUCK_END[0]:
            truck.x += 1

        else: 
            disasterClient = Disaster.Disaster(conn1, conn2, cursor1, cursor2) 
            disasterClient.backup('copy')
            print('Data successfully backed up!') 
            status = 'stay' 
        
        conn1.commit()
        conn2.commit() 
        conn1.close() 
        conn2.close()

        return status

def truck_right(truck): 
    if truck.x != TRUCK_END[0]: 
        truck.x += 1

def truck_recover(truck): 
        conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='db')
        cursor1 = conn1.cursor()  
        conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb') 
        cursor2 = conn2.cursor() 
        
        status = 'recover'
        if truck.x != TRUCK_START[0]:
            truck.x -= 1
        
        else: 
            disasterClient = Disaster.Disaster(conn1, conn2, cursor1, cursor2)
            disasterClient.recover()
            print('Data successfully recovered!')  
            status = 'stay' 

        conn1.commit()
        conn2.commit() 
        conn1.close() 
        conn2.close()

        return status

def simulate_earthquake(): 
    conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='db')
    cursor1 = conn1.cursor()  
    conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb') 
    cursor2 = conn2.cursor() 

    disasterClient = Disaster.Disaster(conn1, conn2, cursor1, cursor2) 
    disasterClient.simulate_earthquake('high')

    cursor1.close() 
    cursor2.close() 
    conn1.commit() 
    conn2.commit() 
    conn1.close() 
    conn2.close() 

def simulate_info_breach(): 
    conn1 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='db')
    cursor1 = conn1.cursor()  
    conn2 = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='Lakshyavit_12', db='backupdb') 
    cursor2 = conn2.cursor() 

    disasterClient = Disaster.Disaster(conn1, conn2, cursor1, cursor2) 
    disasterClient.simulate_breach(2)

    cursor1.close() 
    cursor2.close() 
    conn1.commit() 
    conn2.commit() 
    conn1.close() 
    conn2.close() 

def db_page(current_x, current_y): 

    boxes = draw_dbboxes() 
    clock = pygame.time.Clock() 
    running = 'db'
    while running == 'db': 
        clock.tick(FPS) 

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                print('Hope you liked the DRP Simulation!') 
                running = False
            
            if event.type == MOUSEBUTTONDOWN: 
                
                pos = pygame.mouse.get_pos() 
                for box in boxes: 
                    if box.rect.collidepoint(pos): 
                        if  WIDTH - 160<=pos[0] <= WIDTH - 10: 
                                print('Going back to main page!')
                                running = 'main'

        draw_dbbackground() 
        boxes.draw(WIN)
        draw_servers()
        draw_dbtext() 

        pygame.display.update()
    
    if running == 'main': 
        main(current_x, current_y) 
        
def main(current_x = TRUCK_START[0], current_y = TRUCK_START[1]): 
    
    truck = pygame.Rect(current_x, current_y, TRUCK_DIM[0], TRUCK_DIM[1])
    truck_status = 'stay'
    truck_move = 'stay'
    boxes = draw_boxes()
    
    
    clock = pygame.time.Clock() 
    running = 'main'
    while running == 'main': 
        clock.tick(FPS)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                print('Hope you liked the DRP Simulation!') 
                running = False 
            
            
            # Checking if user chose to recover/backup
            if event.type == MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos() 
                for box in boxes: 
                    if box.rect.collidepoint(pos): 
                        if  130<=pos[0]<=280:
                            if truck.x != TRUCK_START[0]: 
                                print('Backup already going on or failure!') 
                            else: 
                                print('Backup started!') 
                                truck_status = 'backup'  
                                current_x = TRUCK_END[0] 
                                current_y = TRUCK_END[1]
                        
                        if  580<=pos[0]<=720: 
                            if truck.x != TRUCK_END[0]: 
                                print('Recovery already going on or failure!') 
                            else: 
                                print('Recovering started!') 
                                truck_status = 'recover'
                                current_x = TRUCK_START[0] 
                                current_y = TRUCK_START[1]
                        
                        if  340<=pos[0]<=430: 
                            print('Now Displaying: Databases')
                            running = 'db'

                        if 0 <=pos[0] <= 90: 
                            simulate_earthquake() 
                            truck_move = 'right' 
                            current_x = TRUCK_END[0] 
                            current_y = TRUCK_END[1]
                        
                        if  WIDTH - 130 <= pos[0] <= WIDTH: 
                            simulate_info_breach() 
                            
        if truck_status == 'backup': 
            truck_status = truck_backup(truck) 

        if truck_status == 'recover': 
            truck_status = truck_recover(truck) 

        if truck_move == 'right': 
            truck_right(truck)

        draw_window(truck) 
        boxes.draw(WIN)
        draw_text() 
        pygame.display.update()
    
    if running == 'db': 
        db_page(current_x, current_y)

if __name__ == '__main__':
    main()  