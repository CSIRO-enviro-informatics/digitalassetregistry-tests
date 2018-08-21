import argparse
import faker
import requests
import logging
import json

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Create random test users in CKAN instance')
parser.add_argument('--target', help='ckan api key for admin user - the corresponding user should have sufficienct privledges to create other users')
parser.add_argument('--admin_key', help='ckan api key for admin user - the corresponding user should have sufficienct privledges to create other users')
parser.add_argument('--user_file', required=False, default='created_users.json', help='output file in which to write json of create user details')
parser.add_argument('--num_users', required=False, default=10, type=int, help='number of users to create')

args = parser.parse_args()

if __name__ == '__main__':

    faker = faker.Faker()
    responses = []
    print(args.num_users)
    for i in range(0, args.num_users):
        first_name = faker.first_name().lower()
        last_name = faker.last_name().lower()
        person_id = '{0}_{1}_test_user'.format(first_name, last_name)
        person_password = '{0}_{1}_test_password'.format(first_name, last_name)
        person_email= '{0}_{1}_test_email@nowhere.null'.format(first_name, last_name)
        headers = {'Authorization': args.admin_key, 'content-type':'application/json' }
        payload = json.dumps({ 'name': person_id, 'email': person_email, 'password': person_password})
        response = requests.post('http://' + args.target + "/api/3/action/user_create", headers=headers, data=payload)
        logging.debug('User id {0} - User password {1}'.format(person_id, person_password))
        logging.info('User create response {0}'.format(response.text))
        response_json =  response.json()['result']
        response_json["password"] = person_password
        responses.append(response_json)
    with open(args.user_file, 'w') as output_file:
        output_file.write(json.dumps(responses, indent=4))

