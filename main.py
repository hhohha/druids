import pygame as pg
import config
import time
from board import cBoard

IMAGE_NAMES = ['base', 'empty', 'glasses', 'gold', 'sharp', 'strong', 'water', 'boots', 'fast', 'gloves', 'scroll', 'stone', 'tree']
IMAGES = {}

def main():
    pg.init()
    boardSizeX, boardSizeY = config.MAP_SIZE
    screen_size = (config.IMG_SIZE * boardSizeX, config.IMG_SIZE * boardSizeY)
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()
    pg.display.set_caption('Mystery of the druids')

    for name in IMAGE_NAMES:
        IMAGES[name] = pg.image.load('imgs/' + name + '.png').convert_alpha()

    board = cBoard(boardSizeX, boardSizeY)
    seed = round(time.time())
    print(f'map seed: {seed}')
    board.generate_map(seed)

    screen.fill(config.SCREEN_BKG_COLOR)

    while True:
        for event in pg.event.get():
            if event.type is pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    screen.fill(config.SCREEN_BKG_COLOR)
                    seed = round(time.time())
                    print(f'map seed: {seed}')
                    board.generate_map(seed)

        #for team in teams:
        #    team.make_move()

        for square in board.edited_squares():
            screen.blit(IMAGES[board.get_square(square.x, square.y)], (square.x * 32, square.y * 32))

        clock.tick(30)
        pg.display.flip()


if __name__ == '__main__':
    main()
