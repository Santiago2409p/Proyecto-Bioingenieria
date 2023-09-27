import speech_recognition as sr

def main():
    # Inicializa el reconocedor
    recognizer = sr.Recognizer()

    # Captura el audio del micrófono
    with sr.Microphone() as source:
        print("Por favor, di un comando: (adelante, freno, izquierda, derecha)")
        
        try:
            # Escucha el audio del micrófono
            audio_data = recognizer.listen(source, timeout=5)

            # Reconoce el audio usando Google Web Speech API
            text = recognizer.recognize_google(audio_data).lower()

            # Verifica el comando
            if "forward" in text:
                print("Moviéndose hacia adelante.")
            elif "break" in text: #brake
                print("Frenando.")
            elif "left" in text:
                print("Girando a la izquierda.")
            elif "right" in text:
                print("Girando a la derecha.")
            else:
                print(f"Comando no reconocido: {text}")

        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado.")
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"Error en la solicitud; {e}")

if __name__ == "__main__":
    main()
