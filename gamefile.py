#importing packages
import random
import pygame as pg

#initializing pygame and game variables
pg.init()
screen = pg.display.set_mode((1280,720))
clock =pg.time.Clock()
gameState = 'startscreen'
selectedDifficulty = 'easy'
score = 0

#creating a class to create objects
class CreateObject():
    #function to create text
    def text(self, position, text, colour,size, rectpos = None, **kwargs):
        self.surface = pg.font.Font(None, size).render(text, False, colour)
        if rectpos == 'topleft':
            self.rect = self.surface.get_rect(topleft = position)
        else:
            self.rect = self.surface.get_rect(midtop = position)

    #function to blit the text to the screen
    def screenBlit(self):
        screen.blit(self.surface,self.rect)

#Creating the objects
startGame, difficulty, easy, medium, hard, guessNumberText, guessText, returnToStartMenu, textSurface, winCheck, scoreSurface =CreateObject(), CreateObject(), CreateObject(), CreateObject(),CreateObject(),CreateObject(), CreateObject(), CreateObject(), CreateObject(), CreateObject(), CreateObject()
#setting the text for the objects
startGame.text((370,300),"Start game","yellow",80)
difficulty.text((870, 100), "Difficulty", "Blue", 60)
easy.text((870,200), 'easy','#5ced73',40)
medium.text((870,300), 'medium','#e69b00',40)
hard.text((870,400), 'hard','#5E1914',40)
returnToStartMenu.text((1100, 650),"Return To Start Menu","Red",30)

#initilizing the music
pg.mixer.music.load('assets/backroundmusic.mp3')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.2)

#game loop
while True:
    #checking for events
    for event in pg.event.get():
        #check if the user wants to quit
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        #check for gamestate
        if gameState == 'startscreen':
            #check for mouse clicks
            if event.type == pg.MOUSEBUTTONDOWN:
                #check if the mouse is clicking on easy button
                if easy.rect.collidepoint(event.pos):
                    selectedDifficulty = 'easy'

                #check if the mouse is clicking on medium button
                if medium.rect.collidepoint(event.pos):
                    selectedDifficulty = 'medium'

                #check if the mouse is clicking on hard button
                if hard.rect.collidepoint(event.pos):
                    selectedDifficulty = 'hard'

                #check if the mouse is clicking on start game button
                if startGame.rect.collidepoint(event.pos):
                    playerWon = False
                    #set the number to guess and the amount of guesses based on the difficulty and change gamestate to start the game
                    if selectedDifficulty == 'easy':
                        numberToGuess = random.randint(0, 25)
                        guesses = 4
                        guessNumberText.text((640,120),'Guess my number! It is between 0 and 25', 'Black', 70)

                    if selectedDifficulty == 'medium':
                        numberToGuess = random.randint(0,50)
                        guesses = 5
                        guessNumberText.text((640, 120), 'Guess my number! It is between 0 and 50', 'Black', 70)

                    if selectedDifficulty == 'hard':
                        numberToGuess = random.randint(0,75)
                        guesses = 6
                        guessNumberText.text((640, 120), 'Guess my number! It is between 0 and 75', 'Black', 70)

                    userText = ''
                    playGame = True
                    gameState = 'game'
        #check for gamestate
        if gameState == 'game':
            #check for mouse clicks
            if event.type == pg.MOUSEBUTTONDOWN:
                #check if the mouse is clicking on the return to start menu button and reset the game
                if returnToStartMenu.rect.collidepoint(event.pos):
                    del winCheck
                    winCheck = CreateObject()
                    gameState = 'startscreen'
            #check for keyboard input
            if event.type == pg.KEYDOWN and playGame is True:
                #check if the user is pressing the backspace key to delete the last character
                if event.key == pg.K_BACKSPACE:
                    userText = userText[:-1]
                #check if the user is pressing the enter key to check their guess
                elif event.key == pg.K_RETURN and userText != '':
                    if int(userText) == numberToGuess:
                        winCheck.text((640, 400), 'You Win!, Return to main menu to play again', 'Black', 70)
                        if selectedDifficulty == 'easy':
                            score += 1
                        if selectedDifficulty == 'medium':
                            score += 2
                        if selectedDifficulty == 'hard':
                            score += 3
                        playerWon = True
                        playGame = False
                    if int(userText) > numberToGuess:
                        winCheck.text((640, 400), f'You guessed {userText}, My Number is Lower!', 'Black', 70)
                    if int(userText) < numberToGuess:
                        winCheck.text((640, 400), f'You guessed {userText}, My Number is Higher!', 'Black', 70)
                    userText = ''
                    #check if the user has run out of guesses and has not won
                    guesses -= 1
                    if guesses == 0 and playerWon is False:
                        winCheck.text((640, 400), f'You Lose! My Number was {numberToGuess}, Return to main menu to play again', 'Black', 50)
                        playGame = False
                #check if the user is pressing a number key and add it to the userText
                if event.type == pg.KEYDOWN and event.unicode.isdigit():
                    userText += event.unicode

    #creating surface for score
    scoreSurface.text((10, 10), f"Score: {score}", "Black", 50, rectpos = 'topleft')
    #drawing the start screen
    if gameState == 'startscreen':
        screen.fill('#554904')
        scoreSurface.screenBlit()
        startGame.screenBlit()
        difficulty.screenBlit()
        easy.screenBlit()
        medium.screenBlit()
        hard.screenBlit()

        #draw a rectangle around the selected difficulty
        if selectedDifficulty == 'easy':
            pg.draw.rect(screen, 'Blue',(easy.rect.left, easy.rect.top, easy.rect.right - easy.rect.left, easy.rect.bottom - easy.rect.top), 3)

        if selectedDifficulty == 'medium':
            pg.draw.rect(screen, 'Blue',(medium.rect.left, medium.rect.top, medium.rect.right - medium.rect.left, medium.rect.bottom - medium.rect.top), 3)

        if selectedDifficulty == 'hard':
            pg.draw.rect(screen, 'Blue',(hard.rect.left, hard.rect.top, hard.rect.right - hard.rect.left, hard.rect.bottom - hard.rect.top), 3)

    #drawing the game screen
    if gameState == 'game':
        screen.fill('#fff5be')
        scoreSurface.screenBlit()
        guessText.text( (1100, 20), f"You Have {guesses} Guesses Left!", "black", 30)
        guessText.screenBlit()
        guessNumberText.screenBlit()
        returnToStartMenu.screenBlit()
        #draw the users guess and check for win or loss
        if hasattr(winCheck, 'surface'):
            winCheck.screenBlit()
        textSurface.text((160, 250),f'{userText}',"Black",60, rectpos = 'topleft')
        textSurface.screenBlit()
    pg.display.update()
    clock.tick(60)
