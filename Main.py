import Menu
import NginxManager
import sys
import argparse

def main():
    try:
        
        parser = argparse.ArgumentParser(description="Gestor de sitios para Nginx")
        parser.add_argument("--enable", help="Habilitar un sitio")
        parser.add_argument("--disable", help="Deshabilitar un sitio")
        parser.add_argument("--list", action="store_true", help="Listar todos los sitios")
        parser.add_argument("--create", nargs=3, help="Crear un nuevo sitio. Requiere tres argumentos: SITE_NAME, PHP_VERSION, PROJECT_TYPE")
        args = parser.parse_args()
        
        #Create a new nginx manager
        nginx = NginxManager.NginxManager()
        #Create a new menu
        menu = Menu.Menu(nginx)
        #Inject the menu into the nginx manager
        nginx.set_menu(menu)
        
        if args.enable:
            nginx.enable_site_by_arg(args.enable)
        elif args.disable:
            nginx.disable_site_by_arg(args.disable)
        elif args.list:
            nginx.list_sites_by_arg()
        elif args.create:
            nginx.create_site_by_arg(args.create[0], args.create[1], args.create[2])
        else:
            menu.show_menu()
        
    except KeyboardInterrupt:
        print("\nSaliendo...")
        sys.exit(0)
        
if __name__ == "__main__":
    main()