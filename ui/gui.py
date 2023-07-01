import os
from time import sleep

import pygame

from board.board import Board
from game import Game, GameError


class Gui:

    WIDTH, HEIGHT = 800, 704

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)

    FPS = 60
    DOUBLE_CLICK_TIME = 500

    LEFT = 1
    MIDDLE = 2
    RIGHT = 3

    MINE_IMAGE = pygame.image.load(os.path.join("assets", "mine.png"))
    FLAG_IMAGE = pygame.image.load(os.path.join("assets", "flag.png"))

    def __init__(self, game: Game):
        self.__game = game

        self.__cell_width = Gui.WIDTH // self.__game.number_of_columns
        self.__cell_height = Gui.HEIGHT // self.__game.number_of_rows

        Gui.MINE_IMAGE = pygame.transform.scale(Gui.MINE_IMAGE, (self.__cell_width, self.__cell_height))
        Gui.FLAG_IMAGE = pygame.transform.scale(Gui.FLAG_IMAGE, (self.__cell_width, self.__cell_height))

        pygame.init()

    def run_ui(self):
        window = pygame.display.set_mode((Gui.WIDTH, Gui.HEIGHT))
        pygame.display.set_caption("Minesweeper")
        pygame.display.set_icon(Gui.MINE_IMAGE)

        clock = pygame.time.Clock()
        double_click_timer = pygame.time.Clock()

        while True:
            clock.tick(Gui.FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(1)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # double click = reveal all neighbors
                    if event.button == Gui.LEFT and double_click_timer.tick() < Gui.DOUBLE_CLICK_TIME:
                        try:
                            self.__game.reveal_neighbors(event.pos[1] // self.__cell_height,
                                                         event.pos[0] // self.__cell_width)
                            if self.__game.is_game_over:
                                self.__game_over(window)

                        except GameError:
                            pass

                    # left click = reveal cell
                    if event.button == Gui.LEFT:
                        try:
                            self.__game.reveal(event.pos[1] // self.__cell_height,
                                               event.pos[0] // self.__cell_width)
                            if self.__game.is_game_over:
                                self.__game_over(window)

                        except GameError:
                            pass

                    # right click = flag cell / unflag cell
                    elif event.button == Gui.RIGHT:
                        try:
                            self.__game.flag(event.pos[1] // self.__cell_height,
                                             event.pos[0] // self.__cell_width)
                            if self.__game.is_game_over:
                                self.__game_over(window)

                        except GameError:
                            try:
                                self.__game.unflag(event.pos[1] // self.__cell_height,
                                                   event.pos[0] // self.__cell_width)
                            except GameError:
                                pass

            self.__draw_window(window)

    def __game_over(self, window: pygame.Surface):
        self.__draw_window(window)

        if self.__game.is_game_won:
            text = pygame.font.SysFont("Arial", 50).render("You Won!", True, Gui.BLACK)
        else:
            text = pygame.font.SysFont("Arial", 50).render("Game Over!", True, Gui.BLACK)

        sleep(0.7)
        window.fill(Gui.WHITE)
        window.blit(text, text.get_rect(center=(Gui.WIDTH // 2, Gui.HEIGHT // 2 - 50)))

        # new game button
        new_game_text = pygame.font.SysFont("Arial", 30).render("New Game", True, Gui.BLACK)
        new_game_button = pygame.Rect(Gui.WIDTH // 2 - 100, Gui.HEIGHT // 2, 200, 50)
        pygame.draw.rect(window, Gui.GRAY, new_game_button)
        window.blit(new_game_text, new_game_text.get_rect(center=new_game_button.center))

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(1)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == Gui.LEFT:
                        if new_game_button.collidepoint(event.pos):
                            board = Board(self.__game.number_of_rows, self.__game.number_of_columns,
                                          self.__game.number_of_mines)

                            self.__game = Game(board)
                            self.run_ui()

    # ----------------------------------------- #

    def __draw_window(self, window: pygame.Surface):
        window.fill(Gui.WHITE)
        self.__draw_board(window)
        pygame.display.update()

    def __draw_board(self, window: pygame.Surface):
        for cell in self.__game.cells:
            cell_rect = pygame.Rect(
                cell.column * self.__cell_width,
                cell.row * self.__cell_height,
                self.__cell_width,
                self.__cell_height
            )

            pygame.draw.rect(window, Gui.BLACK, cell_rect, 1)

            if cell.is_revealed:
                if cell.is_mine:
                    window.blit(Gui.MINE_IMAGE, cell_rect)

                else:
                    if cell.mine_neighbors > 0:
                        text = pygame.font.SysFont("Arial", 20).render(str(cell.mine_neighbors), True, Gui.BLACK)
                        window.blit(text, text.get_rect(center=cell_rect.center))
                    else:
                        pygame.draw.rect(window, Gui.GRAY, cell_rect)

            elif cell.is_flagged:
                window.blit(Gui.FLAG_IMAGE, cell_rect)
