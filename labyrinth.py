from pygame import *


window = display.set_mode((700, 500))
display.set_caption('Догонялки')
background = transform.scale(image.load('background.jpg'), (700, 500))



clock = time.Clock()
FPS = 60


mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()

speed = 10

game = True

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

        if key_pressed[K_d] and self.rect.x < 700 - 80 :
           self.rect.x += self.speed

        if key_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed

        if key_pressed[K_s] and self.rect.y < 500 - 80:
            self.rect.y += self.speed


class Ememy(GameSprite):
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= 700 - 85:
            self.direction = 'left'


        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, color_1,wall_x,  wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.width = wall_width
        self.heidht = wall_height

        self.image = Surface((wall_width, wall_height))
        self.image.fill(color_1)


        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




player = Player('hero.png', 5, 500 - 80, 4)
monster = Ememy('cyborg.png', 700 - 80, 280, 4)
final = GameSprite('treasure.png', 700 - 120, 500 - 80, 0)

w1 = Wall((154, 205, 50), 100, 20, 450, 10)
w2 = Wall((154, 205, 50), 100, 480, 350, 10)
w3 = Wall((154, 205, 50), 100, 20, 10, 380)
w4 = Wall((154, 205, 50), 200, 130, 10, 350)
w5 = Wall((154, 205, 50), 450, 130, 10, 360)
w6 = Wall((154, 205, 50), 300, 20, 10, 350)
w7 = Wall((154, 205, 50), 390, 120, 130, 10)

wall = [w1,w2,w3,w4,w5,w6,w7]
font.init()
font = font.Font(None, 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')
finish = False


while game: 
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish != True:
        window.blit(background,(0, 0))
        player.update()
        monster.update()
        player.reset()
        monster.reset()
        final.reset()
        for w in wall:
            w.draw_wall()
            if sprite.collide_rect(player, monster) or sprite.collide_rect(player, w):
                finish = True
                window.blit(lose, (200, 200))
                kick.play

        if sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    if key.get_pressed()[K_SPACE]:
        player.rect.x = 5
        player.rect.y = 500 - 80
        finish = False


    
    display.update()
    clock.tick(FPS)


