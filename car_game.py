# Thư viện
import pygame
from pygame.locals import *
import random
pygame.init()

# Màu nền
gray = (100,100,100)
green = (76,208,56)
yellow = (255,232,0)
red = (200,0,0)
white = (255,255,255)

# Tạo cửa sổ game
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Car Game")

# Khởi tạo biến
gameplay = False
speed = 2
score = 0

# Đường xe chạy
road_width = 300
street_width = 10
street_height = 50
# Lane
lane_left = 150
lane_center = 250
lane_right =350
lanes = [lane_left, lane_center, lane_right]
lane_move_y = 0

#Road và edge
road =(100,0,road_width,height)
left_edge = (95,0,street_width,height)
right_edge = (395,0,street_width,height)

#Vị trí ban đầu của xe người chơi
player_x = 250
player_y = 400
#Đối tượng xe lưu thông
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        #Scale images
        image_scale = 45/image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image,(new_width,new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image,x,y)
# sprite groups
player_group = pygame.sprite.Group()
Vehicle_group = pygame.sprite.Group()
# Tạo xe người chơi
player = PlayerVehicle(player_x, player_y)
player_group.add(player)
# Load xe lưu thông
image_name = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
Vehicle_images = []
for name in image_name:
    image = pygame.image.load('images/' + name)
    Vehicle_images.append(image)

# Cài đặt FPS
clock = pygame.time.Clock()
fps = 120

# Vòng lặp xử lý game
running = True
while running:
    # chỉnh fps
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # Điều khiển xe:
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > lane_left:
                player.rect.x -= 100
            if event.key == K_RIGHT and player.rect.center[0] < lane_right:
                player.rect.x += 100
    # Vẽ địa hình cỏ
    screen.fill(green)
    # Vẽ đường chạy
    pygame.draw.rect(screen,gray,road)
    # Vẽ Edge - lề đường
    pygame.draw.rect(screen,yellow,left_edge)
    pygame.draw.rect(screen,yellow,right_edge)
    # Vẽ lane đường
    lane_move_y += speed*2
    if lane_move_y >= street_height*2:
        lane_move_y = 0
    for y in range(street_height* -2, height, street_height*2):
        pygame.draw.rect(screen,white,(lane_left + 45, y + lane_move_y, street_width, street_height))
        pygame.draw.rect(screen,white,(lane_center + 45, y + lane_move_y, street_width, street_height))
    # Vẽ xe Player
    player_group.draw(screen)
    # Vẽ phương tiện giao thông
    if len(Vehicle_group) < 2:
        add_vehicle = True
        for vehicle in Vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(Vehicle_images)
            vehicle = Vehicle(image, lane,height / -2)
            Vehicle_group.add(vehicle)
    # Cho xe lưu thông
    for vehicle in Vehicle_group:
        vehicle.rect.y += speed
        
        # remove vehicle
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            # Tăng độ khó cho game
            if score > 0 and score % 20 == 0:
                speed += 1
    # Vẽ nhóm xe
    Vehicle_group.draw(screen)
    pygame.display.update()
pygame.display.quit()