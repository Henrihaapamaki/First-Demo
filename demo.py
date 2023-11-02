import pygame
import sys

# Alustetaan pygame moduulit.
pygame.init()

# Määritetään ikkunan koko ja nimi.
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Catch the ball!")

# Luodaan väri-muuttujat.
black = (0, 0, 0)
white = (255, 255, 255)

# Määritetään pallon arvot.
ball_radius = 10
ball_color = white
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 5
ball_speed_y = 5

game_won = False
play_again = False

# Luodaan clock objecti, joka mahdollistaa mm. ajoittamisen ja fps-säädöt.
clock = pygame.time.Clock()

# Alustaa uuden pelin.
def reset_game():
    global ball_x, ball_y, game_won, play_again
    ball_x = width // 2
    ball_y = height // 2
    game_won = False
    play_again = False

# Pääsilmukka pelin suorittamisesta. Niin kauan kuin running arvo on true, peli on käynnissä.
running = True
while running:
    # Ingame eventtien tapahtumankäsittely (klikkailu ja hiiren liike).
    for event in pygame.event.get():
        # Tarkistaa onko ehtolauseen tyyppi pygame.quit eli yritetäänkö peli sulkea.
        # Jos ehtolause toteutuu eli pelaaja sulkee pelin muuttujan running arvo epätodeksi, jolloin peli sulkeutuu.
        if event.type == pygame.QUIT:
            running = False
        # Tarkastetaan hiiren klikkaus    
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Tarkistetaan osuma ehtolauseella onko klikkaus tarpeeksi lähellä ja
            # asetetaan muuttujat game_won ja play_again todeksi.
            if (ball_x - mouse_x)**2 + (ball_y - mouse_y)**2 <= ball_radius**2:
                game_won = True
                play_again = True

    # Kysytään pelaajalta syötettä uudesta pelistä. Luodaan surface default fontilla, jonka koko on 36.
    if play_again:
        screen.fill(black)
        font = pygame.font.Font(None, 36)
        text = font.render("Voitit pelin! Haluatko pelata uudestaan? (y/n)", True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        # Asetetaan muuttuja todeksi ilmaisemaan odotetaanko syötettä.
        waiting_for_input = True
        
        # While looppi käynnissä niin kauan kuin pelaaja antaa syötteen.
        while waiting_for_input:
            # Käy läpi pelin tapahtumat viime päivityksen jälkeen.
            for event in pygame.event.get():
                # 
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_input = False
                # Tarkistaa onko näppäin painettuna.   
                elif event.type == pygame.KEYDOWN:
                    # Jos "Y" painettu suorittaa koodin joka alustaa uuden pelin.
                    if event.key == pygame.K_y:
                        reset_game()
                        waiting_for_input = False
                    # Jos "N" painettu running ja waiting for input toteutuu ja peli sulkeutuu.   
                    elif event.key == pygame.K_n:
                        running = False
                        waiting_for_input = False

    # Liikutetaan palloa annetuilla arvoilla jos peliä ei ole voitettu.    
    else:
        if not game_won:
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Pallon liikkeen määrittäminen kun ruutu loppuu eli kimpoilu.
            # Pallon liike siirtyy vastakkaiseksi (-ball speed).
            if ball_x + ball_radius > width or ball_x - ball_radius < 0:
                ball_speed_x = -ball_speed_x
            if ball_y + ball_radius > height or ball_y - ball_radius < 0:
                ball_speed_y = -ball_speed_y
        
        # tyhjentään näytön aina uutta piirtoa joten saadaan näkymään pallona
        screen.fill(black)
        
        # Funktiolla piirretään ympyrä, joka käyttää ball_color arvoa värinä.
        pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    pygame.display.flip() #Näytön päivitys.
    clock.tick(60) #FPS-määrittely.

# Lopetetaan peli.
pygame.quit()
sys.exit()
