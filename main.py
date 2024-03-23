from pygame import *
import random
window = display.set_mode((700, 500))
clock = time.Clock()
mixer.init()

space = mixer.Sound("space.ogg")
space.play()
background = image.load("galaxy.jpg")
background = transform.scale(background, (700,500))

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




        


rocket1=Player(300, 340 , 80,130,5)


enemys = sprite.Group()

for i in range(5):
    Enemy1= Enemy(random.randint(100,565), -100, 100, 50, random.randint(1,4), "ufo.png" )
    enemys.add(Enemy1)


font.init()

font1 = font.Font(None, 50)
font2 = font.Font(None, 50)
font3 = font.Font(None, 50)
font4 = font.Font(None, 50)
Game = True

finish = False


lifes = 3

while Game:
    for e in event.get():
        if e.type == QUIT:
            Game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket1.fire()

    window.blit(background, (0, 0))
    killed = 0
    if finish!= True:

        rocket1.reset()
        rocket1.move()
        
        window.blit(font1.render(f"Лічильник: {counter}", True, (255,255,255)), (15,10))
        window.blit(font2.render(f"Збито: {monster_kill}", True, (255,255,255)), (15,50))
        window.blit(font3.render(f"Життя: {lifes}", True, (255,255,255)), (15,90))
        window.blit(font4.render(f"Збитих ворогів: {killed}", True, (255,255,255)), (15,130))

        for i in enemys:
            i.reset()
            i.move()



        for b in bullets:
            b.reset()
            b.move()
    
        list_collides = sprite.spritecollide(rocket1, enemys, False)       
        for collide in list_collides:
            if collide:
                lifes -= 1
                for i in enemys:
                    i.rect.y = -100
                    if lifes == 0:
                        finish = True
                        i.rect.y = -100
                        i.rect.x = random.randint(50, 565)
    
        list_collides = sprite.groupcollide(enemys, bullets, True, False)
        for collide in list_collides:
            if collide:
                killed +=1
                Enemy1 = Enemy(random.randint(50,565), -100,100,30, random.randint(1,4), "ufo.png")
                enemys.add(Enemy1)


                


        

       
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