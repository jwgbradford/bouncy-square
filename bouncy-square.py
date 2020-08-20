import pygame as pg
from sys import exit
from random import randrange
vec = pg.math.Vector2

# set our constants
TITLE = 'Bouncy Square'
HEIGHT = 700
WIDTH = 500
FPS = 60
FONT_NAME = 'arial'
WHITE = (255, 255, 255)

# define colors
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BGCOLOR = (0, 155, 155)

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 40, WIDTH, 40),
                (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
                (125, HEIGHT - 350, 100, 20),
                (350, 200, 100, 20),
                (175, 100, 50, 20)]
# Player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.player = pg.sprite.Group()
        p = Player()
        self.player.add(p)
        self.platforms = pg.sprite.Group()
        self.show_start_screen()

    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
        self.player.update(self.platforms)
        for p in self.player:
            if p.rect.top <= HEIGHT / 4:
                p.pos.y += abs(p.vel.y)
                for plat in self.platforms:
                    plat.rect.y += abs(p.vel.y)
                    if plat.rect.top >= HEIGHT:
                        plat.kill()
                        self.score += 10
            elif p.rect.bottom > HEIGHT:
                for plat in self.platforms:
                    plat.rect.y -= max(p.vel.y, 10)
                    if plat.rect.bottom < 0:
                        plat.kill()
                if len(self.platforms) == 0:
                    self.game_over()
        while len(self.platforms) < 6:
            width = randrange(50, 100)
            p = Platform(randrange(0, WIDTH - width),
                        randrange(-75, -30),
                        width, 20)
            self.platforms.add(p)

    def game_over(self):
        self.screen.fill(BGCOLOR)
        self.text_to_image("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.text_to_image("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.text_to_image("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_any_key()

    def text_to_image(self, text, size, color, x, y):
        font = pg.font.SysFont(FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_any_key(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit_game()
                if event.type == pg.KEYUP:
                    self.reset()
                    return

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.text_to_image(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.text_to_image("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.text_to_image("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_any_key()

    def quit_game(self):
        pg.quit()
        exit()

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.platforms.draw(self.screen)
        self.player.draw(self.screen)
        pg.display.flip()

    def reset(self):
        self.score = 0
        self.platforms.empty()
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.platforms.add(p)
        for p in self.player:
            p.reset()

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.accel = vec(0,0)
        
    def update(self, platforms):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.accel.x += PLAYER_ACC
        elif keys[pg.K_LEFT]:
            self.accel.x -= PLAYER_ACC
        if keys[pg.K_SPACE]:
            self.jump(platforms)
        self.accel.x += self.vel.x * PLAYER_FRICTION
        self.accel.y = PLAYER_GRAV
        self.vel += self.accel
        self.pos += self.vel
        self.rect.midbottom = self.pos
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self, platforms, False)
            if hits:
                self.pos.y = hits[0].rect.top
                self.vel.y = 0
        self.accel.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

    def jump(self, platforms):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

if __name__ == "__main__":
    my_game = Game()
    my_game.run()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
