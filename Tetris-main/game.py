from grid import Grid
from blocks import *
import random
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.rows_cleared_last = 0

    # ---------- Score + Levels ----------
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1: self.score += 100
        if lines_cleared == 2: self.score += 200
        if lines_cleared == 3: self.score += 500
        if lines_cleared == 4: self.score += 1000
        self.score += move_down_points

        # High score update
        if self.score > self.high_score:
            self.high_score = self.score

        # Level increases every 500 points
        self.level = 1 + (self.score // 500)

    # ---------- Block Handling ----------
    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside() or not self.block_fits():
            self.current_block.undo_rotation()

    # ---------- Lock + Clear ----------
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for pos in tiles:
            if not self.grid.is_inside(pos.row, pos.column):
                self.game_over = True
                return
            self.grid.grid[pos.row][pos.column] = self.current_block.id

        self.current_block = self.next_block
        self.next_block = self.get_random_block()

        rows_cleared = self.grid.clear_full_rows()
        self.rows_cleared_last = rows_cleared
        self.update_score(rows_cleared, 0)

        if not self.block_fits():
            self.game_over = True

    # ---------- Checks ----------
    def block_inside(self):
        for tile in self.current_block.get_cell_positions():
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def block_fits(self):
        for tile in self.current_block.get_cell_positions():
            if not self.grid.is_empty(tile.row, tile.column):
                return False
        return True

    # ---------- Reset ----------
    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
        self.level = 1
        self.rows_cleared_last = 0
        self.game_over = False

    # ---------- Draw ----------
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)
