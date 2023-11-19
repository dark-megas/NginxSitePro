# Gestor de Sitios para Nginx

Este proyecto es un script en Python diseñado para facilitar la gestión de sitios en un servidor Nginx. Permite habilitar, deshabilitar, listar, crear y editar sitios de forma interactiva.

## Características

- Habilitar y deshabilitar sitios en Nginx.
- Listar todos los sitios habilitados.
- Crear nuevos sitios con configuraciones predefinidas para diferentes tipos de proyectos.
- Editar la configuración de sitios existentes.
- Interfaz de usuario interactiva para una fácil gestión.

## Requisitos

- Python 3
- Nginx
- `inquirer` Python package
- `subprocess` Python package
- `os` Python package
- `argparse` Python package
- `time` Python package
- `re` Python package

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
El script se puede ejecutar en modo interactivo simplemente ejecutándolo sin argumentos

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
