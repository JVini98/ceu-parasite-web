# CEU Parasite Web 
Aplicación web para la detección automática de parásitos en fotografías de muestras fecales y la anotación manual de las mismas.

## Versión desplegada

La aplicación se encuentra disponible en https://parasites.app/.

## Versión local (Docker)
Para ejecutar la aplicación en local, debe tener instaldo `Docker Engine` y `Docker Compose`.  

En el caso de que no tenga instalado `Docker Engine`, siga los pasos indicados para su sistema operativo: https://docs.docker.com/engine/install/  

En el caso de que no tenga instalado `Docker Compose`, siga los pasos indicados para su sistema operativo: https://docs.docker.com/compose/install/  

En esta versión local, la detección de parásitos no está disponible, correspondiente a la sección `Uploads` de la aplicación, ya que el servidor de inteligencia artificial no es accesible desde IPs arbitrarias. Sin embargo, esta no forma parte del alcance de este trabajo fin de grado.
Por tanto, la detección de parásitos se ha sustituido por una modificación de la imagen original (se "tacha" con una X) para simular la modificación de la imagen origen.

Para usar `Docker` es necesario seguir los dos primeros pasos, existiendo un tercer paso opcional.

1. En primer lugar se debe crear un fichero `.env` en la raíz del proyecto con el siguiente formato:

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
CELERY_BROKER_URL='redis://redis:6379/0'
CELERY_RESULT_BACKEND='redis://redis:6379/0'
```

Las líneas marcadas con `<-----------` deben ser configuradas con una cuenta de `Gmail` para permitir el envío de correos electrónicos durante el registro y la sustitución de contraseñas olvidadas de los usuarios. 
Este paso es opcional y se detalla en la subsección 3.
Si no se sigue este paso, el registro y la sustitución de contraseñas olvidadas de los de usuarios no funcionará. Por lo tanto, para poder utilizar la aplicación es necesario registrar un usuario en la base de datos. 

2. Para registrar usuarios, bastaría con incluir el siguiente fichero `users.json` en la carpeta `parasite_web/users/fixtures/`. `Docker compose` se encarga de registrar al usuario `user@user.com` con contraseña `parasites`.

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

3. [Opcional] Si se desea habilitar el registro y la sustitución de las contraseñas olvidadas de los usuarios, deben seguirse los siguientes pasos para habilitar el envío de correos a los usuarios. En este caso, se ha utilizado el `servidor SMTP de Gmail` por lo que debe usarse una cuenta de `Gmail`:

* Abrir `Gmail` desde el navegador. Escribir la dirección de correo en el fichero `.env`, variable `EMAIL_HOST_USER`.
* Pulsar en el icono de la cuenta y pulsar el botón "Gestionar tu cuenta de Google".
* En el menú, seleccionar el apartado de “Seguridad”. 
* Activar la verificación en dos pasos en el caso de que no esté activa. Es necesario activarla para poder realizar el siguiente paso.  
* En el apartado de "Contraseñas de aplicaciones", seleccionar "Otra (nombre personalizado)"
en el desplegable de "Seleccionar aplicación" y asignarle un nombre (ejemplo: Django Email).  
* Escribir la contraseña que se ha generado para la aplicación en el fichero `.env`, 
variable `EMAIL_HOST_PASSWORD`.

Tras realizar la configuración, es posible ejecutar la aplicación con `Docker compose`:
```bash 
sudo docker compose up --build
```
Se puede usar la aplicación en `127.0.0.1:8000`.
