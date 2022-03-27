#this is a memory game in which different images has been hidden in a grid board userhas to select image pairs. selected pair sremain unhidden.
import pygame, random, time


# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Memory game')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.score = 0
        self.board_size = 4
        self.board = []
        self.create_board()
        self.tile1 = None  #no tile in the beginning 
        self.tile2 = None
        self.clicked = 0

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()
            if self.continue_game:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def create_board(self):

        self.images = []
        
        new_images = ['image1.bmp', 'image2.bmp', 'image3.bmp', 'image4.bmp', 'image5.bmp', 'image6.bmp', 'image7.bmp',
                     'image8.bmp']   #list of images stored in an empty list
        new_images = new_images*2
        random.shuffle(new_images)
        for image in new_images:
       
            self.images.append(image)
        face_image= pygame.image.load('image0.bmp')  #face_image for all the images

        width = self.surface.get_width() // 5  #height and width of the board
        height = self.surface.get_height() // 4
    
        for row_index in range(0, self.board_size):
            #creating a board using nested for and while loops and lists
            row = []
            
            for col_index in range(0, self.board_size):
               
                x = col_index * width
                y = row_index * height
                imageindex = row_index * self.board_size + col_index
                self.image = self.images[imageindex]
               

                self.tile = Tile(x, y, self.image, face_image, self.surface)
               
                row.append(self.tile)
           
            self.board.append(row)

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.game_play(event.pos)

    def game_play(self, position): #how tiles marked and shown
       
        for row in self.board:
            for tile in row:
                if tile.opening_tile(position):

                    if self.tile1 == None:         
                        tile.paired_tiles(True)
                        
                        self.tile1 = [self.board.index(row), row.index(tile)] #conatins details about rows and column for tile 1 

                    else:
                        tile.paired_tiles(True)
                       
                        self.tile2 = [self.board.index(row), row.index(tile)] #for tile 2


    def back_to_face_image(self):
        #if tiles dont match then face_image will be displayed again
        if self.tile1 != None and self.tile2 != None:
            if not self.board[self.tile1[0]][self.tile1[1]].match_tiles(
                    self.board[self.tile2[0]][self.tile2[1]]):
                time.sleep(1)
                self.board[self.tile1[0]][self.tile1[1]].paired_tiles(False)
                self.board[self.tile2[0]][self.tile2[1]].paired_tiles(False)
            self.tile1 = None
            self.tile2 = None


    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        for row in self.board:
            for tile in row:
                tile.draw()
        self.draw_score()
        pygame.display.update()  # make the updated surface appear on the display

    def draw_score(self): #drawing the score
      
        size = self.surface.get_width()
        fg_color = pygame.Color('white')
        
        font = pygame.font.SysFont('', 70)
        
        text_string = '' + str(self.score)
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        surface_height = self.surface.get_width()
        text_box_height = text_box.get_width()
        location = (surface_height - text_box_height, 0)
    
        self.surface.blit(text_box, location)

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update
        self.score = pygame.time.get_ticks() // 1000
        self.back_to_face_image()

    def decide_continue(self):
        # Check and remember if the game should continue
        # - self is the Game to check
        tiles_exposed = 0
        for row in self.board:
            for self.tile in row:
                if self.tile.opened_tile == True:
                    tiles_exposed += 1
        if tiles_exposed == 16:
            self.continue_game = False


class Tile:
     #this class has all the properties associated with a tile 
    def __init__(self, x, y, image, face_image, surface): #the coordinates color and all the specific an dparticular objects related to tile is pesented here
      

        self.left = x
        self.top = y

        self.surface = surface
        self.image = image
        self.face_image = face_image
        self.opened_tile = False  #no tile is opened in the beginning



    def draw(self):
        # draws a Tile object
        # -self is the Tile object to draw
        color = pygame.Color('black')
        border_width = 5
        image = pygame.image.load(self.image)
        self.rect = pygame.Rect(self.left, self.top, image.get_width(), image.get_height())
        pygame.draw.rect(self.surface, color, self.rect, border_width,)

        self.surface.blit(self.face_image, self.rect)
        if self.opened_tile == True:
            self.surface.blit(image, self.rect)
        else:
            self.surface.blit(self.face_image, self.rect)

    def match_tiles(self, other_tile):#checks if tiles match
        
        if self.image == other_tile.get_image():
            return True

    def paired_tiles(self, is_exposed):
        #if 2 tiles match then they are remaied open 
        self.opened_tile = is_exposed

    def get_image(self):
        #returns the new image of tile
        return self.image
    def opening_tile(self, position):
     #opeing of tile 
        if self.rect.collidepoint(position):
            if not self.opened_tile:
                return True
            else:
                return False                    



main()
#collaborated with rahulpreet