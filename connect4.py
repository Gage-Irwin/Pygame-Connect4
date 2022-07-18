import pygame
pygame.font.init()

# Game settings
CONNECT = 4
BOARD_WIDTH = 7
BOARD_HIGHT = 6

NODE_SIZE = 100
RADIUS_SIZE = NODE_SIZE//2 - 5
WIDTH = BOARD_WIDTH*NODE_SIZE
HEIGHT = BOARD_HIGHT*NODE_SIZE
pygame.display.set_caption("connect4")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60
TEXT_FONT = pygame.font.SysFont('comicsans', 60)
TEXT_FONT_2 = pygame.font.SysFont('comicsans', 30)

END_SCREEN = pygame.Rect(NODE_SIZE, NODE_SIZE+NODE_SIZE/2, 5*NODE_SIZE, 2*NODE_SIZE)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0 , 0)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
GREY = (169, 169, 169)
DARK_BROWN = (179,133,100)
LIGHT_BROWN = (210,179,140)

class Node():

    def __init__(self, x, y, piece = None):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE)
        self.piece = piece
        self.clicked = False
        self.ghost = False

    def highlight(self):
        self.ghost = True

    def unhighlight(self):
        self.ghost = False

    def draw(self, turn):

        action = None

        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos) and self.piece == None:

            action = 'hover'

            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = 'clicked'

            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        if self.ghost:
            if turn == 'RED':
                pygame.draw.circle(screen, RED, (self.rect.x+NODE_SIZE//2, self.rect.y+NODE_SIZE//2), RADIUS_SIZE//2)
            if turn == 'YELLOW':
                pygame.draw.circle(screen, YELLOW, (self.rect.x+NODE_SIZE//2, self.rect.y+NODE_SIZE//2), RADIUS_SIZE//2)

        if self.piece == 'RED':
            pygame.draw.circle(screen, RED, (self.rect.x+NODE_SIZE//2, self.rect.y+NODE_SIZE//2), RADIUS_SIZE)
        elif self.piece == 'YELLOW':
            pygame.draw.circle(screen, YELLOW, (self.rect.x+NODE_SIZE//2, self.rect.y+NODE_SIZE//2), RADIUS_SIZE)

        return action

class Board():

    def __init__(self):
        self.reset_board()

    def reset_board(self):
        self.board = self.new_board()
        self.turn = 'RED'
        self.winner = None

    def new_board(self):
        return [[Node(x, y) for x in range(BOARD_WIDTH)] for y in range(BOARD_HIGHT)]

    def next_turn(self):
        self.turn = 'YELLOW' if self.turn == 'RED' else 'RED'

    def show_drop_path(self, node):
        for y in range(len(self.board)):
            if y != len(self.board)-1:
                if self.board[y][node.x].piece == None and self.board[y+1][node.x].piece != None:
                    self.board[y][node.x].highlight()
                    break
            elif self.board[y][node.x].piece == None:
                self.board[y][node.x].highlight()

        for y in self.board:
            for x in y:
                if x.x == node.x:
                    continue
                x.unhighlight()

    def drop_piece(self, node):
        for y in range(len(self.board)):
            if y != len(self.board)-1:
                if self.board[y][node.x].piece == None and self.board[y+1][node.x].piece != None:
                    self.board[y][node.x].piece = self.turn
                    break
            elif self.board[y][node.x].piece == None:
                self.board[y][node.x].piece = self.turn
        if self.check_connect4(self.board[y][node.x]):
            self.winner = self.turn
            return
        self.next_turn()

    def check_next_node(self, node, x1, y1):
        # out of bounds check
        if node.y+y1 < 0 or node.y+y1 > BOARD_HIGHT-1 or node.x+x1 < 0 or node.x+x1 > BOARD_WIDTH-1:
            return False
        next_node = self.board[node.y+y1][node.x+x1]
        if next_node.piece == self.turn:
            return True
        return False

    def check_connect4(self, node):
        horizontal = 1
        vertical = 1
        diagonal_1 = 1
        diagonal_2 =1
        for c in {(1,0),(-1,0)}:
            for n in range(1,CONNECT):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    horizontal += 1
        for c in {(0,1),(0,-1)}:
            for n in range(1,CONNECT):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    vertical += 1
        for c in {(-1,1),(1,-1)}:
            for n in range(1,CONNECT):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    diagonal_1 += 1
        for c in {(1,1),(-1,-1)}:
            for n in range(1,CONNECT):
                if self.check_next_node(node,c[0]*n,c[1]*n):
                    diagonal_2 += 1
        if any(v == CONNECT for v in (horizontal, vertical, diagonal_1, diagonal_2)):
            return True
        return False

    def draw(self):
        # draw board background
        for y in range(BOARD_HIGHT):
            for x in range(BOARD_WIDTH):
                pygame.draw.rect(screen, BLUE, (x*NODE_SIZE, y*NODE_SIZE, NODE_SIZE, NODE_SIZE))
                pygame.draw.circle(screen, WHITE, (x*NODE_SIZE+NODE_SIZE//2, y*NODE_SIZE+NODE_SIZE//2), RADIUS_SIZE)

        # draw pieces
        for y in self.board:
            for x in y:
                action = x.draw(self.turn)
                if action == 'hover' and not self.winner:
                    self.show_drop_path(x)
                elif action == 'clicked' and not self.winner:
                    self.drop_piece(x)

        # winner screen
        if self.winner:
            pygame.draw.rect(screen, WHITE, END_SCREEN)
            pygame.draw.rect(screen, BLACK, END_SCREEN, 5)
            end_text = TEXT_FONT.render(str(self.winner)+" WON!", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+(5*NODE_SIZE - end_text.get_width())//2, END_SCREEN.y+20))
            end_text = TEXT_FONT_2.render("Press 'r' to reset game.", 1, BLACK)
            screen.blit(end_text, (END_SCREEN.x+80, END_SCREEN.y+120))

def main():

    connect4 = Board()
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    connect4.reset_board()
        connect4.draw()

        pygame.display.update()

if __name__ == '__main__':
    main()
