import os
import subprocess
import argparse
import inquirer
import time
import re

def restart_nginx():
    """ Reinicia el servicio de Nginx. """
    subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
    print("Nginx ha sido reiniciado.")
        
def get_sites(directory):
    """ Obtiene una lista de sitios desde un directorio específico. """
    return [site for site in os.listdir(directory) if os.path.isfile(os.path.join(directory, site))]

def handle_site(action):
    """ Maneja la habilitación o deshabilitación de sitios. """
    directory = "/etc/nginx/sites-enabled" if action == "disable" else "/etc/nginx/sites-available"
    sites = get_sites(directory)
    other_directory = "/etc/nginx/sites-enabled" if action == "enable" else "/etc/nginx/sites-available"
    other_sites = get_sites(other_directory)

    if action == "enable":
        sites = [site for site in sites if site not in other_sites]

    if not sites:
        print(f"No hay sitios para {action}.")
        time.sleep(2)
        show_menu()

    sites.append("Volver al menú")
    site_name = prompt_user_choice(sites, f"Selecciona un sitio para {action}:")

    if site_name == "Volver al menú":
        show_menu()
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
    restart_nginx()
    
def enable_site():
    """ Habilita un sitio de Nginx disponible. """
    handle_site('enable')
    
def disable_site():
    """ Deshabilita un sitio de Nginx habilitado. """
    handle_site('disable')
    
def prompt_user_choice(options, message):
    """ Presenta una lista de opciones al usuario y devuelve la elección. """
    questions = [inquirer.List('choice', message=message, choices=options)]
    answers = inquirer.prompt(questions)
    return answers['choice']
   
def list_sites():
    sites_enabled = os.listdir("/etc/nginx/sites-enabled")
    print("Sitios habilitados:")
    for site in sites_enabled:
        print(site)
    #back to menu
    show_menu()

def modify_site():
    sites_enabled = get_sites("/etc/nginx/sites-enabled")

    if not sites_enabled:
        print("No hay sitios habilitados para modificar.")
        return

    questions = [
        inquirer.List('site',
                      message="Selecciona un sitio para modificar",
                      choices=sites_enabled),
    ]
    answers = inquirer.prompt(questions)
    site_name = answers['site']
    vhost_path = f"/etc/nginx/sites-available/{site_name}"

    # Leer y mostrar la configuración actual
    with open(vhost_path, 'r') as file:
        current_config = file.read()
    print("Configuración actual:")
    print(current_config)

    # Pedir cambios
    new_server_name = input(f"Nuevo server_name (dejar en blanco para mantener {site_name}): ") or site_name
    new_root = input("Nuevo root (dejar en blanco para no cambiar): ")
    new_php_version = input("Nueva versión de PHP (ejemplo: 8.1, dejar en blanco para no cambiar): ")

    # Reemplazar los valores
    current_config = current_config.replace(f"server_name {site_name};", f"server_name {new_server_name};")
    if new_root:
        current_config = re.sub(r'root\s+.+;', f'root {new_root};', current_config)
    if new_php_version:
         current_config = re.sub(r'fastcgi_pass unix:/var/run/php/.+?-fpm.sock;', f'fastcgi_pass unix:/var/run/php/php{new_php_version}-fpm.sock;', current_config)

    # Guardar los cambios
    with open(vhost_path, 'w') as file:
        file.write(current_config)

    # Reiniciar Nginx
    restart_nginx()

    print(f"Configuración de {site_name} actualizada.")

def show_varsSite():
    sites_enabled = get_sites("/etc/nginx/sites-enabled")

    if not sites_enabled:
        print("No hay sitios habilitados para modificar.")
        return

    questions = [
        inquirer.List('site',
                      message="Selecciona un sitio para modificar",
                      choices=sites_enabled),
    ]
    answers = inquirer.prompt(questions)
    site_name = answers['site']
    vhost_path = f"/etc/nginx/sites-available/{site_name}"

    # Leer y mostrar la configuración actual
    with open(vhost_path, 'r') as file:
        current_config = file.read()
    print("Configuración actual:")
    print(current_config)
    
    #back to menu
    show_menu()

def show_menu():
    try:
        questions = [
            inquirer.List('action',
                          message="¿Qué acción te gustaría realizar?",
                          choices=['Habilitar un sitio', 'Deshabilitar un sitio', 'Listar todos los sitios', 'Crear un nuevo sitio','Mostrar opciones del sitio' ,'Editar sitio', 'Salir'],
                          ),
        ]
        answers = inquirer.prompt(questions)

        if answers is None:
            raise KeyboardInterrupt

        if answers['action'] == 'Habilitar un sitio':
            enable_site()
        elif answers['action'] == 'Deshabilitar un sitio':
            disable_site()
        elif answers['action'] == 'Listar todos los sitios':
            list_sites()
        elif answers['action'] == 'Crear un nuevo sitio':
            create_new_site()
        elif answers['action'] == 'Editar sitio':
            modify_site()
        elif answers['action'] == 'Mostrar opciones del sitio':
            show_varsSite()
        elif answers['action'] == 'Salir':
            exit()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario. Saliendo...")
        exit(0)
    
def create_new_site():
    base_path = '/var/www'
    if os.path.exists('/var/www/html'):
        base_path = '/var/www/html'

    site_name = input("Introduce el nombre del sitio (ejemplo.com): ")
    site_path = os.path.join(base_path, site_name)

    if not os.path.exists(site_path):
        os.makedirs(site_path)
        print(f"Directorio creado en {site_path}")
    else:
        print(f"El directorio ya existe en {site_path}")
        print("Continuando sin crear directorio...")

    php_versions = get_installed_php_versions()
    php_version = inquirer.list_input("Elige la versión de PHP:", choices=php_versions)

    project_type = inquirer.list_input("Tipo de proyecto:", choices=["PHP en blanco", "Laravel", "CodeIgniter"])

    if project_type == "Laravel":
        subprocess.run(["composer", "create-project", "laravel/laravel", site_path])
        vhost_template = "templates/laravel.test"
    elif project_type == "CodeIgniter":
        subprocess.run(["git", "clone", "https://github.com/bcit-ci/CodeIgniter.git", "-b", "3.1-stable", site_path])
        vhost_template = "templates/codeigniter.test"
    else:
        vhost_template = None  # O una plantilla por defecto para PHP en blanco

    if vhost_template and os.path.exists(vhost_template):
        with open(vhost_template, 'r') as vhost_file:
            vhost_content = vhost_file.read()

        vhost_content = vhost_content.replace("{server_name}", site_name)
        vhost_content = vhost_content.replace("{document_root}", site_path)
        vhost_content = vhost_content.replace("{php_version}", php_version)

        vhost_path = f"/etc/nginx/sites-available/{site_name}"
        with open(vhost_path, 'w') as vhost_file:
            vhost_file.write(vhost_content)

        symlink_path = f"/etc/nginx/sites-enabled/{site_name}"
        os.symlink(vhost_path, symlink_path)

        subprocess.run(["sudo", "systemctl", "restart", "nginx"])
        print(f"Sitio {site_name} creado y habilitado.")
    else:
        print(f"No se encontró la plantilla {vhost_template}. No se puede continuar.")
    show_menu()
    
def get_installed_php_versions():
    result = subprocess.run(["apt", "list", "--installed"], capture_output=True, text=True)
    installed_packages = result.stdout.split('\n')

    # Expresión regular para identificar paquetes de PHP y sus versiones
    php_version_regex = re.compile(r'php(\d\.\d)')

    php_versions = set()
    for package in installed_packages:
        match = php_version_regex.search(package)
        if match:
            php_versions.add(match.group(1))

    return list(php_versions)
        
def main():
    
    try:    
        parser = argparse.ArgumentParser(description="Gestor de sitios para Nginx")
        parser.add_argument("--enable", help="Habilitar un sitio")
        parser.add_argument("--disable", help="Deshabilitar un sitio")
        parser.add_argument("--list", action="store_true", help="Listar todos los sitios habilitados")

        args = parser.parse_args()

        if args.enable:
            enable_site(args.enable)
        elif args.disable:
            disable_site(args.disable)
        elif args.list:
            list_sites()
        else:
            show_menu()
    except KeyboardInterrupt:
        print("\nSaliendo...")
        exit()
           
if __name__ == "__main__":
    main()
