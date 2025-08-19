import math          # Biblioteca para funções matemáticas, calcular distância
import pyautogui     # Biblioteca para controlar o mouse e o teclado via Python

class Click:
    # Variáveis de classe para armazenar a posição anterior do mouse
    # Necessário para aplicar o filtro exponencial e suavizar o movimento
    prev_x = 0
    prev_y = 0
    alpha = 0.3  # fator de suavização do filtro exponencial (quanto menor, mais suave)

    # Decorador @staticmethod indica que este método não depende da instância da classe
    # Chama Click.move_and_click diretamente, sem criar objeto
    @staticmethod
    def move_and_click(hand_landmarks, frame):
        """
        Recebe os landmarks da mão e o frame da webcam,
        calcula a posição do dedo indicador na tela, move o mouse
        e realiza clique quando dedo indicador e médio estão próximos.
        """

        # Pega coordenadas do dedo indicador (landmark 8)
        # hand_landmarks.landmark[8].x/y são valores normalizados (0 a 1)
        # Multiplica pelo tamanho do frame para converter em pixels da imagem
        x = int(hand_landmarks.landmark[8].x * frame.shape[1])
        y = int(hand_landmarks.landmark[8].y * frame.shape[0])

        # Converte para coordenadas da tela do computador
        # screen_width e screen_height são a resolução do monitor
        screen_width, screen_height = pyautogui.size()
        screen_x = int(x / frame.shape[1] * screen_width)
        screen_y = int(y / frame.shape[0] * screen_height)

        # Aplica filtro exponencial para suavizar movimentos
        # A ideia: o mouse segue a nova posição suavemente
        # screen_x = prev_x + (nova_posicao - prev_x) * alpha
        screen_x = int(Click.prev_x + (screen_x - Click.prev_x) * Click.alpha)
        screen_y = int(Click.prev_y + (screen_y - Click.prev_y) * Click.alpha)

        # Atualiza as variáveis de classe com a nova posição filtrada
        Click.prev_x, Click.prev_y = screen_x, screen_y

        # Move o mouse pra posição calculada
        # pyautogui.moveTo(x, y) move o cursor do mouse instantaneamente
        pyautogui.moveTo(screen_x, screen_y)

        # Calcula distância entre dedo indicador (8) e dedo médio (12)
        # Determina se vai realizar um clique
        x2 = int(hand_landmarks.landmark[12].x * frame.shape[1])
        y2 = int(hand_landmarks.landmark[12].y * frame.shape[0])
        distance = math.hypot(x2 - x, y2 - y)  # calcula a distância Euclidiana

        # Realiza clique se os dedos estiverem próximos
        # Ajuste do threshold (30 pixels) pode ser alterado 
        if distance < 30:
            pyautogui.click()

