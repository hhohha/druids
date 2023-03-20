import pygame as pg
import config
import time
from board import Board, Square, Pos
from game import Game


# TODOs
#  - different colors for teams
#  - display info on the side
#  - implement reasonable strategies
#  - implement modular strategies
#  - continue improving typings
#  - press to step
#  - change speed
#  - unplug map
#  - record history
#  - coalitions


IMAGE_NAMES = ['empty', 'base', 'sharp', 'strong', 'fast', 'glasses', 'gloves', 'boots', 'gold', 'water', 'tree', 'stone', 'scroll']
IMAGES = {}

def main():
    pg.init()
    boardSizeX, boardSizeY = config.MAP_SIZE
    screen_size = (config.IMG_SIZE * boardSizeX + 300, config.IMG_SIZE * boardSizeY)
    screen = pg.display.set_mode(screen_size)
    clock = pg.time.Clock()
    pg.display.set_caption('Mystery of the druids')

    for idx, name in zip(Square, IMAGE_NAMES):
        IMAGES[idx] = pg.image.load('imgs/' + name + '.png').convert_alpha()

    board = Board(Pos(boardSizeX, boardSizeY))
    seed = round(time.time()*100)
    print(f'map seed: {seed}')
    board.generate_map(seed)
    print(f'map done')

    screen.fill(config.SCREEN_BKG_COLOR)
    game = Game(board, config.TEAM_CNT)
    font = pg.font.Font('freesansbold.ttf', 32)
    step = 0

    while True:
        for event in pg.event.get():
            if event.type is pg.QUIT:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    screen.fill(config.SCREEN_BKG_COLOR)
                    seed = round(time.time()*100)
                    print(f'map seed: {seed}')
                    board.generate_map(seed)
                    print(f'map done')
                elif event.key == pg.K_s:
                    if game.running:
                        game.pause()
                    else:
                        game.run()

        if game.running:
            game.step()
            step += 1

        for square in board.edited_squares():
            pg.draw.rect(screen, config.SCREEN_BKG_COLOR, pg.Rect(square.x * 32, square.y * 32, 32, 32))
            screen.blit(IMAGES[board.get_square(square)], (square.x * 32, square.y * 32))  # TODO - blits instead of blit

        for (color, agentType), pos in board.characterSquares.items():
            screen.blit(IMAGES[agentType.value], (pos.x * 32, pos.y * 32))

        text = font.render('Step ' + str(step), True, (0, 255, 0), (0, 0, 128))
        screen.blit(text, (config.IMG_SIZE * boardSizeX + 25, config.IMG_SIZE * boardSizeY / 2))


        clock.tick(3)
        pg.display.flip() # TODO - update instead of flip


if __name__ == '__main__':
    main()