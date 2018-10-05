import logging
logging.basicConfig(level=logging.INFO)
from locust import HttpLocust, TaskSet, task

class MyTaskSet(TaskSet):
    def on_start(self):
        response = self.client.post("/ldap_login_handler", {"login":"admin", "password":"admin", "remember": "63072000"})

    @task(1)
    def about(self):
        response = self.client.get("/dashboard?id=admin")
        logging.info(response.content)

class MyLocust(HttpLocust):
    task_set = MyTaskSet
