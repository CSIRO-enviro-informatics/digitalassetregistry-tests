import logging
#logging.basicConfig(level=logging.INFO)
from locust import HttpLocust, TaskSet, task, seq_task
import random
import string
import time

def random_string(length):
    output = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(length)])
    return output  


class MyTaskSet(TaskSet):

    def on_start(self):
        response = self.client.post("/ldap_login_handler", {"login":"admin", "password":"admin", "remember": "63072000"})

    @seq_task(1)
    def about(self):
        response = self.client.get("/dashboard?id=admin")
    
    @seq_task(2)
    def new_resource_and_package_create(self):
        self.resource_name = random_string(8).lower()
        response = self.client.get("/dataset/new")
        response = self.client.post("/dataset/new", {"_ckan_phase":"dataset_new_1","pkg_name":"","title": self.resource_name,"name": self.resource_name, "asset_type":"dataset","asset_status":"sm_local-media_storage","notes":"","asset_owner":"","license_id":"notspecified","owner_org":"e70f6776-05f3-48a7-9c24-2fff14e7899a","private":"False","author":"admin","maintainer":"admin","other_affiliates":"","expl_notes":"","verified":"True","tag_string":"","related_projects":"","related_publications":"","save":""})
        response = self.client.get("/dataset/new_resource/" + self.resource_name)
        response = self.client.post("/dataset/new_resource/" + self.resource_name, { "id" : "", "name" : random_string(8).lower() , "description":"", "webtype_url":"", "filetype_url":"", "url":"", "format":"", "restricted":"", "allowed_users":"", "save": "go-metadata" })

class MyLocust(HttpLocust):
    task_set = MyTaskSet

