import inquirer
import sys
import os
import argparse

class Menu:
    def __init__(self, nginx_manager, mariaDbInstaller):
        self.nginx_manager = nginx_manager
        self.mariaDbInstaller = mariaDbInstaller

    def show_menu(self):
        try:
            questions = [
                inquirer.List(
                    "action",
                    message="¿Qué acción te gustaría realizar?",
                    choices=[
                        "Habilitar un sitio",
                        "Deshabilitar un sitio",
                        "Listar todos los sitios",
                        "Crear un nuevo sitio",
                        "Mostrar opciones del sitio",
                        "Instalar MariaDB",
                        "Cambiar contraseña de root de MariaDB",
                        "Salir",
                    ],
                ),
            ]
            answers = inquirer.prompt(questions)

            if answers is None:
                raise KeyboardInterrupt

            if answers["action"] == "Habilitar un sitio":
                self.nginx_manager.enable_site()
            elif answers["action"] == "Deshabilitar un sitio":
                self.nginx_manager.disable_site()
            elif answers["action"] == "Listar todos los sitios":
                self.nginx_manager.list_sites()
            elif answers["action"] == "Crear un nuevo sitio":
                self.nginx_manager.create_new_site()
            elif answers["action"] == "Editar sitio":
                self.nginx_manager.modify_site()
            elif answers["action"] == "Mostrar opciones del sitio":
                self.nginx_manager.show_varsSite()
            elif answers["action"] == "Instalar MariaDB":
                self.mariaDbInstaller.install_mariadb()
            elif answers["action"] == "Cambiar contraseña de root de MariaDB":
                self.mariaDbInstaller.change_root_password()
            elif answers["action"] == "Salir":
                # clear console
                os.system("clear")
                exit()
                        
        except KeyboardInterrupt:
            os.system("clear")
            print("\nOperación cancelada por el usuario. Saliendo...")
            exit(0)
