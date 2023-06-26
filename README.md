# CEU Parasite Web 
Web para la detección automática de parásitos en fotografías de muestras fecales 
y la anotación manual de las mismas.

La aplicación se encuentra disponible en https://parasites.app/.

## Docker
Para ejecutar la aplicación en local, se puede utilizar Docker y Docker compose. 
En esta versión en local la detección de parásitos no está disponible, ya que el 
servidor de IA no es accesible desde IPs arbitrarias y no forma parte de este TFG.
En su lugar, la detección de parásitos se sustituye por una modificación de la imagen 
original (se "tacha" con una X) para simular la modificación de la imagen origen.

Para usar Docker son necesarios dos pasos, existiendo también un tercer paso opcional.

1. En primer lugar se debe crear un fichero `.env` en la raíz del proyecto 
con el siguiente formato:

```bash
SECRET_KEY='doge-wow-such-insecure-much-scary'
# DOCKER compose is prepared to run in debug mode only!! 
DEBUG=True
ALLOWED_HOSTS='*'
# Database
DB_ENGINE='django.db.backends.mysql'
DB_NAME='parasites'
DB_USER='django'
DB_PASSWORD='django'
DB_HOST='db'
DB_PORT='3306'
# Email
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='should-be-configured@gmail.com' # <-----------
EMAIL_HOST_PASSWORD='your-password'  # <-----------
EMAIL_PORT=587
PASSWORD_RESET_TIMEOUT=1800

# Celery
CELERY_BROKER_URL='redis:/celery:6379/0'
CELERY_RESULT_BACKEND='redis:/celery:6379/0'
```

Las líneas marcadas con `<-----------` deben ser configuradas con una cuenta de 
gmail para permitir el envío de correos electrónicos para el registro de usuarios. 
Este paso es opcional y se detalla en la siguiente subsección, si bien sin él 
el registro de usuarios no funcionará. Para poder usar la aplicación es por tanto
necesario registrar un usuario en la base de datos. 

2. Para registrar usuarios, bastaría con incluir el siguiente fichero 
`users.json` en la carpeta `parasite_web/users/fixtures/`. Docker compose se encarga 
de registrar al usuario `user@user.com` con contraseña `parasites`.

```json
[
  {
    "model": "users.user",
    "pk": 1,
    "fields": {
      "first_name": "user",
      "last_name": "user",
      "email": "user@user.com",
      "password": "pbkdf2_sha256$390000$BwqVIbh3PrDfIdK7dRzNku$kH28Wkam08MzCz+PApyXmvuwXihmWLH9edpIuCxNHhs=",
      "is_active": "True"
    }
  }
]
```

3. [Opcional] Si se desea habilitar el registro de usuarios, deben seguirse los 
siguientes pasos para habilitar el envío de correos a los usuarios. En este caso, 
se ha utilizado el servidor SMTP de Gmail por lo que debe usarse una cuenta de gmail:

* Abrir Gmail desde el navegador. Usar la dirección de correo en `EMAIL_HOST_USER`.
* Pulsar en el icono de la cuenta y pulsar el botón "Gestionar tu cuenta de Google".
* En el menú, seleccionar el apartado de “Seguridad”. 
* Activar la verificación en dos pasos en el caso de que no esté activa. 
Es necesario activarla para poder realizar el siguiente paso.  
* En el apartado de "Contraseñas de aplicaciones", seleccionar "Otra (nombre personalizado)"
en el desplegable de "Seleccionar aplicación" y asignarle un nombre (ejemplo: Django Email).  
* Escribir la contraseña que se ha generado para la aplicación en el fichero `.env`, 
variable `EMAIL_HOST_PASSWORD`.

Tras realizar la configuración, es posible ejecutar la aplicación con Docker compose:
```bash 
docker compose up --build
```
Se puede usar la aplicación en `127.0.0.1:8000`.
