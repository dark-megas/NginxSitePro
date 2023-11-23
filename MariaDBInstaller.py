import os
import subprocess

class MariaDBInstaller:
    def __init__(self):
        # Constructor, puede incluir configuraciones iniciales si es necesario
        pass

    def install_mariadb(self):
        # Este método instala MariaDB en el servidor
        try:
            print("Iniciando la instalación de MariaDB...")
            os.system('sudo apt update')
            os.system('sudo apt install mariadb-server')
            print("MariaDB instalado con éxito.")
            self.configure_mariadb()
            self.menu.show_menu()
        except Exception as e:
            print(f"Error al instalar MariaDB: {e}")

    def change_root_password(self):
        # Este método cambia la contraseña del usuario root de MariaDB
        try:
            password = input("Ingresa la contraseña de root de MariaDB: ")
            new_password = password
            os.system(f'mysqladmin -u root password "{new_password}"')
            print("La contraseña de root de MariaDB ha sido cambiada con éxito.")
        except Exception as e:
            print(f"Error al cambiar la contraseña: {e}")

    def configure_mariadb(self):
        # Este método realiza una configuración básica de MariaDB
        try:
            default_root_password = "password"
            print("Configurando MariaDB...")
            commands = [
                f"SET PASSWORD FOR 'root'@'localhost' = PASSWORD('{default_root_password}');",
                "DELETE FROM mysql.user WHERE User='';",
                "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');",
                "DROP DATABASE IF EXISTS test;",
                "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';",
                "FLUSH PRIVILEGES;"
            ]
            command_string = " && ".join(f"mysql -u root -e \"{cmd}\"" for cmd in commands)
            os.system(f'echo "{command_string}" | sudo bash')
            print("MariaDB configurado con éxito.")
        except Exception as e:
            print(f"Error al configurar MariaDB: {e}")

    def set_menu(self, menu):
        self.menu = menu