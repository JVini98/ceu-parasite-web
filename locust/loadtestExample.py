from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def acceso_pagina_inicio(self):
        self.client.get("/") 
