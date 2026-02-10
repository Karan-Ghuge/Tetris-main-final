import pygame, sys
from game import Game
from colors import Colors

pygame.init()

WIDTH, HEIGHT = 500, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

# ---------- Fonts ----------
title_font = pygame.font.Font(None, 64)
label_font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

# ---------- Themes ----------
THEMES = {
    "Neon": {"bg": (20, 25, 45), "panel": (44, 44, 127),
             "button": (0, 200, 255), "hover": (0, 255, 255),
             "text": (255, 255, 255)},
    "Retro": {"bg": (15, 15, 15), "panel": (50, 20, 20),
              "button": (255, 128, 0), "hover": (255, 180, 80),
              "text": (255, 255, 0)},
    "Light": {"bg": (230, 230, 240), "panel": (200, 200, 220),
              "button": (120, 160, 255), "hover": (160, 200, 255),
              "text": (20, 20, 20)}
}
current_theme = "Neon"

# ---------- Button ----------
class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.hover = False

    def draw(self, surface, font, theme):
        bg = THEMES[theme]["hover"] if self.hover else THEMES[theme]["button"]
        txt_col = THEMES[theme]["text"]
        pygame.draw.rect(surface, bg, self.rect, border_radius=16)
        pygame.draw.rect(surface, txt_col, self.rect, 2, border_radius=16)
        txt = font.render(self.text, True, txt_col)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

    def update_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hover

# ---------- Dropdown ----------
class Dropdown:
    def __init__(self, rect, options, selected=0):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.selected = selected
        self.open = False

    def draw(self, surface, font, theme):
        bg = THEMES[theme]["button"]
        txt_col = THEMES[theme]["text"]

        # Main button
        pygame.draw.rect(surface, bg, self.rect, border_radius=12)
        pygame.draw.rect(surface, txt_col, self.rect, 2, border_radius=12)
        txt = font.render(self.options[self.selected], True, txt_col)
        surface.blit(txt, txt.get_rect(center=self.rect.center))

        # Dropdown options
        if self.open:
            for i, option in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x - self.rect.width,
                                       self.rect.y + (i+1)*self.rect.height,
                                       self.rect.width, self.rect.height)
                pygame.draw.rect(surface, bg, opt_rect, border_radius=12)
                pygame.draw.rect(surface, txt_col, opt_rect, 2, border_radius=12)
                txt = font.render(option, True, txt_col)
                surface.blit(txt, txt.get_rect(center=opt_rect.center))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                return None
            elif self.open:
                for i, option in enumerate(self.options):
                    opt_rect = pygame.Rect(self.rect.x - self.rect.width,
                                           self.rect.y + (i+1)*self.rect.height,
                                           self.rect.width, self.rect.height)
                    if opt_rect.collidepoint(event.pos):
                        self.selected = i
                        self.open = False
                        return option
                self.open = False
        return None

# ---------- Game State ----------
STATE_INTRO, STATE_PLAYING, STATE_LEVELS = 0, 1, 2
current_state = STATE_INTRO

game = Game()
paused = False

# Sidebar buttons
btn_pause = Button("Pause", (330, 100, 150, 40))
btn_resume = Button("Resume", (330, 150, 150, 40))
btn_exit = Button("Exit", (330, 200, 150, 40))
btn_level = Button("Levels", (330, 250, 150, 40))
mode_dropdown = Dropdown((330, 300, 150, 40), list(THEMES.keys()), 0)

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 600)

# ---------- Intro Page ----------
def intro_page():
    global current_state
    start_button = pygame.Rect(150, 500, 200, 60)

    while current_state == STATE_INTRO:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
                current_state = STATE_PLAYING

        screen.fill(THEMES[current_theme]["bg"])
        title = title_font.render("TETRIS", True, THEMES[current_theme]["button"])
        screen.blit(title, title.get_rect(center=(WIDTH//2, 100)))

        # Instructions
        panel = pygame.Rect(60, 180, WIDTH-120, 260)
        pygame.draw.rect(screen, THEMES[current_theme]["panel"], panel, border_radius=12)
        pygame.draw.rect(screen, THEMES[current_theme]["button"], panel, 2, border_radius=12)
        guide = [
            "← / → : Move block left/right",
            "↑ : Rotate block",
            "↓ : Soft drop (hold for faster)",
            "Space : Hard drop instantly",
            "P : Pause / Resume game",
            "Enter : Restart after Game Over",
            "Esc : Quit"
        ]
        y = 200
        for line in guide:
            txt = small_font.render(line, True, THEMES[current_theme]["text"])
            screen.blit(txt, (panel.x + 20, y))
            y += 35

        # Start button
        pygame.draw.rect(screen, THEMES[current_theme]["button"], start_button, border_radius=16)
        pygame.draw.rect(screen, THEMES[current_theme]["text"], start_button, 2, border_radius=16)
        txt = label_font.render("START GAME", True, THEMES[current_theme]["text"])
        screen.blit(txt, txt.get_rect(center=start_button.center))

        pygame.display.update()
        clock.tick(60)

# ---------- Sidebar ----------
def draw_sidebar():
    global current_theme
    mouse_pos = pygame.mouse.get_pos()
    for btn in [btn_pause, btn_resume, btn_exit, btn_level]:
        btn.update_hover(mouse_pos)
        btn.draw(screen, label_font, current_theme)

    # Dropdown
    mode_dropdown.draw(screen, small_font, current_theme)

    # Score/High/Level
    y = 380
    for label, val in [("Score", game.score), ("High", game.high_score), ("Level", game.level)]:
        pill = pygame.Rect(330, y, 150, 40)
        pygame.draw.rect(screen, THEMES[current_theme]["button"], pill, border_radius=16)
        pygame.draw.rect(screen, THEMES[current_theme]["text"], pill, 2, border_radius=16)
        txt = small_font.render(f"{label}: {val}", True, THEMES[current_theme]["text"])
        screen.blit(txt, txt.get_rect(center=pill.center))
        y += 50

# ---------- Levels Page ----------
def levels_page():
    global current_state
    back_button = pygame.Rect(150, 500, 200, 50)
    while current_state == STATE_LEVELS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                current_state = STATE_INTRO

        screen.fill(THEMES[current_theme]["bg"])
        title = title_font.render("Levels", True, THEMES[current_theme]["button"])
        screen.blit(title, title.get_rect(center=(WIDTH//2, 80)))

        levels = ["Level 1 (Unlocked)", "Level 2 (Locked)", "Level 3 (Locked)", "Level 4 (Locked)", "Level 5 (Locked)"]
        y = 180
        for i, level in enumerate(levels):
            col = THEMES[current_theme]["button"] if i == 0 else (150, 150, 150)
            txt = label_font.render(level, True, col)
            screen.blit(txt, (WIDTH // 2 - 100, y))
            y += 50

        # Back
        pygame.draw.rect(screen, THEMES[current_theme]["button"], back_button, border_radius=16)
        pygame.draw.rect(screen, THEMES[current_theme]["text"], back_button, 2, border_radius=16)
        txt = label_font.render("GO BACK", True, THEMES[current_theme]["text"])
        screen.blit(txt, txt.get_rect(center=back_button.center))

        pygame.display.update()
        clock.tick(60)

# ---------- Game Loop ----------
while True:
    if current_state == STATE_INTRO:
        intro_page()
        continue
    if current_state == STATE_LEVELS:
        levels_page()
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # Auto drop
        if event.type == GAME_UPDATE and not paused and not game.game_over:
            game.move_down()

        # Mouse controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn_pause.clicked(event): paused = True
            if btn_resume.clicked(event): paused = False
            if btn_exit.clicked(event):
                paused = False; game.reset(); current_state = STATE_INTRO
            if btn_level.clicked(event): current_state = STATE_LEVELS

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if not paused and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_SPACE:  # hard drop
                    while not game.game_over:
                        before = game.current_block.row_offset
                        game.move_down()
                        after = game.current_block.row_offset
                        if after == before:
                            break
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_RETURN and game.game_over:
                game.reset()

        # Mode dropdown
        mode_change = mode_dropdown.handle_event(event)
        if mode_change:
            current_theme = mode_change

    # Drawing
    screen.fill(THEMES[current_theme]["bg"])
    game.draw(screen)
    draw_sidebar()

    if game.game_over:
        over_txt = title_font.render("GAME OVER", True, THEMES[current_theme]["text"])
        screen.blit(over_txt, over_txt.get_rect(center=(200, 300)))

    pygame.display.update()
    clock.tick(60)
