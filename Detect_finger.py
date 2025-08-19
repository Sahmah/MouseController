import mediapipe as mp  # Biblioteca MediaPipe para detecção de mãos e rastreamento de landmarks

class DetectFinger:
    # mp.solutions.hands contém os módulos do MediaPipe para detectar mãos
    mp_hands = mp.solutions.hands

    # mp.solutions.drawing_utils contém funções para desenhar landmarks e conexões
    mp_draw = mp.solutions.drawing_utils

    # Inicializa o objeto Hands do MediaPipe
    # max_num_hands=1 limita a detecção a apenas 1 mão
    hands = mp_hands.Hands(max_num_hands=1)
