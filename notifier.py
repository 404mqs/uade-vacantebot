import yagmail
from plyer import notification
import pyttsx3  # Importa la librería pyttsx3 para TTS

class Notifier:
    def __init__(self, email_user, email_password, email_recipient):
        self.email_user = email_user
        self.email_password = email_password
        self.email_recipient = email_recipient
        self.yag = yagmail.SMTP(email_user, email_password)
        self.tts_engine = pyttsx3.init()  # Inicializa el motor TTS

    def send_email(self, subject, body):
        try:
            self.yag.send(to=self.email_recipient, subject=subject, contents=body)
            print(f"[+] Correo enviado a {self.email_recipient} con el asunto '{subject}'")
        except Exception as e:
            print(f"[?] Error al enviar el correo: {e}")

    def send_desktop_notification(self, title, message):
        try:
            notification.notify(
                title=title,
                message=message,
                app_name='Notifier',
                timeout=10
            )
            print(f"[+] Notificación de escritorio enviada: {title}")
        except Exception as e:
            print(f"[!] Error al enviar la notificación: {e}")

    def speak(self, text):
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            print(f"[+] Notificación hablada: {text}")
        except Exception as e:
            print(f"[!] Error al hablar la notificación: {e}")

    def notify(self, subject, body):
        self.send_email(subject, body)
        self.send_desktop_notification(subject, body)
        self.speak(body)

# Ejemplo de uso
if __name__ == "__main__":
    email_user = 'tu_correo@gmail.com'
    email_password = 'tu_contraseña'
    email_recipient = 'destinatario@gmail.com'
    
    notifier = Notifier(email_user, email_password, email_recipient)

    # Cuando encuentres una vacante
    notifier.notify("Vacante Encontrada", "¡Se ha encontrado una vacante! Revisa el sitio para más detalles.")
