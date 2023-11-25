import os
import subprocess
import re
import time
import Menu
import inquirer

class NginxManager:
    def __init__(self):
        self.sites_available_path = "/etc/nginx/sites-available"
        self.sites_enabled_path = "/etc/nginx/sites-enabled"
        
    
    def restart_nginx(self):
        """Reinicia el servicio de Nginx."""
        try:
            subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
            print("Nginx ha sido reiniciado.")
        except subprocess.CalledProcessError as e:
            print(f"Error al reiniciar Nginx: {e}")

    def get_sites(self, directory):
        """Obtiene una lista de sitios desde un directorio específico."""
        return [
            site
            for site in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, site))
        ]

    def handle_site(self,action):
        #clear console
        os.system("clear")
        """Maneja la habilitación o deshabilitación de sitios."""
        directory = (
            "/etc/nginx/sites-enabled"
            if action == "disable"
            else "/etc/nginx/sites-available"
        )
        # sites = get_sites(directory)
        sites = self.get_sites(directory)
        other_directory = (
            "/etc/nginx/sites-enabled"
            if action == "enable"
            else "/etc/nginx/sites-available"
        )
        other_sites = self.get_sites(other_directory)

        if action == "enable":
            sites = [site for site in sites if site not in other_sites]

        if not sites:
            print(f"No hay sitios para {action}.")
            time.sleep(2)
            self.menu.show_menu()

        sites.append("Volver al menú")
        site_name = self.prompt_user_choice(sites, f"Selecciona un sitio para {action}:")

        if site_name == "Volver al menú":
            self.menu.show_menu()
            return

        site_path = f"/etc/nginx/sites-available/{site_name}"
        site_link_path = f"/etc/nginx/sites-enabled/{site_name}"

        if action == "enable":
            if not os.path.exists(site_link_path):
                os.symlink(site_path, site_link_path)
                print(f"Sitio {site_name} habilitado.")
            else:
                print(f"El sitio {site_name} ya está habilitado.")
        else:
            if os.path.exists(site_link_path):
                os.remove(site_link_path)
                print(f"Sitio {site_name} deshabilitado.")
            else:
                print(f"El sitio {site_name} no está habilitado o no existe.")
        self.restart_nginx()

    def enable_site(self):
        """Habilita un sitio de Nginx disponible."""
        self.handle_site("enable")

    def disable_site(self):
        """Deshabilita un sitio de Nginx habilitado."""
        self.handle_site("disable")

    def prompt_user_choice(options, message):
        """Presenta una lista de opciones al usuario y devuelve la elección."""
        questions = [inquirer.List("choice", message=message, choices=options)]
        answers = inquirer.prompt(questions)
        return answers["choice"]

    def list_sites(self):
        #clear console
        os.system("clear")
        sites_enabled = os.listdir("/etc/nginx/sites-enabled")
        print("Sitios habilitados:")
        for site in sites_enabled:
            print(site)
        #show menu
        self.menu.show_menu()

    def create_new_site(self):
        #clear console
        os.system("clear")
        base_path = "/var/www"
        if os.path.exists("/var/www/html"):
            base_path = "/var/www/html"

        site_name = input("Introduce el nombre del sitio (ejemplo.com): ")
        if not re.match(r"^[a-zA-Z0-9.-]+$", site_name):
            print("Nombre del sitio inválido.")
            return

        site_path = os.path.join(base_path, site_name)

        if not os.path.exists(site_path):
            os.makedirs(site_path)
            print(f"Directorio creado en {site_path}")
        else:
            print(f"El directorio ya existe en {site_path}")
            print("Continuando sin crear directorio...")

        php_versions = self.get_installed_php_versions()
        php_version = inquirer.list_input(
            "Elige la versión de PHP:", choices=php_versions
        )
        project_type = inquirer.list_input(
            "Tipo de proyecto:", choices=["PHP en blanco", "Laravel", "CodeIgniter"]
        )

        # Versiones del framework laravel del 8 al 10
        laravel_versions = ["10.0", "9.0", "8.0"]
        laravel_version = None

        if project_type == "Laravel":
            # Consultar si desea instalar un proyecto existente o crear uno nuevo
            laravel_project_type = inquirer.list_input(
                "¿Desea instalar un proyecto existente o crear uno nuevo?:",
                choices=["Instalar proyecto existente", "Crear proyecto nuevo"],
            )

            # Si desea instalar un proyecto existente
            if laravel_project_type == "Instalar proyecto existente":
                # Pedir url del repositorio
                laravel_repo_url = input("Introduce la url del repositorio: ")
                # Clonar repositorio
                subprocess.run(["git", "clone", laravel_repo_url, site_path])
            else:
                laravel_version = inquirer.list_input(
                    "Elige la versión de Laravel:", choices=laravel_versions
                )
                subprocess.run(
                    [
                        "composer",
                        "create-project",
                        f"laravel/laravel:^{laravel_version}",
                        site_path,
                    ]
                )
            vhost_template = "templates/laravel.test"

        elif project_type == "CodeIgniter":
            # Consultar si desea instalar un proyecto existente o crear uno nuevo
            codeigniter_project_type = inquirer.list_input(
                "¿Desea instalar un proyecto existente o crear uno nuevo?:",
                choices=["Instalar proyecto existente", "Crear proyecto nuevo"],
            )

            # Si desea instalar un proyecto existente
            if codeigniter_project_type == "Instalar proyecto existente":
                # Pedir url del repositorio
                codeigniter_repo_url = input("Introduce la url del repositorio: ")
                # Clonar repositorio
                subprocess.run(
                    [
                        "git",
                        "clone",
                        codeigniter_repo_url,
                        "-b",
                        "3.1-stable",
                        site_path,
                    ]
                )
            else:
                subprocess.run(
                    [
                        "git",
                        "clone",
                        "https://github.com/bcit-ci/CodeIgniter.git",
                        "-b",
                        "3.1-stable",
                        site_path,
                    ]
                )
            vhost_template = "templates/codeigniter.test"

        else:
            vhost_template = None  # O una plantilla por defecto para PHP en blanco

        if vhost_template and os.path.exists(vhost_template):
            with open(vhost_template, "r") as vhost_file:
                vhost_content = vhost_file.read()

            vhost_content = vhost_content.replace("{server_name}", site_name)
            vhost_content = vhost_content.replace("{document_root}", site_path)
            vhost_content = vhost_content.replace("{php_version}", php_version)

            vhost_path = f"/etc/nginx/sites-available/{site_name}"
            with open(vhost_path, "w") as vhost_file:
                vhost_file.write(vhost_content)

            symlink_path = f"/etc/nginx/sites-enabled/{site_name}"
            os.symlink(vhost_path, symlink_path)

            subprocess.run(["sudo", "systemctl", "restart", "nginx"])
            print(f"Sitio {site_name} creado y habilitado.")
        else:
            print(
                f"No se encontró la plantilla {vhost_template}. No se puede continuar."
            )
        self.restart_nginx()
        self.show_menu()

    def get_installed_php_versions():
        result = subprocess.run(
            ["apt", "list", "--installed"], capture_output=True, text=True
        )
        installed_packages = result.stdout.split("\n")

        # Expresión regular para identificar paquetes de PHP y sus versiones
        php_version_regex = re.compile(r"php(\d\.\d)")

        php_versions = set()
        for package in installed_packages:
            match = php_version_regex.search(package)
            if match:
                php_versions.add(match.group(1))

        return list(php_versions)

    def enable_site_by_arg(self,site_name):
        """Habilita un sitio de Nginx por nombre."""
        try:
            site_path = f"/etc/nginx/sites-available/{site_name}"
            site_link_path = f"/etc/nginx/sites-enabled/{site_name}"

            if not os.path.exists(site_path):
                print(f"El sitio {site_name} no existe en 'sites-available'.")
                return

            if os.path.exists(site_link_path):
                print(f"El sitio {site_name} ya está habilitado.")
                return

            os.symlink(site_path, site_link_path)
            print(f"Sitio {site_name} habilitado.")
            self.restart_nginx()
        except OSError as e:
            print(f"Error al habilitar el sitio: {e}")

    def disable_site_by_arg(self,site_name):
        """Deshabilita un sitio de Nginx por nombre."""
        # Validaciones
        if not re.match(r"^[a-zA-Z0-9.-]+$", site_name):
            print("Nombre del sitio inválido.")
            return
        try:
            site_link_path = f"/etc/nginx/sites-enabled/{site_name}"

            if not os.path.exists(site_link_path):
                print(f"El sitio {site_name} no está habilitado o no existe.")
                return

            os.remove(site_link_path)
            print(f"Sitio {site_name} deshabilitado.")
            self.restart_nginx()
        except OSError as e:
            print(f"Error al deshabilitar el sitio: {e}")

    def create_site_by_arg(self,site_name, php_version, project_type):
        """Crea un nuevo sitio en Nginx con los parámetros especificados."""
        # Validaciones
        if not re.match(r"^[a-zA-Z0-9.-]+$", site_name):
            print("Nombre del sitio inválido.")
            return
        if not re.match(r"^\d+\.\d+$", php_version):
            print("Versión de PHP inválida.")
            return
        if project_type not in ["PHP en blanco", "Laravel", "CodeIgniter"]:
            print("Tipo de proyecto inválido.")
            return

        base_path = "/var/www"
        if os.path.exists("/var/www/html"):
            base_path = "/var/www/html"

        site_path = os.path.join(base_path, site_name)

        # Crear directorio si no existe
        if not os.path.exists(site_path):
            os.makedirs(site_path)
            print(f"Directorio creado en {site_path}")
        else:
            print(
                f"El directorio ya existe en {site_path}. Continuando sin crear directorio..."
            )

        # Determinar la plantilla de configuración según el tipo de proyecto
        vhost_template = None
        if project_type == "Laravel":
            subprocess.run(["composer", "create-project", "laravel/laravel", site_path])
            vhost_template = "templates/laravel.test"
        elif project_type == "CodeIgniter":
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/bcit-ci/CodeIgniter.git",
                    "-b",
                    "3.1-stable",
                    site_path,
                ]
            )
            vhost_template = "templates/codeigniter.test"
        else:  # Proyecto PHP en blanco
            vhost_template = "templates/php_blank.test"  # Asumiendo que existe una plantilla para PHP en blanco

        # Crear y habilitar el sitio
        if vhost_template and os.path.exists(vhost_template):
            with open(vhost_template, "r") as vhost_file:
                vhost_content = vhost_file.read()

            vhost_content = vhost_content.replace("{server_name}", site_name)
            vhost_content = vhost_content.replace("{document_root}", site_path)
            vhost_content = vhost_content.replace("{php_version}", php_version)

            vhost_path = f"/etc/nginx/sites-available/{site_name}"
            with open(vhost_path, "w") as vhost_file:
                vhost_file.write(vhost_content)

            symlink_path = f"/etc/nginx/sites-enabled/{site_name}"
            os.symlink(vhost_path, symlink_path)

            subprocess.run(["sudo", "systemctl", "restart", "nginx"])
            print(f"Sitio {site_name} creado y habilitado.")
        else:
            print(
                f"No se encontró la plantilla {vhost_template}. No se puede continuar."
            )
        self.restart_nginx()

    def list_sites_by_arg(self):
        # Listar todos los sitios y crear una tabla con el nombre y el estado
        sites_enabled = os.listdir("/etc/nginx/sites-enabled")
        sites_available = os.listdir("/etc/nginx/sites-available")

        sites = []
        for site in sites_available:
            if site in sites_enabled:
                sites.append([site, "Habilitado"])
            else:
                sites.append([site, "Deshabilitado"])

        print("Sitios:")
        print("Nombre\t\tEstado")
        for site in sites:
            print(f"{site[0]}\t\t{site[1]}")

    def show_varsSite(self):
        sites_enabled = self.get_sites("/etc/nginx/sites-enabled")

        if not sites_enabled:
            print("No hay sitios habilitados para modificar.")
            return

        questions = [
            inquirer.List(
                "site",
                message="Selecciona un sitio para modificar",
                choices=sites_enabled,
            ),
        ]
        answers = inquirer.prompt(questions)
        site_name = answers["site"]
        vhost_path = f"/etc/nginx/sites-available/{site_name}"

        # Leer y mostrar la configuración actual
        with open(vhost_path, "r") as file:
            current_config = file.read()
        print("Configuración actual:")
        print(current_config)

        # back to menu
        self.menu.show_menu()

    def set_menu(self, menu):
        self.menu = menu
    
    
    def InstallNginx(self):
        #clear console
        os.system("clear")
        try:
            #Install Nginx 
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "nginx"], check=True)
            print("Nginx instalado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"Error al instalar Nginx: {e}")
        #show menu
        self.menu.show_menu()