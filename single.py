import pygame
import os
import random

pygame.font.init()
os.environ['SDL_AUDIODRIVER'] = 'dsp'
pygame.init()

# ustawienie wielkości okna
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# nazwa okna
pygame.display.set_caption('Space Invaders - Singleplayer mode')

# ładujemy wszystkie obrazki
statek = pygame.image.load('data/ship.png')
bullet = pygame.image.load('data/bullet.png')
bcg = pygame.image.load('data/bcg.png')
alien = pygame.image.load('data/alien.png')

# pozycja, w której respi się statek, a później te zmienne będą używane do określania aktualnej pozycji statku
actual_position_x = 270
actual_position_y = 300

# lista przechowująca aktywne pociski
bullets = []

# lista z przeciwnikami
enemies = []

# te zmienne służą nam aby ograniczyć prędkość strzelania z naszego statku
fire_rate = 333  # 3 pociski na sekundę (1000 ms / 3)
last_shot_time = 0

# czcionka
main_font = pygame.font.SysFont("arial", 25)

#podstawowe poczatkowe dane
level = 1
lives = 5
score = 0 

#funkcja kończąca gre po pregranej lub wygranej w zależności od parametru
def exit_game(message):
    game_over = main_font.render(message, 1, (255, 255, 255)) #tworzymy napis game over albo zwycięstwo z pomocą wczesniej zaimpoirtowanych czcionek
    screen.blit(game_over, (300 - game_over.get_width() // 2, 200)) #wyswietlamy napis na ekranie
    pygame.display.flip() #resetujemy ekran, tzn renderujemy wszystko co trzeba jescze raz

    pygame.time.wait(2000)#czekamy 2 sekundy po wyswietleniu komunikatu na zamkniecie gry

    pygame.quit()#zamykanie gry

def spawn_enemies(level): #ilosc zrespionych enemies zalezy od levelu na jakim jestesmy, dlatego level jest jako nasz param
    enemies.clear()  # czysciym wszystkich poprzednich enemy z listy w razie jakby jacys zostali
    ile_enemies = 5 * level  # z kazdym levelem zwiekszamy ilosc enemies
    for i in range(ile_enemies):
        x = random.randrange(5, 555) #losowa pozycja nad ekranem w x axis
        y = random.randrange(-500, -5) #losowa pozycja nad ekranem w y axis
        speed = 1 + (level - 1) * 0.05  # z kazdym levelem nie dosc ze przeciwnikow jest wiecej to jesze są szybsi
        enemies.append([x, y, speed])#dodajemy do listy z enemies to enemy z losowymi koordynatami i okresloną predkoscią


#zmienna która sprawia ze fala zrespi się tylko raz, a nie z kazdą klatką (warunki w linii 164)
wave = False



# główna pętla gry to co sie tu dzieje to tak jakby kazda klatka 
running = True
while running:

    # tło, rysujemy na samym dole co kazdą klatke
    screen.blit(bcg, (0, 0))
    
    # wygeneruj wyniki
    lives_display = main_font.render(f"Życia: {lives}", 1, (255, 255, 255)) #życia
    level_display = main_font.render(f"Poziom: {level}", 1, (255, 255, 255)) #level
    score_display = main_font.render(f"Wynik: {score}", 1, (255, 255, 255)) #wynik
    
    #wyswietl wyniki
    screen.blit(lives_display, (5, 5))
    screen.blit(level_display, (480, 5))
    screen.blit(score_display, (250, 5)) 

    #jezeli mamy jeszcze zycia to kontynuujmy gre
    if lives > 0:
        # zdarzenia zewnętrzne np. kliknięcie na klawiaturze
        for event in pygame.event.get():
            # zdarzenie zamknięcia programu jesli klikniemy iksa to zeby faktycznie program sie zamknał a nie scrashował
            if event.type == pygame.QUIT:
                running = False

        # kolekcja zawierająca przyciśnięte klawisze
        keys = pygame.key.get_pressed()

        # poruszanie się statku
        if keys[pygame.K_LEFT]:
            if actual_position_x > 0: #ograniczenie zeby nie poruszyc sie za ekran w lewo
                actual_position_x -= 3

        if keys[pygame.K_UP]:
            if actual_position_y > 0: #ograniczenie zeby nie poruszyc sie za ekran w górę
                actual_position_y -= 3

        if keys[pygame.K_RIGHT]:
            if actual_position_x < 540: #ograniczenie zeby nie poruszyc sie za ekran w prawo
                actual_position_x += 3

        if keys[pygame.K_DOWN]:
            if actual_position_y < 352: #ograniczenie zeby nie poruszyc sie za ekran w dół
                actual_position_y += 3

        # strzelanie - dodanie pocisku do listy i ograniczenia względem firerate
        current_time = pygame.time.get_ticks() #bierzemy aktualny czas aby mierzyc odstęp między strzelaniem i miec odpowiedni firerate
        if keys[pygame.K_RCTRL]:
            if current_time - last_shot_time >= fire_rate: #jesli minął odpowiedni czas od ostatniego strzału, można znowu strzelić
                bullets.append([actual_position_x + 25, actual_position_y - 10]) #dodajemy pocisk do listy, na srodku statku i troche nad nim
                last_shot_time = current_time #aktualizujemy czas ostatniego strzału aby określac firerate

        # rysowanie statku
        screen.blit(statek, (actual_position_x, actual_position_y))

        
        bullets_to_remove = [] #lista do której damy wszystkie pociski które będa sklasyfikowane do wywalenia (np uderzyły w coś bądź wyszły za ekran )

        # rysowanie pocisków
        for bullet_pos in bullets: #w liscie kazdy jej element (wiersz) potraktujemy jako bullet_pos ponieważ każdy element zawiera 2 wartosci: x y i jest to pozycja
            bullet_pos[1] -= 5  # przesuwamy w góre pocisk i zaraz sprawdzimy czy to jest ok
            if bullet_pos[1] < 0: #jesli pocisk wyszedł za ekran
                bullets_to_remove.append(bullet_pos) #to dodaj go do listy pocisków do usunięcia
            else:
                screen.blit(bullet, bullet_pos) #jesli pocisk nie wyszedl za ekran to wyswietlaj go dalej


        # Tworzenie prostokąta dla pocisku, aby pozniej sprawdzic czy pociski zderzają sie z alienami
        bullets_rects = [pygame.Rect(bp[0], bp[1], 10, 10) for bp in bullets]
        #bp to tymaczasowa zmienna okreslająca element listy i używając np bp[0] (od indeksu 0) to pobieramy aktualną pozycje. dajemy pozniej fora, aby zrobic to dla kazdego bulleta z listy

        # Sprawdzenie kolizji pocisku z każdym przeciwnikiem
        enemies_to_remove = [] # ta sama sytuacja co z bullets_to_remove
        for enemy_pos in enemies: #enemy_pos to tymczasowa nazwa dla kazdego elementu listy
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], 40, 40) #tworzymy rectangla
            #enemy_pos to tymaczasowa zmienna okreslająca element listy i używając np enemy_pos[0] (od indeksu 0) to pobieramy aktualną pozycje aliena.

            #zagniezdazamy fora i dla kazdego enemy sprawdzamy kazdy bullet
            for bullet_rect in bullets_rects: #dla kazdego prostokąta bulleta ze swojej listy
                if bullet_rect.colliderect(enemy_rect): #sprawdzamy czy prostokąt bulleta koliduje z prostokątem enemy
                    bullets_to_remove.append([bullet_rect.x, bullet_rect.y])  # jesli tak to dodajemy 
                    enemies_to_remove.append(enemy_pos)
                    score += 1  # Increase score
                    break  # Stop checking other bullets for this enemy


            #USUWAMIE POCISKÓW
                
        for bullet_pos in bullets_to_remove: #sprawdzamy które pociski z z wyswietlonych znajdują się na lscie do usuniecia i je usuwamy
            if bullet_pos in bullets: #zdarzało się, że gra się wywalała po próbowała usunąć niesistniejący element listy, dlatego jest trakie zabezpieczenie w postaci ifa
                bullets.remove(bullet_pos) #usuwamy niepotrzebne bullety czy to przez wyjscie poza ekran czy uderzenie w aliena

        




            #OBSŁUGA FAL

        #jesli fala (poziom) nie została wystartowana oraz jesli nie ma przeciwnikow na ekranie to  respimy fale
        if not wave and not enemies:
            if level == 4: #jak dojdzeimy do 4 levelu to wygralismy
                exit_game("Zwycięstwo") #wysyłamy stringa do funkcji exit game z komunikatem do wyswietlenia o zwyciestwie
            else:
                spawn_enemies(level) #respimy następną falę
                wave = True #ustawiamy zmienną która sprawi ze ten if na respienie fali wykona się tylko raz na fale a nie co kazdą klatke


        if not enemies and wave: #jesli trwa fala ale nie ma juz przeciwników 
            level += 1 #to zwiekszamy level
            wave = False #ustawiamy z powrotem wartosc fali na false aby aktywował się if powyzej z uruchomieniem kolejnej fali






            #WYSWIETLANIE ENEMY, RUSZANIE NIM I PSRAWDZANIE JEGO KOLIZJI Z GRACZEM
        
        for enemy_pos in enemies: #dla każdego enemy z listy musimy go poruszyć, zwiększając jego koordynaty y
            enemy_pos[1] += enemy_pos[2]  #zwiększamy z każdą klatką wartość y o szybkość speed którą wcześniej ustaliliśmy przy respieniu przeciwników
            
            # wczesniej sprawdzalismy kolizje enemy z pociskiem a teraz sprawdzamy kolizje enemy z graczem
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], 40, 40) #pobieramy z każdego enemy jego pozycję i koordynaty
            player_rect = pygame.Rect(actual_position_x, actual_position_y, 60, 48) #pobieramy aktualną pozycję naszego statku

            if enemy_rect.colliderect(player_rect): #jeśli rectangle statku naszego i enemy sie przecinają:
                lives -= 1 #to dejmujemy jedno życie
                enemies_to_remove.append(enemy_pos) #i dodajemy statek aliena do usunięcia 
                

            
            # jesli nie uderzyl w playera to sprawdzamy czy nie wyleciał poza ekran
            elif enemy_pos[1] > 400:
                enemies_to_remove.append(enemy_pos) #dodajemy go do listy do usunięcia
                lives -= 1 #odejmujemy jedno życie
            
            # jeśli przeciwnik ani nie został wywalony poza mape ani nie zderzył sie z playerem to można go wyswietlic (i ile istnieje)
            screen.blit(alien, (enemy_pos[0], enemy_pos[1]))

            #USUWANIE ENEMY
        for enemy_pos in enemies_to_remove: #sprawdzamy które alieny z z wyswietlonych znajdują się na liscie do usuniecia i je usuwamy
            if enemy_pos in enemies: #zdarzało się, że gra się wywalała po próbowała usunąć niesistniejący element listy, dlatego jest trakie zabezpieczenie w postaci ifa
                enemies.remove(enemy_pos) #usuwamy niepotrzebne alieny czy to przez wyjscie z ekranu czy zastrzelenie pociskiem


        

    else: #jesli nie mamy zyc to konczymy gre z komunikatem game over (wysylamy do funkcji parametr ze stringiem ktory sie nam wyswietli)
        exit_game("Game Over")
        
    # odświeżenie ekranu
    pygame.display.flip()

    # ogranicza FPS do 60
    clock.tick(60)

# zamknięcie programu
pygame.quit()
