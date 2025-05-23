from pygame import *
from random import randint

#background music
mixer.init()
mixer.music.load('musicbg.mp3')
mixer.music.play()
fire_sound = mixer.Sound('soundeffect.ogg')

#fonts and labels
font.init()
font2 = font.Font(None, 36)

font1 = font.Font(None, 80)
win = font1.render("YOU WIN!", True, (154, 104, 231))
lose = font1.render("YOU LOSE!", True, (197, 23, 46))

#image
img_back = "bg.png"
img_hero = "klee.png"
img_enemy = "hydro_enemy.png" #enemy

#1
img_bullet = "bomb.png"

score = 0
lost = 0

#2
max_lost = 3
goal = 10

class GameSprite(sprite.Sprite):
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       sprite.Sprite.__init__(self)

       self.image = transform.scale(image.load(player_image), (size_x, size_y))   
       self.speed = player_speed * 0.3333
       #to slow/speed up sprites, just multiply the self.speed

       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
  #method to control the sprite with arrow keys
  def update(self):
      keys = key.get_pressed()
      if keys[K_LEFT] and self.rect.x > 5:
          self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < win_width - 80:
          self.rect.x += self.speed
         
  #5
  def fire(self):
      bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
      bullets.add(bullet)

class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost

       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1


#3
class Bullet(GameSprite):
   def update(self):
       self.rect.y += self.speed

       if self.rect.y < 0:
           self.kill()
  


#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter Game!")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

#4
bullets = sprite.Group()

finish = False

#Main loop
run = True
while run:
   for e in event.get():
       if e.type == QUIT:
           run = False
      
       #6
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
  
   if not finish:
       window.blit(background, (0,0))


       text = font2.render("Score: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))


       text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))


       ship.update()
       monsters.update()
       bullets.update()


       ship.reset()
       monsters.draw(window)
       bullets.draw(window)


       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
           monsters.add(monster)


       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
           finish = True
           window.blit(lose, (200, 200))


       if score >= goal:
           finish = True
           window.blit(win, (200, 200))


       display.update()
   time.delay(50)