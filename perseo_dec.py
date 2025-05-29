import base64
import os
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def print_banner():

    perseo_decoder_ascii = r"""
    ██████╗ ███████╗██████╗ ███████╗███████╗ ██████╗ 
    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔═══██╗
    ██████╔╝█████╗  ██████╔╝███████╗█████╗  ██║   ██║
    ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██╔══╝  ██║   ██║
    ██║     ███████╗██║  ██║███████║███████╗╚██████╔╝
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ 
    ██████╗ ███████╗ ██████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔══██╗
    ██║  ██║█████╗  ██║     ██║   ██║██║  ██║█████╗  ██████╔╝
    ██║  ██║██╔══╝  ██║     ██║   ██║██║  ██║██╔══╝  ██╔══██╗
    ██████╔╝███████╗╚██████╗╚██████╔╝██████╔╝███████╗██║  ██║
    ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    
     # Información adicional
    subtitle = "Decodificador de archivo"
    author = "Creado por Mix Dark"
    date_info = f"Fecha: 29-05-2025"
    version = "Versión: 1.0"
    
    # Línea decorativa
    border = Fore.WHITE + "=" * 65
    
    # Imprimir banner
    print(Fore.WHITE + perseo_decoder_ascii)
    print(border)
    
  # Información centrada
    print(Fore.WHITE  + Style.BRIGHT + subtitle.center(50))
    print(Fore.WHITE  + author.center(50))
    print(Fore.WHITE  + date_info.center(50))
    print(Fore.WHITE + f"{version}".center(50))
    print(border + "\n")

def decodificar_archivo_predeterminado():

    try:
        # Ubicación predeterminada del archivo ofuscado
        appdata_path = os.getenv('APPDATA')
        archivo_entrada = os.path.join(appdata_path, "Microsoft", "Windows", "SystemUpdate", "syslog.dat")
        
        # Verificar que el archivo de entrada existe
        if not os.path.isfile(archivo_entrada):
            print(Fore.RED + "Error: El archivo de registro no existe en la ubicación predeterminada:")
            print(Fore.YELLOW + f"{archivo_entrada}")
            return False
        
        # Procesar el archivo
        return procesar_archivo(archivo_entrada)
        
    except Exception as e:
        print(Fore.RED + f"Error al recuperar los datos: {str(e)}")
        return False

def decodificar_archivo_personalizado(ruta):

    try:
        # Verificar que el archivo de entrada existe
        if not os.path.isfile(ruta):
            print(Fore.RED + "Error: El archivo no existe en la ruta especificada:")
            print(Fore.YELLOW + f"{ruta}")
            return False
        
        # Procesar el archivo
        return procesar_archivo(ruta)
        
    except Exception as e:
        print(Fore.RED + f"Error al recuperar los datos: {str(e)}")
        return False

def procesar_archivo(archivo_entrada):

    try:
        # Determinar el nombre del archivo de salida
        archivo_salida = "registro.txt"
        
        # Leer el contenido ofuscado
        with open(archivo_entrada, 'r', encoding='utf-8') as f:
            contenido_ofuscado = f.read().strip()
        
        # Verificar que el contenido no está vacío
        if not contenido_ofuscado:
            print(Fore.RED + "El archivo está vacío.")
            return False
        
        try:
            # Decodificar el contenido
            contenido_bytes = base64.b64decode(contenido_ofuscado)
            contenido_original = contenido_bytes.decode('utf-8')
            
            # Guardar el contenido decodificado en la carpeta actual
            with open(archivo_salida, 'w', encoding='utf-8') as f:
                f.write(contenido_original)
            
            ruta_completa = os.path.abspath(archivo_salida)
            print(Fore.GREEN + "\n✅ Datos decodificados exitosamente.")
            print(Fore.GREEN + f"📄 Resultado guardado en: {ruta_completa}")
            return True
            
        except base64.binascii.Error:
            print(Fore.RED + "Error: El contenido del archivo no está en formato válido.")
            return False
        
    except Exception as e:
        print(Fore.RED + f"Error al procesar el archivo: {str(e)}")
        return False

def mostrar_menu():

    print(Fore.CYAN + "\nOpciones disponibles:")
    print(Fore.WHITE + "1. Buscar archivo en ubicación predeterminada")
    print(Fore.YELLOW + "   (%APPDATA%\\Microsoft\\Windows\\SystemUpdate\\syslog.dat)")
    print(Fore.WHITE + "2. Especificar ruta personalizada del archivo")
    print(Fore.WHITE + "3. Salir")
    
    opcion = input(Fore.CYAN + "\n→ Seleccione una opción (1-3): " + Fore.WHITE)
    
    if opcion == "1":
        print(Fore.YELLOW + "\nBuscando en ubicación predeterminada...")
        decodificar_archivo_predeterminado()
    elif opcion == "2":
        ruta = input(Fore.YELLOW + "\nIngrese la ruta completa del archivo: " + Fore.WHITE)
        decodificar_archivo_personalizado(ruta)
    elif opcion == "3":
        print(Fore.YELLOW + "\nSaliendo del programa...")
        return False
    else:
        print(Fore.RED + "\n❌ Opción no válida. Por favor, seleccione una opción del 1 al 3.")
    
    return True

if __name__ == "__main__":
    # Mostrar el banner
    print_banner()
    
    continuar = True
    
    while continuar:
        continuar = mostrar_menu()
        
        if continuar:
            input(Fore.CYAN + "\nPresione Enter para continuar..." + Fore.RESET)