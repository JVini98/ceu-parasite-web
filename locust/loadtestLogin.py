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
