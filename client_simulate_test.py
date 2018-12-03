import logging
#logging.basicConfig(level=logging.INFO)
from locust import HttpLocust, TaskSet, task, seq_task
import faker
import random
import json
import string
import time

def random_string(length):
    output = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])
    return output  


class MyTaskSet(TaskSet):
    def fake_user(self):
        self.faker = faker.Faker()
        first_name = self.faker.first_name().lower()
        last_name = self.faker.last_name().lower()
        person_id = '{0}_{1}_test_user'.format(first_name, last_name)
        person_password = '{0}_{1}_test_password'.format(first_name, last_name)
        person_email = '{0}_{1}_test_email@nowhere.null'.format(first_name, last_name)
        headers = {'Authorization': '1dcc37b6-396e-46cf-b881-7e69e07b8b6b', 'content-type': 'application/json'}
        payload = json.dumps({'name': person_id, 'email': person_email, 'password': person_password})
        self.maintainer = person_id
        self.author = person_id
        self.person_id = person_id
        self.person_email = person_email
        self.person_password = person_password
        response = self.client.post("/api/3/action/user_create", headers=headers, data=payload)
        
    def on_start(self):
        self.fake_user()
        print("login",self.person_id, "password",self.person_password)
        response = self.client.post("/ldap_login_handler", {"login":self.person_id, "password":self.person_password, "remember": "63072000"})
        # print(response.text)
    @seq_task(1)
    def about(self):
        response = self.client.get("/dashboard?id="+self.person_id)

    @seq_task(1)
    def about(self):
        response = self.client.get("/dataset")
        # response = self.client.get("/dataset?groups=rwdmsimport")
        # response = self.client.get("/dataset?groups=badmsimport")
        # response = self.client.get("/dataset?groups=dapimport")
        # response = self.client.get("/dataset?groups=group_unit-b6100")
        # response = self.client.get("/dataset?groups=group_unit-b3800")
        # response = self.client.get("/dataset?groups=group_unit-50012972")
        # response = self.client.get("/dataset?tags=Australia")
        # response = self.client.get("/dataset?asset_type=dataset")
        # response = self.client.get("/dataset?asset_type=software")
        #response = self.client.get("/dataset?q=water&sort=score+desc%2C+metadata_modified+desc")


    @seq_task(3)
    def new_resource_and_package_create(self):
        self.resource_name = random_string(8).lower()
        response = self.client.get("/dataset/new")
        response = self.client.post("/dataset/new", {"_ckan_phase":"dataset_new_1","pkg_name":"","title": self.resource_name,"name": self.resource_name, "asset_type":"dataset","asset_status":"sm_local-media_storage","notes":"","asset_owner":"","license_id":"notspecified","author":"admin","maintainer":"admin","other_affiliates":"","expl_notes":"","verified":"True","tag_string":"","related_projects":"","related_publications":"","save":""})
        if response.status_code == 200:
            response = self.client.post("/dataset/groups/" + self.resource_name, { "group_added" : "6d9337de-8140-4911-9a3f-8c02cdc166fa"})

            response = self.client.get("/dataset/new_resource/" + self.resource_name)
            response = self.client.post("/dataset/new_resource/" + self.resource_name, { "id" : "", "name" :random_string(8).lower() , "description":"", "webtype_url":"", "filetype_url":"", "url":"", "format":"", "restricted":"", "allowed_users":"", "save": "go-metadata" })
        response = self.client.get("/dataset/edit/"+self.resource_name)
        
        response = self.client.post("/dataset/edit/"+self.resource_name, {"_ckan_phase":"dataset_new_1","pkg_name":"","title": self.resource_name,"name": self.resource_name, "asset_type":"dataset","asset_status":"sm_local-media_storage","notes":self.resource_name,"asset_owner":"","license_id":"notspecified","author":"admin","maintainer":"admin","other_affiliates":"","expl_notes":"","verified":"True","tag_string":"","related_projects":"","related_publications":"","save":""})
        response = self.client.get("/dataset/"+self.resource_name)
        if response.status_code == 200:
            text = response.text
            data_id_idx = text.find('data-id')
            resource_id = text[data_id_idx+9 : data_id_idx+45]
            response = self.client.get("/dataset/"+self.resource_name+"/resource/"+resource_id)
            response = self.client.post("/dataset/"+self.resource_name+"/resource_edit/"+resource_id, { "id" : resource_id, "name" :random_string(8).lower() , "description":self.resource_name, "webtype_url":"", "filetype_url":"", "url":"", "format":"", "restricted":"", "allowed_users":"", "save": "go-metadata" })
        # response = self.client.post("/dataset/delete/"+self.resource_name)
class MyLocust(HttpLocust):
    task_set = MyTaskSet

