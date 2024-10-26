import pygame
import random

# Oyun ayarları
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000
CARD_WIDTH = 200
CARD_HEIGHT = 200
MARGIN = 10
ROWS = 5
COLS = 4

# Zaman limiti (saniye cinsinden)
TIME_LIMIT = 60  # 60 saniye

# Renkler
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Kart görsellerini yükleme ve boyutlandırma
def load_and_scale_image(filename):
    image = pygame.image.load(filename)
    return pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT))

# Kart çiftlerini oluştur
def create_pairs():
    return [
        load_and_scale_image('dog.png'),
        load_and_scale_image('cat.png'),
        load_and_scale_image('rabbit.png'),
        load_and_scale_image('pig.png'),
        load_and_scale_image('frog.png'),
        load_and_scale_image('lion.png'),
        load_and_scale_image('koala.png'),
        load_and_scale_image('tiger.png'),
        load_and_scale_image("zebra.png"),
        load_and_scale_image("giraffe.png")
    ] * 2  # Her bir görüntüyü iki kez ekleyerek toplam 16 kart oluşturuyoruz.

# Kartları karıştır
def shuffle_cards(cards):
    random.shuffle(cards)
    return cards

# Kart sınıfı
class Card:
    def __init__(self, image):
        self.image = image
        self.revealed = False

    def draw(self, screen, x, y):
        if self.revealed:
            screen.blit(self.image, (x, y))
        else:
            pygame.draw.rect(screen, GRAY, (x, y, CARD_WIDTH, CARD_HEIGHT))

def play_music():
    pygame.mixer.music.load('antony.wav')  # Kendi müzik dosyanızın yolunu girin
    pygame.mixer.music.play(-1)  # Sonsuz döngüde çal

# Oyun döngüsü
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Eşleştirme Oyunu")
    play_music()
    
    cards = shuffle_cards(create_pairs())
    card_objects = [Card(image) for image in cards]

    # Kontrol: Kart nesneleri sayısının doğru olduğunu doğrulayın
    if len(card_objects) != ROWS * COLS:
        print("Hata: Kart sayısı ve grid boyutları uyuşmuyor!")
        return  # Hata durumunda oyunu başlatma

    first_selection = None
    second_selection = None
    pairs_found = 0
    running = True
    start_ticks = pygame.time.get_ticks()  # Başlangıç zamanı
    font = pygame.font.Font(None, 74)  # Font tanımı

    while running:
        screen.fill(WHITE)

        # Kalan süreyi hesapla
        seconds = TIME_LIMIT - (pygame.time.get_ticks() - start_ticks) // 1000
        
        # Süre dolmuşsa oyunu bitir
        if seconds <= 0:
            print("Zaman doldu!")
            running = False

        # Süreyi sağ üst köşede göster
        timer_text = font.render(f'Time: {seconds}', True, (0, 0, 0))
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 10))  # Sağ üst köşeye yerleştiriyoruz

        for i in range(ROWS):
            for j in range(COLS):
                index = i * COLS + j
                
                # Geçerli indeks kontrolü
                if index < len(card_objects):
                    card = card_objects[index]
                    card.draw(screen, j * (CARD_WIDTH + MARGIN), i * (CARD_HEIGHT + MARGIN))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                col = x // (CARD_WIDTH + MARGIN)
                row = y // (CARD_HEIGHT + MARGIN)
                index = row * COLS + col
                
                # Geçerli bir indeks olup olmadığını kontrol et
                if index < len(card_objects) and not card_objects[index].revealed:
                    card_objects[index].revealed = True
                    
                    if first_selection is None:
                        first_selection = index
                    elif second_selection is None:
                        second_selection = index

        if first_selection is not None and second_selection is not None:
            if card_objects[first_selection].image == card_objects[second_selection].image:
                pairs_found += 1
            else:
                pygame.time.wait(1000)  # 1 saniye bekle
                card_objects[first_selection].revealed = False
                card_objects[second_selection].revealed = False
            first_selection = None
            second_selection = None

        pygame.display.flip()

        if pairs_found == len(card_objects) // 2:
            print("Tebrikler! Tüm eşleşmeleri buldunuz!")
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
