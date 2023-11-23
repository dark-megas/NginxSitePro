import os
import subprocess

class PHPInstaller:
    def __init__(self):
        # Constructor, puede incluir configuraciones iniciales si es necesario
        pass

    def install_php(self):
        """ Instala una versión específica de PHP. """
        try:
            version = input("Ingresa la versión de PHP que deseas instalar: ")
            print(f"Iniciando la instalación de PHP {version}...")
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', f'php{version}', '-y'], check=True)
            print(f"PHP {version} instalado con éxito.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar PHP {version}: {e}")

    def configure_php(self, config_file, settings):
        """ Realiza cambios en la configuración de PHP. """
        try:
            print(f"Configurando PHP utilizando el archivo {config_file}...")
            with open(config_file, 'a') as file:
                for setting in settings:
                    file.write(f"{setting}\n")
            print("Configuración de PHP actualizada.")
        except Exception as e:
            print(f"Error al configurar PHP: {e}")
