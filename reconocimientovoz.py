import speech_recognition as sr
import tkinter as tk

# Función para cambiar el color del cuadrado a verde
def cambiar_color_verde():
    square.configure(bg="green")

# Función para cambiar el color del cuadrado a rojo
def cambiar_color_rojo():
    square.configure(bg="red")

# Función para manejar los comandos de voz en español
def manejar_comandos():
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 4000  # Puedes ajustar este valor según tu entorno
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Ajustar el nivel de ruido
        
        print("Por favor, di un comando: (adelante, freno, izquierda, derecha)")
        
        try:
            audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio_data, language="es-ES").lower()
            
            print("Comando reconocido:", text)  # Imprimir el comando reconocido en la terminal
            
            if "adelante" in text or "freno" in text or "izquierda" in text or "derecha" in text:
                cambiar_color_verde()
            else:
                cambiar_color_rojo()
        
        except sr.WaitTimeoutError:
            print("Tiempo de espera agotado.")
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
        except sr.RequestError as e:
            print(f"Error en la solicitud: {e}")

# Configurar la ventana
root = tk.Tk()
root.title("Control de Cuadrados")

# Crear cuadrados
square = tk.Label(root, width=10, height=5, bg="white")
square.pack(pady=20)

# Botón para iniciar el reconocimiento de voz
start_button = tk.Button(root, text="Iniciar", command=manejar_comandos)
start_button.pack()

# Iniciar la aplicación
root.mainloop()
