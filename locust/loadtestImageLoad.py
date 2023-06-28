from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def acceso_pagina_inicio(self):
        self.client.get("/")

    @task
    def acceso_pagina_usuario(self):
        self.client.get("/users")

    @task
    def inicio_sesion(self):
        self.client.post(
           "/users", {"username": "our-user", "password": "our-pass"})

    @task
    def acceso_pagina_subida_parasito(self):
        self.client.get("/uploads")

    @task
    def enviar_imagen(self):
        headers = {"Content-Type": "multipart/form-data"}

        with open("example_images/00000010.jpg", "rb") as file:
            files = {"image": file}
            response = self.client.post(
                "/uploads", files=files, headers=headers)

        if response.status_code == 200:
            print("Imagen enviada exitosamente")
        else:
            print("Error al enviar la imagen")
