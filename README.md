Load tests for CSIRO Land and Water Digital Asset Registry


## How to Run the test

```bash
python3 -m pip install -r requirements.txt
locust -f load_test.py --host=http://hub-dev.research.csiro.au

# Open brower with url: localhost:8089
# Type mock test users and tests per second param at test front page

```

## The on_start()
Class UserBehavior is a test instance, which may be created by class WebsiteUser for multipal times as people input in the test front page.
For each of test instance, the on_start() will be called only one time, and the instance context, such as session cookies, variables, will be maintained by the instance: self . 
The number in the @task(number) indicates the frequence of the test function executed. 

## on_quit()
Locust does not have a tear_down like function yet. In order to clean the data generated during the test, a custom on_quite function was created, and regiested at on_start function as a quitting event. When Locust is quitting, the on_quite function will be executed. 
For this test scenariao, only the test user will be deleted. More work shoud be done on it: 

- [] Keep all genearted dataset (package) as a list.
- [] Keep all generated resources as a list.
- [] Delete all generated dataset and resources.

## Test was implemented in this test scenariao

- [x] Mock browser login
- [x] Mock browser logout
- [x] Mock browser query all dataset
- [x] Mock browser query a dataset by dataset id
- [x] Mock browser explor index page
- [x] Mock browser explor dashboard page
- [x] Use ckan API to create fake users (after create user, the user session/cookies was created and kept by the instance (self) by default)
- [x] use ckan API to create new Dataset and resources attached to a dataset
