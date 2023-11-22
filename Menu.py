import inquirer
import sys
import os
import argparse

class Menu:
    def __init__(self, nginx_manager):
        self.nginx_manager = nginx_manager

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
                        "Editar sitio",
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
            elif answers["action"] == "Salir":
                # clear console
                os.system("clear")
                exit()
                        
        except KeyboardInterrupt:
            os.system("clear")
            print("\nOperación cancelada por el usuario. Saliendo...")
            exit(0)