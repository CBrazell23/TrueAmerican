import pygame
import random

# Center Table with 4 branches out of it each with 5 tiles
# Shit load of drinks on the Center Table
# Game begins with everyone shotgunning then running to a random tile
# Every time you pass Center Table, pick up a drink
# Can only have up to two drinks at a time
# Shoot empty cans into a corner bin - make it and give someone a drink
# Each drink finished is a point
# All points between players can be bargained for but NO FREEBIES
# First to 15 points wins

players = ["Andrew", "Cole", "Andreas", "Holly", "Shreya", "Annie"]

crazyOptions = ["Everybody move forward 2 spaces",
                "Switch drinks with the person closest to you and finish the drink",
                "Put up a number on one hand! If you share that number with anyone, take that many drinks",
                "Unlucky :( Finish your drink",
                "Finish your drink and steal a point from someone"]

normalOptions = ["JFK! Everyone gains a point",  # FDR
                 "T OR D",
                 "Paranoia",
                 "Donald Trump!",  # Build that wall
                 "Hot seat! Everyone asks you a question. You may choose to not answer, but take a step forward. Answer them all for a point",
                 "Come up with a Never Have I Ever. Anyone who has done it must drink",
                 "2 Truths and a Lie. Anyone who correctly guesses the lie may take a step back",
                 "Drive! Loser takes a step forward",
                 "Pick someone. You both drink and take a step forward",
                 "Ladies drink! All take a step forward",
                 "Guys drink! All take a step forward",
                 "Heaven! Loser takes a drink and a step forward",
                 "You are now the sole questionmaster. Anyone who answers any of your questions must drink",
                 "Come up with a new rule. You may twerk at any point to remove this rule",
                 "Do a celebrity impression. If someone guesses it within your first 10 seconds, take a step back",
                 "Flamingo time. First person to fall, take a step forward",
                 "Everyone shorter than you drink. That means you, Andrew"  # Delete if no dd lol
                 ]

retiredCrazies = []
tempNorm = ""
chosen = ""

pygame.init()

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 780

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

text_font = pygame.font.SysFont("Arial", 60)


def draw_text(text, font, text_col, x, y, max_width, screen_width, screen_height):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)

    # Calculate total height of the text
    total_height = len(lines) * font.get_height()
    # Calculate starting position for vertically centering
    y_pos = (screen_height - total_height) // 2

    for line in lines:
        img = font.render(line, True, text_col)
        text_width = font.size(line)[0]
        x_pos = (screen_width - text_width) // 2
        screen.blit(img, (x_pos, y_pos))
        y_pos += font.get_height()


run = True
numPlayers = 0
name = ""
while run:
    if(numPlayers == 0):
        numPlayers = len(players)
    name = players[len(players) - numPlayers]
    numPlayers -= 1

    option = name + ": "
    saveCrazy = random.randint(1, 10)  # Generate 1 in 10 chance to save a crazy
    if (saveCrazy == 10 and len(retiredCrazies) != 0):  # Ensures retiredCrazies isn't empty
        crazyOptions.append(retiredCrazies[0])  # Puts the crazy back in crazyOptions
        retiredCrazies.pop(0)  # Pops the crazy out of retiredCrazies

    if (len(crazyOptions) == 0):
        crazyOptions.append(retiredCrazies.pop(0))

    n = random.randint(1, 5)
    if (n == 5):  # Generate 1 in 5 chance any given turn is crazy
        randInt = random.randint(0, len(crazyOptions) - 1)  # Picks a random option from crazyOptions
        option += crazyOptions[randInt]  # Appends to option
        retiredCrazies.append(crazyOptions[randInt])  # Retires the crazy
        crazyOptions.pop(randInt)  # Pops the crazy out of crazyOptions
    else:
        while (chosen == tempNorm):  # While loop to ensure same option doesn't happen twice in a rwo
            randInt = random.randint(0, len(normalOptions) - 1)
            chosen = normalOptions[randInt]
        tempNorm = chosen  # Sets the temp norm to previous output
        if (tempNorm == "T OR D"):
            idx = random.randint(0, len(players) - 1)
            person2 = players[idx]
            option += person2 + " Truth or Dare"
        elif (tempNorm == "Paranoia"):
            idx = random.randint(0, len(players) - 1)
            person2 = players[idx]
            option += "Lava is off for you. Ask " + person2 + " a Paranoia. Any player may move forward " \
                                                                         "three spaces to reveal the question"
        else:
            option += normalOptions[randInt]

    screen.fill((0, 73, 83))  # Background color

    max_text_width = int(0.8 * SCREEN_WIDTH)  # 80% of the screen width
    draw_text(option, text_font, (169, 172, 182), 0, 0, max_text_width, SCREEN_WIDTH, SCREEN_HEIGHT)

    pygame.display.flip()

    # Wait for space bar press
    space_pressed = False
    while not space_pressed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
            if event.type == pygame.QUIT:
                run = False
                space_pressed = True  # Break the loop and exit the game if the window is closed

pygame.quit()
