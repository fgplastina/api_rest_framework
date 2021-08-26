import requests,json, random, string

#Funcion principal del script. 
def load_snippets_data():
    #Solicito input
    option = input("Hola! \n Elija una opción o especifique una cantidad en concreto \n A - crea 10 snippets \n B - crea 20 snippets \n C - Crea 50 snippets \n O bien ingrese un numero entero cualquiera. \n Opcion: ").upper()
    #Si puedo convertir a int la opcion lo hago sino dejo continuar el script
    try:
        option = int(option)
    except ValueError:
        pass
    #Si el tipo es distinto de int voy al switch case. Sino voy a crear los snippets directamente
    if type(option) != int:
        create_snippets(switch_options(option))
    else:
        create_snippets(option)

#Para la ejecucion del script en caso de no ser válida la opción.
def resume_on_error():
    print('Opción no válida.')
    raise SystemExit

#Implementacion de switch case en python con funciones
def switch_options(arg):
    if not arg.isupper():
        arg = arg.upper()

    def diez():
        return 10
    def veinte():
        return 20
    def cincuenta():
        return 50
    def default():
        resume_on_error()

    switcher = {
        'A': diez,
        'B': veinte,
        'C': cincuenta,
    }
    return switcher.get(arg,default)()

#Randomizador para generar "comandos"
def random_command():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(0,10))

#Generador de snippets. 
def create_snippets(cantidad):
    #
#    cantidad = int(cantidad)
    for i in range(0,cantidad):
        try:
            data = {
                'code': random_command(),
                'language': 'bash',
            }
            response = requests.post('http://127.0.0.1:8000/snippets/', auth=('admin','admin.12345'), json=data)
            response.raise_for_status()
            print('Carga exitosa. Resultado: ' + str(response.status_code))

        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)


# Llamada al 'main'
load_snippets_data()
