#Создай собственный Шутер!
from random import randint
from turtle import screensize
from pygame import *
from time import time as get_time
FPS = 60
SPRITE_SIZE = 65
SCREEN_SIZE = (1250, 800)
WHITE = (255, 255, 255)
font.init()


def show_text(x, y, text, color, fsize = 50):
    
    label = font.Font(None, fsize).render(text, True, color)
    window.blit(label, (x, y))

class Counter:
    def __init__(self, x, y, text, font_size=40):
        self.pos = (x,y)
        self.text = text
        self.count = 0
        self.font = font.SysFont('Arial', font_size)
    
    def render(self):
        self.image = self.font.render(self.text + str(self.count), True, WHITE)

    def show(self):
        window.blit(self.image, self.pos)

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, image_name, speed, scale):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (SPRITE_SIZE // scale, SPRITE_SIZE // scale))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, image_name, speed, scale):
        super().__init__(x, y, image_name, speed, scale)
        self.rect.y = SCREEN_SIZE[1] - self.rect.height - 5
        self.last_shoot_time =  0
        self.amount_bullets = 20
        self.lives = 3
        self.img_live = transform.scale(image.load(image_name), (SPRITE_SIZE // (scale*2), SPRITE_SIZE // (scale*2)))
    def move(self):
        pressed = key.get_pressed()
        if pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if pressed[K_d] and self.rect.x < SCREEN_SIZE[0] - self.rect.width:
            self.rect.x += self.speed
        if pressed[K_SPACE] and self.amount_bullets > 0:
            if get_time() - self.last_shoot_time > 0.2:
                self.shoot()
                self.last_shoot_time = get_time()
                self.amount_bullets -= 1
    
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        show_text(SCREEN_SIZE[0]-200, 15, f'Осталось пуль: {self.amount_bullets}', WHITE, 30)
        for i in range(self.lives):
            x = SCREEN_SIZE[0] - 20 - self.img_live.get_width()
            x -= i * (10 + self.img_live.get_width())
            y = 40
            window.blit(self.img_live, (x,y))
    def shoot(self):
        bullet1 = Bullet(self.rect.x, self.rect.y, 'bullet.png', 5, 4)
        bullet1.rect.x += int(1.5 *  bullet1.rect.width)
        bullets.add(bullet1)
        mixer.Sound('fire.ogg').play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            missed_count.count += 1
            missed_count.render()
        self.show()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)


window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')
#fanta spritekii
player = Player(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] - SPRITE_SIZE-5, 'unnamed.jpg', 6, 0.5)
enemies = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
for _ in range(5):
    enemies.add(Enemy(randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 'avatars-NAvMUoLS7pWdi8wO-phyP3Q-t500x500.jpg', randint(1, 2), 0.6))
for _ in range(2):
    asteroids.add(Enemy(randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, 'bazacopy.jpeg', randint(1, 2), 0.6))
missed_count = Counter(10, 50, 'кол-во опЛОХностей: ')
missed_count.render()
killed_count = Counter(10, 100, 'кол-во обМОЛОДЕЦностей: ' )
killed_count.render()
#fon sceny
bg = transform.scale(image.load('galaxy.jpg'), SCREEN_SIZE)


#muzyka
mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.1)
mixer.music.play()

clock = time.Clock()
#igrovoy cykl
game = True
finish = False

while game:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(bg, (0, 0))
        player.show()
        player.move()
        enemies.update()
        asteroids.update()

        missed_count.show()
        killed_count.show()

        bullets.update()
        bullets.draw(window)

        sprites_list = sprite.groupcollide(enemies, bullets, False, True)
        for s in sprites_list:
            s.rect.y = 0
            s.rect.x = randint(0, SCREEN_SIZE[1] - SPRITE_SIZE)
            killed_count.count += 1
            killed_count.render()
        if killed_count.count >= 10:
            finish = True
            show_text(300, 200, 'МАЛАДЭЦ ПАРТИЯ ГОРДИТСЬСО ТАБОЙ', WHITE)
        for s in sprite.spritecollide(player, enemies, False) + sprite.spritecollide(player, asteroids, False):
            s.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            s.rect.y = -SPRITE_SIZE
            player.lives -= 1
            if isinstance(s, Enemy):
                killed_count.count += 1
                killed_count.render()
        if player.lives <= 0:   
            finish = True
            show_text(300, 200, 'YOU LOSE!', WHITE)
        display.update()