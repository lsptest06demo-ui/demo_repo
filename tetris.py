#!/usr/bin/env python3
"""俄罗斯方块 - 使用 pygame 实现"""

import pygame
import random
import sys

# 常量
COLS = 10
ROWS = 20
CELL_SIZE = 30
SIDEBAR_WIDTH = 160
WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
HEIGHT = ROWS * CELL_SIZE
FPS = 60

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
GRID_COLOR = (50, 50, 50)

# 七种方块形状及颜色 (I, O, T, S, Z, J, L)
SHAPES = {
    "I": {
        "color": (0, 240, 240),
        "cells": [[(0, 1), (1, 1), (2, 1), (3, 1)]],
    },
    "O": {
        "color": (240, 240, 0),
        "cells": [[(0, 0), (1, 0), (0, 1), (1, 1)]],
    },
    "T": {
        "color": (160, 0, 240),
        "cells": [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ],
    },
    "S": {
        "color": (0, 240, 0),
        "cells": [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
        ],
    },
    "Z": {
        "color": (240, 0, 0),
        "cells": [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
        ],
    },
    "J": {
        "color": (0, 0, 240),
        "cells": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ],
    },
    "L": {
        "color": (240, 160, 0),
        "cells": [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
    },
}

SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}


class Piece:
    def __init__(self, shape_name=None):
        self.name = shape_name or random.choice(list(SHAPES.keys()))
        self.color = SHAPES[self.name]["color"]
        self.rotations = SHAPES[self.name]["cells"]
        self.rotation_index = 0
        self.x = COLS // 2 - 2
        self.y = 0

    @property
    def cells(self):
        return self.rotations[self.rotation_index % len(self.rotations)]

    def rotated_cells(self):
        return self.rotations[(self.rotation_index + 1) % len(self.rotations)]


class Tetris:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("俄罗斯方块")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20)
        self.big_font = pygame.font.SysFont("arial", 28, bold=True)
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.current = Piece()
        self.next_piece = Piece()
        self.fall_time = 0
        self.fall_speed = 500  # 毫秒

    def valid_position(self, cells, offset_x=0, offset_y=0):
        for cx, cy in cells:
            x = self.current.x + cx + offset_x
            y = self.current.y + cy + offset_y
            if x < 0 or x >= COLS or y >= ROWS:
                return False
            if y >= 0 and self.board[y][x] is not None:
                return False
        return True

    def lock_piece(self):
        for cx, cy in self.current.cells:
            x = self.current.x + cx
            y = self.current.y + cy
            if y < 0:
                self.game_over = True
                return
            self.board[y][x] = self.current.color

        cleared = self.clear_lines()
        if cleared:
            self.lines_cleared += cleared
            self.score += SCORE_TABLE.get(cleared, cleared * 200)
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(100, 500 - (self.level - 1) * 40)

        self.current = self.next_piece
        self.next_piece = Piece()
        if not self.valid_position(self.current.cells):
            self.game_over = True

    def clear_lines(self):
        full_rows = [
            row for row in range(ROWS) if all(self.board[row][col] is not None for col in range(COLS))
        ]
        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [None for _ in range(COLS)])
        return len(full_rows)

    def move(self, dx, dy):
        if self.valid_position(self.current.cells, dx, dy):
            self.current.x += dx
            self.current.y += dy
            return True
        return False

    def rotate(self):
        old_index = self.current.rotation_index
        self.current.rotation_index = (self.current.rotation_index + 1) % len(self.current.rotations)
        if not self.valid_position(self.current.cells):
            # 简单 wall kick：尝试左右偏移
            for kick in (-1, 1, -2, 2):
                if self.valid_position(self.current.cells, kick, 0):
                    self.current.x += kick
                    return
            self.current.rotation_index = old_index

    def hard_drop(self):
        while self.move(0, 1):
            self.score += 2

    def update(self, dt):
        if self.game_over:
            return
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.fall_time = 0
            if not self.move(0, 1):
                self.lock_piece()

    def draw_cell(self, x, y, color, offset_x=0, offset_y=0):
        rect = pygame.Rect(
            offset_x + x * CELL_SIZE + 1,
            offset_y + y * CELL_SIZE + 1,
            CELL_SIZE - 2,
            CELL_SIZE - 2,
        )
        pygame.draw.rect(self.screen, color, rect, border_radius=3)

    def draw_board(self):
        board_surface_x = 0
        for row in range(ROWS):
            for col in range(COLS):
                color = self.board[row][col]
                if color:
                    self.draw_cell(col, row, color, board_surface_x, 0)
                else:
                    rect = pygame.Rect(
                        board_surface_x + col * CELL_SIZE,
                        row * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    )
                    pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for cx, cy in piece.cells:
            self.draw_cell(piece.x + cx, piece.y + cy, piece.color, offset_x, offset_y)

    def draw_sidebar(self):
        sidebar_x = COLS * CELL_SIZE + 10
        labels = [
            ("分数", str(self.score)),
            ("等级", str(self.level)),
            ("消行", str(self.lines_cleared)),
        ]
        y = 20
        for title, value in labels:
            self.screen.blit(self.font.render(title, True, GRAY), (sidebar_x, y))
            self.screen.blit(self.big_font.render(value, True, WHITE), (sidebar_x, y + 22))
            y += 70

        self.screen.blit(self.font.render("下一个", True, GRAY), (sidebar_x, y))
        preview_x = sidebar_x
        preview_y = y + 30
        for cx, cy in self.next_piece.cells:
            self.draw_cell(cx, cy, self.next_piece.color, preview_x, preview_y)

        help_y = HEIGHT - 180
        help_lines = [
            "操作说明:",
            "← → 移动",
            "↑ 旋转",
            "↓ 软降",
            "空格 硬降",
            "R 重新开始",
            "Esc 退出",
        ]
        for i, line in enumerate(help_lines):
            self.screen.blit(self.font.render(line, True, GRAY), (sidebar_x, help_y + i * 22))

    def draw_game_over(self):
        overlay = pygame.Surface((COLS * CELL_SIZE, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        text = self.big_font.render("游戏结束", True, WHITE)
        rect = text.get_rect(center=(COLS * CELL_SIZE // 2, HEIGHT // 2 - 20))
        self.screen.blit(text, rect)
        hint = self.font.render("按 R 重新开始", True, GRAY)
        hint_rect = hint.get_rect(center=(COLS * CELL_SIZE // 2, HEIGHT // 2 + 20))
        self.screen.blit(hint, hint_rect)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_board()
        if not self.game_over:
            self.draw_piece(self.current)
        self.draw_sidebar()
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def handle_key(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if key == pygame.K_r:
            self.reset()
            return

        if self.game_over:
            return

        if key == pygame.K_LEFT:
            self.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.move(1, 0)
        elif key == pygame.K_DOWN:
            if self.move(0, 1):
                self.score += 1
        elif key == pygame.K_UP:
            self.rotate()
        elif key == pygame.K_SPACE:
            self.hard_drop()
            self.lock_piece()

    def run(self):
        while True:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.update(dt)
            self.draw()


def main():
    game = Tetris()
    game.run()


if __name__ == "__main__":
    main()
