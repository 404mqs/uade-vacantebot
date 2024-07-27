import configparser
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from elements_manager import get_xpath
from notifier import Notifier  

# Leer configuración desde el archivo config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Obtener la configuración
driver_path = config.get('settings', 'driver_path')
uade_user = config.get('settings', 'uade_user')
uade_pass = config.get('settings', 'uade_pass')
uade_turno = config.get('settings', 'uade_turno')
email_user = config.get('settings', 'email_user')
email_password = config.get('settings', 'email_password')
email_recipient = config.get('settings', 'email_recipient')
intervalo_chequeo = config.getint('settings', 'intervalo_chequeo')
modo_repetitivo = config.getboolean('settings', 'modo_repetitivo')  # Leer configuración de modo repetitivo

# Leer listas de materias y códigos a ignorar
materias_a_seleccionar = [item.strip() for item in config.get('materias', 'materias_a_seleccionar').split(',')]
codigos_a_ignorar = [item.strip() for item in config.get('ignorar', 'codigos_a_ignorar').split(',')]

# Configuración del servicio de ChromeDriver
service = Service(driver_path)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')  # Ejecutar en modo headless
options.add_argument('--disable-gpu')  # Desactivar la GPU (a veces necesario en modo headless)
options.add_argument('--window-size=1920x1080')  # Tamaño de ventana para evitar errores

# Inicializa el navegador con el servicio especificado
driver = webdriver.Chrome(service=service, options=options)

# Configura el notificador
notifier = Notifier(email_user, email_password, email_recipient)

os.system("cls")

def extract_course_name(text):
    # Encontrar la posición del guion y el espacio siguiente
    delimiter_index = text.find(' - ')
    if delimiter_index != -1:
        # Extraer la parte después del guion
        return text[delimiter_index + 3:].strip()
    return text.strip()

def scrape_data(codigos_materias, codigos_ignorar):
    # Abre la URL en el navegador
    driver.get(f'https://{uade_user}:{uade_pass}@inscripcionespia.uade.edu.ar/InscripcionClaseBuscar.aspx?param=D5o2MtoGiK0%3d-P0lkU2Vzc2lvbj0scGFyYW1BbHVtSWQ9Mjk2MTgyLHBhcmFtTml2QWNhZD0xMzAscGFyYW1BbmlvQ2FsZW5kYXJpbz0yMDI0LHBhcmFtQ3VhdHJpbWVzdHJlPTU5NyxwYXJhbVNlZGU9MSxwYXJhbVRpcG9BZG1pbj0zNDAzMCxwYXJhbVRpcG9JbnZvY2Fkb3I9MixwYXJhbVByaVZlej0xLHBhcmFtT2ZyZWNpbWllbnRvPQ%3d%3d')
    os.system("cls")

    print("[++] ---- DETECTOR DE VACANTES UADE ---- [++]\n")

    stop = False  # Inicializa stop aquí

    try:
        # Hacer clic en el elemento "Seleccione sus Mater..."
        driver.find_element(By.XPATH, get_xpath(driver,'KCOLYNpPpspdc6u')).click()

        # Esperar a que la página se cargue completamente
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ContentPlaceHolder1_ucMateriaInscripcionBuscador_rptMaterias_grdMaterias_0"))
        )

        for codigo_materia in codigos_materias:
            try:
                # Buscar el checkbox de la materia por su código
                checkbox_xpath = f"//td[contains(@class, 'colCodigo') and text()='{codigo_materia}']/preceding-sibling::td[contains(@class, 'colAcciones')]//input[@type='checkbox']"
                
                # Esperar a que el checkbox esté presente en el DOM
                checkbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, checkbox_xpath))
                )

                # Hacer scroll hasta el elemento para asegurarnos de que es visible
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)

                # Usar JavaScript para hacer clic en el checkbox
                driver.execute_script("arguments[0].click();", checkbox)
                print(f"[!] Checkbox de la materia con código {codigo_materia} seleccionado exitosamente.\n")
            
            except Exception as e:
                print(f"Error al seleccionar la materia con código {codigo_materia}: {str(e)}")

        # Hacer clic en el elemento "Cerrar"
        driver.find_element(By.XPATH, get_xpath(driver,'udAzQeon0tR0N2S')).click()

        # Seleccionar el turno
        select_element = driver.find_element(By.XPATH, '//*[@id="ContentPlaceHolder1_cboTurno"]')
        select = Select(select_element)
        select.select_by_visible_text(uade_turno)

        time.sleep(2)

        # Marca todos los checkboxes si no están ya seleccionados
        checkboxes = driver.find_elements(By.XPATH, '//td//input[@type="checkbox"]')
        for checkbox in checkboxes:
            if not checkbox.is_selected():
                try:
                    checkbox.click()
                except:
                    pass

        # Encuentra y clic en el botón "Buscar"
        buscar_button = driver.find_element(By.ID, 'ContentPlaceHolder1_btnBuscar')
        buscar_button.click()

        time.sleep(2)  # Espera a que se cargue la tabla

        # Encuentra la tabla general que contiene todas las materias
        materias = driver.find_elements(By.CLASS_NAME, "anio")

        for index, materia in enumerate(materias):
            if materia.text.strip():
                print("\n-------------------------------------------------")
                print(f"\nMateria: {materia.text}\n")

                # Encuentra la tabla de clases para esta materia
                tabla_id = f"ContentPlaceHolder1_rptMateriaClases_grdClases_{index}_grdResultados_{index}"
                try:
                    tabla = driver.find_element(By.ID, tabla_id)

                    # Obtiene las filas de la tabla
                    rows = tabla.find_elements(By.TAG_NAME, "tr")

                    for row in rows:
                        columns = row.find_elements(By.TAG_NAME, "td")
                        column_data = [column.text for column in columns]
                        if len(column_data) != 0 and column_data[1] not in codigos_ignorar:
                            print(column_data)
                            if int(column_data[14]) > 0:
                                print(f"[!] Vacantes encontradas para la clase {extract_course_name(column_data[1])}!")

                                # Construir el mensaje con el f-string
                                message = f"¡Se ha encontrado una vacante para {extract_course_name(materia.text)}! Revisa inscripciones."

                                notifier.notify("Vacante Encontrada", message)
                                stop = True

                except Exception as e:
                    pass

        if stop:
            print("\n[+] VACANTE ENCONTRADA. :D")
            # Llama al método notify para enviar notificaciones
            return 1

        # Si no se encontró vacante, devuelve 0
        return 0

    except Exception as e:
        print(f"Se produjo un error: {e}")
        return 0

# Bucle para actualizar la página según el modo definido
if modo_repetitivo:
    while True:
        scrape_data(materias_a_seleccionar, codigos_a_ignorar)
        print("\n[!] Reanudando bucle...\n")
        time.sleep(intervalo_chequeo)  # Espera según el intervalo definido
        os.system('cls')
else:
    while True:
        resultado = scrape_data(materias_a_seleccionar, codigos_a_ignorar)
        if resultado == 1:
            break
        print("\n[!] Reanudando bucle...\n")
        time.sleep(intervalo_chequeo)  # Espera según el intervalo definido
        os.system('cls')


