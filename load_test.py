from locust import HttpLocust, TaskSet, task
import locust
import faker
import json


class UserBehavior(TaskSet):

    faker = faker.Faker()

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.verify = False
        locust.events.quitting += self.on_quit

        self.fake_user()

    def on_quit(self):
        headers = {'Authorization': 'c2375a97-0bd6-4831-9267-b024fb71e2d3', 'content-type': 'application/json'}
        payload = json.dumps({'id': self.person_id})
        response = self.client.delete("/api/3/action/user_delete", headers=headers, data=payload)

    def fake_user(self):
        first_name = self.faker.first_name().lower()
        last_name = self.faker.last_name().lower()
        person_id = '{0}_{1}_test_user'.format(first_name, last_name)
        person_password = '{0}_{1}_test_password'.format(first_name, last_name)
        person_email = '{0}_{1}_test_email@nowhere.null'.format(first_name, last_name)
        headers = {'Authorization': 'c2375a97-0bd6-4831-9267-b024fb71e2d3', 'content-type': 'application/json'}
        payload = json.dumps({'name': person_id, 'email': person_email, 'password': person_password})
        self.maintainer = person_id
        self.author = person_id
        self.person_id = person_id
        self.person_password = person_password
        response = self.client.post("/api/3/action/user_create", headers=headers, data=payload)
        self.api_key = json.loads(response._content)["result"]["apikey"]

    @task(20)
    def login(self):
        self.client.post("/ldap_login_handler", {"login": self.person_id, "password": self.person_password})

    def logout(self):
        self.client.get("/user/_logout")

    @task(30)
    def query_dataset(self):
        self.client.get("/dataset")

    @task(1)
    def new_dataset(self):
        self.name = self.faker.name()
        payload = json.dumps({
            "name": self.name.lower().replace(' ', '_'),
            "title": self.name,
            "maintainer": self.maintainer,
            "author": self.author,
            "verified": True
        })
        print(self.person_id, self.person_password, self.name, self.client.cookies, self.api_key)
        response = self.client.post("/api/3/action/package_create", headers={'Authorization': self.api_key, 'content-type': 'application/json'}, data=payload)
        self.package_id = json.loads(response.content)['result']['id']



        resource_payload = json.dumps({
            "package_id": self.package_id,
            "url": 'http://test/'+self.package_id,
            "name": 'TEST-'+self.package_id
        })

        resource_res = self.client.post("/api/3/action/resource_create", headers={'Authorization': self.api_key, 'content-type': 'application/json'}, data=resource_payload)
        # print(resource_res.__dict__)

    @task(20)
    def dataset_query(self):
        self.client.get('/dataset/' + self.package_id)

    @task(40)
    def index(self):
        self.client.get("/")

    @task(20)
    def dashboard(self):
        self.client.get("/dashboard")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
