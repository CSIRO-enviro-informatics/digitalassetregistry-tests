from locust import HttpLocust, TaskSet, task
from requests_toolbelt import MultipartEncoder
import locust
import faker
import json
import urllib3
import time
import random as r
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class UserBehavior(TaskSet):

    faker = faker.Faker()
    min_wait = 0
    max_wait = 0

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.verify = False
        locust.events.quitting += self.on_quit
        self.fake_user()
        headers={"Content-Type":"application/x-www-form-urlencoded",}
        res = self.client.post("/ldap_login_handler", data={"login":self.person_id, "password":self.person_password},  headers=headers)
        print(self.client.cookies)

    def on_quit(self):

        res = self.client.get("/user/_logout")
        print(self.person_id, self.person_password)
        # headers = {'Authorization': self.api_key, 'Content-Type': 'application/json'}
        # payload = json.dumps({'id': self.person_id})
        # response = self.client.delete("/api/3/action/user_delete", headers=headers, data=payload)
        # print(response.status_code)

    def fake_user(self):
        first_name = self.faker.first_name().lower()
        last_name = self.faker.last_name().lower()
        person_id = '{0}_{1}_test_user'.format(first_name, last_name)
        person_password = '{0}_{1}_test_password'.format(first_name, last_name)
        person_email = '{0}_{1}_test_email@nowhere.null'.format(first_name, last_name)
        headers = {'Authorization': '8932e0f4-a44b-4ac6-9db2-9c3f3c77f03c', 'content-type': 'application/json'}
        payload = json.dumps({'name': person_id, 'email': person_email, 'password': person_password})
        self.maintainer = person_id
        self.author = person_id
        self.person_id = person_id
        self.person_password = person_password
        response = self.client.post("/api/3/action/user_create", headers=headers, data=payload)
        self.api_key = json.loads(response._content)["result"]["apikey"]
        

    # @task(3)
    # def query_dataset(self):
    #     self.client.get("/dataset")

    @task(3)
    def new_dataset(self):
        self.name = self.faker.name()
        payload = {
            "_ckan_phase": "dataset_new_1", 
            "asset_owner": self.author,
            "asset_status": 'sm_local-media_storage',
            "asset_type": "dataset",
            "type": "dataset",
            "author": self.author,
            "expl_notes": "",
            "license_id":"notspecified",
            "maintainer": self.maintainer,
            "name": self.name.lower().replace(' ', '_'),
            "notes": "",
            "other_affiliates": "",
            "owner_org": 'e70f6776-05f3-48a7-9c24-2fff14e7899a',
            "pkg_name": self.name.lower().replace(' ', '_'),
            "private": False,
            "related_projects": "",
            "related_publications": "",
            "save":"go-resource",
            "tag_string":"",
            "title": self.name,
            "verified": True,
        }

        print(self.name.lower().replace(' ', '_'))
        headers={'content-type': 'application/x-www-form-urlencoded', "Cookies": self.client.cookies}
        # print(self.person_id, self.person_password, self.name, self.client.cookies, self.api_key)
        print(self.client.cookies)
        res = self.client.request(method='POST', url="/dataset/new", data=json.dumps(payload), headers=headers)
        print(res)
        print(res.is_permanent_redirect)
        print(res.is_redirect)
        print(res.content)
        # response = self.client.post("/api/3/action/package_create", headers={'Authorization': self.api_key, 'content-type': 'application/json'}, data=payload)
        # self.package_id = json.loads(response.content)['result']['id']

        # time.sleep(10)
        # response = self.client.get('/api/3/action/package_show?id='+self.name.lower().replace(' ', '-'))
        # self.package_id = json.loads(response.content)['result']['id']
        # print(json.loads(response.content)['result'])
        # # add resources to a dataset/package

        resource_headers = {"content-type":"application/x-www-form-urlencoded","Cookies": self.client.cookies }
        resource_payload = json.dumps({
            "name": 'TEST-'+self.name.lower().replace(' ', '-')
        })
        resource_res = self.client.post("/dataset/new_resource/"+self.name.lower().replace(' ', '_'),  data=resource_payload, headers=resource_headers)
        print(resource_res.status_code)
        print(resource_res.content)

    # @task(20)
    # def dataset_query(self):
    #     if hasattr(self, 'package_id'):
    #         self.client.get('/dataset/' + self.package_id)

    # @task(3)
    # def index(self):
    #     self.client.get("/")

    # @task(3)
    # def dashboard(self):
    #     self.client.get("/dashboard")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior

