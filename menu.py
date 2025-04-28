import pygame
import os
from subprocess import call

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Menu")

# Wczytaj tło
background = pygame.image.load('data/bcg.png')

# Definicja kolorów
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definicja przycisków
button_font = pygame.font.Font(None, 50)
info_font = pygame.font.Font(None, 30)  # Czcionka dla informacji

# Utwórz powierzchnie dla przycisków
single_text = button_font.render("Single", True, WHITE)
coop_text = button_font.render("Coop", True, WHITE)

# Utwórz powierzchnie dla informacji
info_text = info_font.render("Statek Pomarańczowy: WASD i lewy ALT", True, WHITE)
info2_text = info_font.render("Statek Niebieski: strzałki i prawy CTRL", True, WHITE)

# Ustawienie pozycji przycisków
single_rect = single_text.get_rect(center=(300, 150))
coop_rect = coop_text.get_rect(center=(300, 250))

# Ustawienie pozycji dla informacji
info_rect = info_text.get_rect(center=(300, 350))
info2_rect = info2_text.get_rect(center=(300, 380))

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if single_rect.collidepoint(event.pos):
                call(["python", "single.py"])
            elif coop_rect.collidepoint(event.pos):
                call(["python", "coop.py"])

    # Rysowanie tła
    screen.blit(background, (0, 0))

    # Rysowanie przycisków
    pygame.draw.rect(screen, BLACK, single_rect.inflate(20, 20))
    pygame.draw.rect(screen, BLACK, coop_rect.inflate(20, 20))
    screen.blit(single_text, single_rect)
    screen.blit(coop_text, coop_rect)

    # Rysowanie informacji o sterowaniu
    screen.blit(info_text, info_rect)
    screen.blit(info2_text, info2_rect)

    # Aktualizacja ekranu
    pygame.display.flip()

# Zakończenie Pygame
pygame.quit()
