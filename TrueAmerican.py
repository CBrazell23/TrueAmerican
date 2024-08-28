import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions and configuration
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 780
SCOREBOARD_WIDTH = 300  # Increased width for buttons
FPS = 60

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("True American")

# Fonts
text_font = pygame.font.SysFont("Arial", 30)
large_font = pygame.font.SysFont("Arial", 60)
clock = pygame.time.Clock()

# Initialize player scores and game settings
players = ["Andrew", "Cole", "Andreas", "Holly", "Shreya", "Annie"]
scores = {player: 0 for player in players}

# Crazy and normal options for the game
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
                 "Do a celebrity impression. If someone guesses it before the timer runs out, take a step back",
                 "Flamingo time. First person to fall, take a step forward",
                 "Everyone shorter than you drink. That means you, Andrew"]  # Delete if no dd lol

# Initialize additional game variables
retiredCrazies = []
tempNorm = ""
chosen = ""

# Timer settings
round_time = 30  # Each round lasts 30 seconds
timer_start = time.time()

# Scoreboard Surface
SCOREBOARD_HEIGHT = SCREEN_HEIGHT
scoreboard_surface = pygame.Surface((SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))
scoreboard_bg_color = (30, 30, 30)  # Dark background for scoreboard
scoreboard_text_color = (255, 255, 255)  # White text for scores

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

    # Calculate starting x position for horizontally centering
    remaining_width = screen_width - SCOREBOARD_WIDTH  # Available width excluding the scoreboard
    x_start = SCOREBOARD_WIDTH + (remaining_width - max_width) // 2

    for line in lines:
        img = font.render(line, True, text_col)
        text_width = font.size(line)[0]
        x_pos = x_start + (max_width - text_width) // 2  # Center text within the remaining space
        screen.blit(img, (x_pos, y_pos))
        y_pos += font.get_height()

def draw_scoreboard():
    """Draw the dynamic scoreboard on the left side of the screen."""
    # Clear the scoreboard surface
    scoreboard_surface.fill(scoreboard_bg_color)

    # Calculate dynamic spacing based on the number of players
    num_players = len(scores)
    if num_players > 0:
        space_between_scores = SCOREBOARD_HEIGHT // (num_players + 1)  # Dynamic spacing

        y_offset = space_between_scores
        for player, score in scores.items():
            score_text = f"{player}: {score}"
            text_surface = text_font.render(score_text, True, scoreboard_text_color)
            scoreboard_surface.blit(text_surface, (20, y_offset))

            # Draw + and - buttons
            minus_button_rect = pygame.Rect(SCOREBOARD_WIDTH - 60, y_offset, 20, 20)
            plus_button_rect = pygame.Rect(SCOREBOARD_WIDTH - 30, y_offset, 20, 20)

            pygame.draw.rect(scoreboard_surface, (255, 255, 255), minus_button_rect)  # White for -
            pygame.draw.rect(scoreboard_surface, (255, 255, 255), plus_button_rect)  # White for +

            # Render + and - text
            minus_text = text_font.render('-', True, scoreboard_bg_color)
            plus_text = text_font.render('+', True, scoreboard_bg_color)

            # Center the + and - text in their respective rectangles
            minus_text_rect = minus_text.get_rect(center=minus_button_rect.center)
            plus_text_rect = plus_text.get_rect(center=plus_button_rect.center)

            scoreboard_surface.blit(minus_text, minus_text_rect)
            scoreboard_surface.blit(plus_text, plus_text_rect)


            y_offset += space_between_scores  # Move down for the next player's score

    # Blit the scoreboard surface onto the main screen
    screen.blit(scoreboard_surface, (0, 0))

def draw_timer():
    """Draw the countdown timer on the screen."""
    elapsed_time = time.time() - timer_start
    remaining_time = max(0, round_time - int(elapsed_time))
    timer_text = f"Time Left: {remaining_time}s"
    text_surface = large_font.render(timer_text, True, (255, 255, 255))
    screen.blit(text_surface, (SCREEN_WIDTH - 450, 10))  # Adjusted X position for visibility

run = True
numPlayers = 0
name = ""

while run:
    if numPlayers == 0:
        numPlayers = len(players)
    name = players[len(players) - numPlayers]
    numPlayers -= 1

    option = name + ": "
    saveCrazy = random.randint(1, 10)  # Generate 1 in 10 chance to save a crazy
    if saveCrazy == 10 and len(retiredCrazies) != 0:  # Ensures retiredCrazies isn't empty
        crazyOptions.append(retiredCrazies[0])  # Puts the crazy back in crazyOptions
        retiredCrazies.pop(0)  # Pops the crazy out of retiredCrazies

    if len(crazyOptions) == 0:
        crazyOptions.append(retiredCrazies.pop(0))

    n = random.randint(1, 5)
    if n == 5:  # Generate 1 in 5 chance any given turn is crazy
        randInt = random.randint(0, len(crazyOptions) - 1)  # Picks a random option from crazyOptions
        option += crazyOptions[randInt]  # Appends to option
        retiredCrazies.append(crazyOptions[randInt])  # Retires the crazy
        crazyOptions.pop(randInt)  # Pops the crazy out of crazyOptions
    else:
        while chosen == tempNorm:  # While loop to ensure same option doesn't happen twice in a row
            randInt = random.randint(0, len(normalOptions) - 1)
            chosen = normalOptions[randInt]
        tempNorm = chosen  # Sets the temp norm to previous output
        if tempNorm == "T OR D":
            idx = random.randint(0, len(players) - 1)
            person2 = players[idx]
            option += person2 + " Truth or Dare"
        elif tempNorm == "Paranoia":
            idx = random.randint(0, len(players) - 1)
            person2 = players[idx]
            option += "Lava is off for you. Ask " + person2 + " a Paranoia. Any player may move forward three spaces to reveal the question"
        else:
            option += normalOptions[randInt]

    # Main screen background color
    screen.fill((0, 73, 83))

    # Draw UI elements
    draw_scoreboard()

    max_text_width = int(0.8 * (SCREEN_WIDTH - SCOREBOARD_WIDTH))  # 80% of the remaining screen width
    draw_text(option, large_font, (169, 172, 182), 0, 0, max_text_width, SCREEN_WIDTH, SCREEN_HEIGHT)

    pygame.display.flip()
    clock.tick(FPS)

    space_pressed = False
    while not space_pressed:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_pressed = True
                    timer_start = time.time()  # Reset timer for a new round
                    random_player = random.choice(list(scores.keys()))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_x < SCOREBOARD_WIDTH:
                    # Determine which player was clicked
                    for idx, player in enumerate(players):
                        space_between_scores = SCOREBOARD_HEIGHT // (len(scores) + 1)
                        y_offset = (idx + 1) * space_between_scores
                        plus_button_rect = pygame.Rect(SCOREBOARD_WIDTH - 30, y_offset, 20, 20)
                        minus_button_rect = pygame.Rect(SCOREBOARD_WIDTH - 60, y_offset, 20, 20)

                        if plus_button_rect.collidepoint(mouse_x, mouse_y):
                            scores[player] += 1
                            draw_scoreboard()
                            pygame.display.flip()
                        elif minus_button_rect.collidepoint(mouse_x, mouse_y):
                            scores[player] -= 1
                            draw_scoreboard()
                            pygame.display.flip()

            if event.type == pygame.QUIT:
                run = False
                space_pressed = True  # Break the loop and exit the game if the window is closed

        # Continuously update the timer while waiting for space press
        screen.fill((0, 73, 83))  # Background color of the main screen
        draw_scoreboard()
        if "Do a celebrity impression. If someone guesses it before the timer runs out, take a step back" in option:
            draw_timer()
        draw_text(option, large_font, (169, 172, 182), 0, 0, max_text_width, SCREEN_WIDTH, SCREEN_HEIGHT)
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
