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

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        # self.client.verify = False
        self.fake_user()
        res = self.client.post("/ldap_login_handler", {"login":self.person_id, "password":self.person_password})
        # response = self.client.post("/ldap_login_handler", {"login":"admin", "password":"admin", "remember": "63072000"})
        print(self.client.cookies)

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
        

    # @task(3)
    # def query_dataset(self):
    #     self.client.get("/dataset")
    def new_resource_and_package_create(self):
        self.resource_name = random_string(8).lower()
        response = self.client.get("/dataset/new")
        response = self.client.post("/dataset/new", {"_ckan_phase":"dataset_new_1","pkg_name":"","title": self.resource_name,"name": self.resource_name, "asset_type":"dataset",
        "asset_status":"sm_local-media_storage","notes":"","asset_owner":"","license_id":"notspecified","owner_org":"e70f6776-05f3-48a7-9c24-2fff14e7899a","private":"False",
        "author":"admin","maintainer":"admin","other_affiliates":"","expl_notes":"","verified":"True","tag_string":"","related_projects":"","related_publications":"","save":""})
        response = self.client.get("/dataset/new_resource/" + self.resource_name)
        response = self.client.post("/dataset/new_resource/" + self.resource_name, { "id" : "", "name" : random_string(8).lower() , "description":"", "webtype_url":"", "filetype_url":"", "url":"", "format":"", "restricted":"", "allowed_users":"", "save": "go-metadata" })
        
    @task(3)
    def new_dataset(self):
        response = self.client.get("/dataset/new")
        self.name = self.faker.name().lower().replace(' ', '_')
        res = self.client.post("/dataset/new",  {"_ckan_phase":"dataset_new_1","pkg_name":"","title": self.name,"name": self.name, "asset_type":"dataset", "asset_status":"sm_local-media_storage","notes":"","asset_owner":"","license_id":"notspecified","owner_org":"e70f6776-05f3-48a7-9c24-2fff14e7899a","private":"False","author":"admin","maintainer":"admin","other_affiliates":"","expl_notes":"","verified":"True","tag_string":"","related_projects":"","related_publications":"","save":""})
        response = self.client.get("/dataset/new_resource/" + self.name)
        # response = self.client.post("/dataset/new_resource/" + self.resource_name, { "id" : "", "name" : random_string(8).lower() , "description":"", "webtype_url":"", "filetype_url":"", "url":"", "format":"", "restricted":"", "allowed_users":"", "save": "go-metadata" })
        response = self.client.get("/dataset/new_resource/" + self.name)
        resource_res = self.client.post("/dataset/new_resource/"+self.name, {
            "name": self.name,
            # "id": "",
            "description":"", 
            "webtype_url":"", 
            "filetype_url":"", 
            "url":"", "format":"", 
            "restricted":"", 
            "allowed_users":"", 
            "save": "go-metadata"
        })
        response = self.client.post("/dataset/delete/" + self.name)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior

