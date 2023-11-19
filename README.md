# Gestor de Sitios para Nginx

Este proyecto es un script en Python diseñado para facilitar la gestión de sitios en un servidor Nginx. Permite habilitar, deshabilitar, listar, crear y editar sitios de forma interactiva y también mediante argumentos de línea de comandos.

## Características

- Habilitar y deshabilitar sitios en Nginx de forma interactiva o mediante argumentos de línea de comandos.
- Listar todos los sitios habilitados.
- Crear nuevos sitios con configuraciones predefinidas para diferentes tipos de proyectos, tanto de forma interactiva como por comandos.
- Editar la configuración de sitios existentes de manera interactiva o a través de argumentos de línea de comandos.
- Interfaz de usuario interactiva para una fácil gestión y opción de manejo mediante comandos para automatización.

## Requisitos

- Python 3
- Nginx
- Paquetes de Python: inquirer, subprocess, os, argparse, time, re

## Instalación y Uso

1. Clona el repositorio en tu servidor:
   ```bash
   git clone https://github.com/dark-megas/NginxSitePro.git
2. Navega al directorio del proyecto:
    ```bash
    cd [nombre_carpeta]
3. Ejecuta el script:
    ```bash
    python3 nsp.py
## Uso
El script se puede ejecutar en modo interactivo simplemente ejecutándolo sin argumentos.

## Uso mediante Argumentos de Línea de Comandos
- --enable [nombre_sitio]: Habilita un sitio específico.
- --disable [nombre_sitio]: Deshabilita un sitio específico.
- --list: Lista todos los sitios disponibles y su estado.
- --create [nombre_sitio] [versión_php] [tipo_proyecto]: Crea un nuevo sitio con los parámetros especificados.
- --modify [nombre_sitio] [nuevo_nombre_servidor] [nuevo_root] [nueva_versión_php]: Modifica la configuración de un sitio existente.

## Ejemplos de Comandos
    python3 nsp.py --enable ejemplo.com
    python3 nsp.py --disable ejemplo.com
    python3 nsp.py --list
    python3 nsp.py --create ejemplo.com 7.4 Laravel
    python3 nsp.py --modify ejemplo.com nuevo-ejemplo.com /var/www/nuevo /usr/bin/php7.4

## Comandos Disponibles

- Habilitar un sitio: Selecciona y habilita un sitio de Nginx.
- Deshabilitar un sitio: Selecciona y deshabilita un sitio de Nginx.
- Listar todos los sitios: Muestra una lista de todos los sitios habilitados.
- Crear un nuevo sitio: Asistente para crear un nuevo sitio.
- Editar sitio: Modifica la configuración de un sitio existente.
- Mostrar opciones del sitio: Muestra la configuración actual de un sitio.
- Salir: Sale del script.

## Contribuciones
Las contribuciones son bienvenidas. Por favor, envía tus pull requests a https://github.com/dark-megas/NginxSitePro.git.
