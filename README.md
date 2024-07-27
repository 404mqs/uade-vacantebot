# Detector de Vacantes de Materias UADE

Este script utiliza Selenium para buscar vacantes en las clases de la UADE y notificar al usuario vía email, notificación de escritorio y voz.

## Características

- Búsqueda automática de vacantes en clases específicas
- Notificaciones por email
- Notificaciones de escritorio
- Notificaciones por voz
- Configuración personalizable

## Instalación

```1.``` Clona este repositorio o descarga los archivos.

```2.``` Instala las dependencias: ```pip install -r requirements.txt```

```3```. Descarga el driver de Selenium para Chrome:
- Visita [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/#stable)
- Descarga la versión compatible con tu versión de Chrome
- Descomprime el archivo y guarda el ejecutable en una ubicación conocida

## Configuración

Edita el archivo `config.ini` con tus datos:

```
[settings]
driver_path = /path/to/chromedriver
; Path al Driver Selenium
uade_user = your_uade_user
; Usuario de UADE
uade_pass = your_uade_pass
; Pass de UADE
uade_turno = NOCHE
; Turno a buscar (uade no permite buscar en mas de 1 turno a la vez) MAÑANA, TARDE, NOCHE, INTENSIVO o VIRTUAL
email_user = your_email_user
; Mail que van a usar para las notificaciones
email_password = your_email_password
; Contraseña SMTP del mail que van a usar para las notificaciones
email_recipient = your_email_recipient
; Mail que van a usar para ser notificados
intervalo_chequeo = 5
; Intervalo de chequeo de materias en segundos
modo_repetitivo = True
; Modo Repeticion

[materias]
materias_a_seleccionar = 3.4.212, 3.4.216
; Materias a buscar

[ignorar]
codigos_a_ignorar = 14045, 12363
; Cursos que quieren ignorar / evitar (ej, ignorar a un curso con un profesor X)
```

### Campos obligatorios:
- driver_path: Ruta al ejecutable de ChromeDriver
- uade_user: Tu usuario de UADE
- uade_pass: Tu contraseña de UADE
- uade_turno: Turno a buscar (MAÑANA, TARDE, NOCHE, INTENSIVO o VIRTUAL)
- intervalo_chequeo: Tiempo entre chequeos en segundos (por defecto 10)
- modo_repetitivo: True para continuar buscando después de encontrar una vacante, False para detenerse

### Campos opcionales (pero recomendados):
- email_user: Email para enviar notificaciones
- email_password: Contraseña SMTP del email
- email_recipient: Email donde recibirás las notificaciones
### Configuración de materias:
- materias_a_seleccionar: Códigos de las materias a buscar, separados por comas
- codigos_a_ignorar: Códigos de cursos a ignorar, separados por comas

## Uso
Ejecuta el script: ```python main.py``` luego de aplicar la configuracion.

### Notas
- Asegúrate de tener una conexión a internet estable.
- Las notificaciones por email requieren configuración adicional en tu cuenta de correo para permitir el acceso de aplicaciones menos seguras.
- El modo repetitivo es útil si buscas vacantes en varias materias, pero puede generar múltiples notificaciones.


