from pygame import *
import random
from time import time as timer
window = display.set_mode((700, 500))
clock = time.Clock()
mixer.init()

space = mixer.Sound("space.ogg")
space.play()
space.set_volume(0.2)
fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)
background = image.load("galaxy.jpg")
background = transform.scale(background, (700,500))

width = 700
height = 500
class Hero(sprite.Sprite):
    def __init__(self, x, y, width, height, speed, image_name="rocket.png"):
        super().__init__()

        self.image = image.load(image_name)
        self.image = transform.scale(self.image, (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
bullets = sprite.Group()



class Bulet(Hero):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y < -60:
            self.kill()  


             
class Player(Hero): 
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <620:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bulet(self.rect.centerx, self.rect.y , 10,10,10, "bullet.png")
        bullets.add(bullet)
counter = 0 
monster_kill = 0



class Enemy (Hero):
    def move(self):
        
        self.rect.y += self.speed
        global counter
        if self.rect.y >560:
            counter+=1
            self.rect.x = random.randint(100,565)
            self.speed = random.randint(1,4)
            self.rect.y = -100

class Asteroid(Hero):
    def move(self):
        self.rect.y += self.speed
        self.rect.x += self.speed
        if self.rect.y > 560 or self.rect.x > 750:
            self.rect.x = random.randint(-200,565)
            self.rect.y = -random.randint(50,150)


        


rocket1=Player(300, 340 , 80,130,5)


enemys = sprite.Group()

for i in range(5):
    Enemy1= Enemy(random.randint(100,565), -100, 100, 50, random.randint(1,4), "ufo.png" )
    enemys.add(Enemy1)
    
asteroids = sprite.Group()

for i in range(5):
    asteroid= Asteroid(random.randint(100,565), -100, 100, 50, random.randint(1,4), "asteroid.png" )
    asteroids.add(asteroid)

font.init()
font_win = font.Font(None, 60)
font_lose = font.Font(None, 60)

font1 = font.SysFont("Times New Romans", 30)
font2 = font.SysFont("Times New Romans", 30)
font3 = font.SysFont("Times New Romans", 30)
font4 = font.SysFont("Times New Romans", 30)
font5 = font.SysFont("Times New Romans", 30)
Game = True

finish = False


lifes = 3
killed = 0

num_bullets = 10

rel_time = False

while Game:
    for e in event.get():
        if e.type == QUIT:
            Game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bullets > 0 and rel_time is False:
                    num_bullets -= 1
                    rocket1.fire()

                if num_bullets == 0 and rel_time is False:
                    rel_time = True
                    last_time = timer()
                    fire_sound.play()

            if e.key == K_r:
                lifes = 3
                killed = 0
                counter = 0
                finish = False
                for i in enemys:
                    i.rect.y = -random.randint(50,200)
                    i.rect.x = random.randint(50, 565)
                for i in asteroids:
                    i.rect.y = -random.randint(50,200)
                    i.rect.x = random.randint(-200,200)

    window.blit(background, (0, 0))
   
    if finish!= True:

        rocket1.reset()
        rocket1.move()
        
        window.blit(font1.render(f"Лічильник: {counter}", True, (255,255,255)), (15,10))
        window.blit(font2.render(f"Збито: {killed}", True, (255,255,255)), (15,50))
        window.blit(font3.render(f"Життя: {lifes}", True, (255,255,255)), (15,90))
        

        for i in enemys:
            i.reset()
            i.move()

        for a in asteroids:
            a.reset()
            a.move()

        for b in bullets:
            b.reset()
            b.move()
    
        if counter >= 5:
            finish = True

        if rel_time is True:
            new_time = timer()
            if new_time - last_time < 3:
                reload_screen = font5.render("WAIT, RELOAD...", 1, (150, 0, 0))
                window.blit (reload_screen, (250, 460))
            else:
                num_bullets = 10
                rel_time = False


        list_collides = sprite.spritecollide(rocket1, enemys, False)       
        for collide in list_collides:
            if collide:
                lifes -= 1
                if lifes ==0:
                    finish = True
                for i in enemys:
                    i.rect.y = random.randint(50,200)
                    i.rect.x = random.randint(50, 565)
                    
    
        list_collides = sprite.groupcollide(enemys, bullets, True, False)
        for collide in list_collides:
            if collide:
                killed +=1
                if killed ==10:
                    finish = True
                Enemy1 = Enemy(random.randint(50,565), -100,100,30, random.randint(1,4), "ufo.png")
                enemys.add(Enemy1)

        list_collides = sprite.spritecollide(rocket1, asteroids, True)

        for collide in list_collides:
            if collide:
                lifes -=1
                asteroid = Asteroid(random.randint(-200, 200), -random.randint(50,150), 30,30,random.randint(1,3), "asteroid.png")
                asteroid.add(asteroids)

    if finish == True:
        if killed == 10:
            window.blit(font_win.render("YOU WIN", True, (0,255,0)), (width / 2 - 150, height / 2 - 50))
    
        if lifes == 0 or counter == 5:
            window.blit(font_lose.render("YOU LOSE", True, (255,0,0)), (width / 2 - 150, height / 2 - 50))
        
        

        window.blit(font1.render(f"Щоб почати спочатку нажміть R", True, (255,255,255)), (width / 2 - 150, height / 2 + 100))
       
    clock.tick(60)
    display.update()



# class GameSprite():
#     def __init__(self, img, speed, x, y):
#         self.img = transform.scale(image.load(img), (65, 65))
#         self.rect = self.img.get_rect()
#         self.speed = speed
#         self.rect.x = x
#         self.rect.y = y
#         self.move_right=False
#         self.move_left=False
#         self.move_up=False
#         self.move_down=False
#         self.direction="right"