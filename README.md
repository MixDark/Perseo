# Perseo

## Descripción
Es un keylogger que captura el teclado, ofuscando el contenido del archivo en base64, se camufla en el sistema de Windows para simular legitimidad y envia el reporte al correo electrónico. Tambien cuenta con un módulo para decodificar la información del archivo ofuscado.

## Capturas de pantalla
![image](https://github.com/user-attachments/assets/9755b24c-9919-45c7-8cb1-537a0635a0d4)

Decodificador

![image](https://github.com/user-attachments/assets/b1de8eff-34c4-44c8-bb2e-d6b47f385c18)

Correo enviado 

![image](https://github.com/user-attachments/assets/faeef2ed-8887-4386-8d4e-6d465de29bb4)

Contenido en base64

![image](https://github.com/user-attachments/assets/4eb69378-f092-4efa-b38c-7889e5e79e81)

Contenido en texto plano 

![image](https://github.com/user-attachments/assets/3a3bd320-718d-417b-b3d0-5adc867529b0)

## Características
- Es compatible con Windows
- Es Compatible con Linux, pero puede requerir permisos de superusuario
- Contenido ofuscado en base64
- Camuflaje como archivo del sistema 
- Envia el reporte al correo electrónico
- Incluye decodificador base64
- Interfaz simple e intuitiva

## Requerimientos
- Python 3.x 
- colorama
- keyboard

## Configuración del archivo .env
Crea el archivo .env en la misma carpeta del script con la estructura que se muestra en el ejemplo, reemplaza los valores con los datos solicitados, para crear la contraseña de aplicación en Gmail sigue los pasos del video https://www.youtube.com/watch?v=xnbGakU7vhE

EMAIL_USER=tucorreodeorigen  
EMAIL_PASSWORD=tucontraseñadeaplicacion  
EMAIL_RECEIVER=tucorreodedestino

## Instalación desde CLI
1. Clona el repositorio: 
git clone https://github.com/MixDark/Perseo.git
2. Instala las dependencias:
pip install -r requirements.txt
3. Ejecuta la aplicación:
python perseo.py

## Uso
1. Ejecuta el script, presione la tecla Esc en el momento que se desee finalizar
2. Espera a que llegue correo electronico
3. Tambien puede buscar el archivo ofuscado en la siguiente ruta %APPDATA%\\Microsoft\\Windows\\SystemUpdate\\syslog.dat
4. Ejecute el decodificador y siga las instrucciones para ver el contenido
5. El archivo en texto plano se guarda en la misma del ruta que el decodificador

## Descargo de responsabilidad
Este script fue creado para simular una situación en la que la gran mayorias de usuarios guardan las contraseñas en el navegador, su uso es para fines educativos y en caso de ser usado con fines maliciosos puede traer consecuencias legales en base a la leyes existentes en cada país.
