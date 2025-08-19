import cv2                     # Biblioteca OpenCV para acessar a webcam e processar imagens
from Detect_finger import DetectFinger  # Classe que inicializa MediaPipe para detectar mãos
from Click import Click         # Classe que controla o movimento e clique do mouse

class WebCam:
    # Decorador @staticmethod indica que o método não precisa de uma instância da classe
    @staticmethod
    def capture():
        """
        Captura imagens da webcam em tempo real, detecta mãos e
        controla o mouse com base na posição do dedo indicador.
        """
        cap = cv2.VideoCapture(0)  # 0 indica a webcam padrão do computador
        
        while True:
            ret, frame = cap.read()  # Lê um frame da câmera
            if not ret:              # Se não conseguir ler, sai do loop
                break
            
            # Converte o frame de BGR (OpenCV) para RGB (MediaPipe)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Processa o frame para detectar mãos
            result = DetectFinger.hands.process(frame_rgb)
            
            # Se alguma mão foi detectada
            if result.multi_hand_landmarks:
                # Percorre 1 mão detectada
                for hand_landmarks in result.multi_hand_landmarks:
                    # Desenha landmarks e conexões na imagem original
                    DetectFinger.mp_draw.draw_landmarks(
                        frame, hand_landmarks, DetectFinger.mp_hands.HAND_CONNECTIONS
                    )

                    # Pega coordenadas da ponta do dedo indicador (landmark 8)
                    x = int(hand_landmarks.landmark[8].x * frame.shape[1])
                    y = int(hand_landmarks.landmark[8].y * frame.shape[0])
                    # Desenha um círculo azul no dedo indicador
                    cv2.circle(frame, (x, y), 10, (255, 0, 0), cv2.FILLED)

                    # Move o mouse e verifica clique usando a classe Click
                    Click.move_and_click(hand_landmarks, frame)
                        
            # Exibe o frame processado em uma janela chamada "Webcam"
            cv2.imshow("Webcam", frame)
            
            # Sai do loop se a tecla 'q' for pressionada
            if cv2.waitKey(1) == ord('q'):
                break
        
        # Libera a câmera e fecha todas as janelas
        cap.release()
        cv2.destroyAllWindows()

# Executa a captura da webcam
WebCam.capture()
