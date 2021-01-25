from rest_framework.test import APITestCase

from lcvista.organizations.tests.factories import (
    OrganizationFactory,
    OrganizationPersonFactory,
    PersonFactory,
)
from lcvista.robotmonkeybutlers.models import RobotMonkeyButler


class RobotMonkeyButlersEndpointTest(APITestCase):
    def setUp(self):
        self.user = PersonFactory(
            password='1',
        )
        self.organization = OrganizationFactory()

        self.op = OrganizationPersonFactory(
            organization=self.organization,
            person=self.user
        )
        self.client.login(username=self.user.username, password='1')

    def test_create(self):
        name = 'Richie'
        response = self.client.post(
            '/api/v1/robotmonkeybutlers/',
            {
                'name': name,
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        robotmonkeybutler = RobotMonkeyButler.objects.get()
        expected_data = {
            'created_by': self.user,
            'name': name,
        }
        for key in expected_data:
            self.assertEqual(expected_data[key], getattr(robotmonkeybutler, key))

    def test_create__triggers_exception(self):
        name = 'Robots are cool!'
        with self.assertRaises(Exception) as e:
            self.client.post(
                '/api/v1/robotmonkeybutlers/',
                {
                    'name': name,
                },
                format='json',
            )
            self.assertEqual(str(e), 'Yes they are!  But thats not a valid name')

    def test_update(self):
        name = 'Richie'

        response = self.client.post(
            '/api/v1/robotmonkeybutlers/',
            {
                'name': name,
            },
            format='json',
        )
        self.assertEqual(response.status_code, 201)
        response = self.client.patch(
            '/api/v1/robotmonkeybutlers/{}/'.format(response.data['id']),
            {
                'name': 'John',
            },
            format='json',
        )

        robotmonkeybutler = RobotMonkeyButler.objects.get()
        expected_data = {
            'id': str(robotmonkeybutler.id),
            'name': 'John',
        }
        for key in expected_data:
            self.assertEqual(expected_data[key], str(getattr(robotmonkeybutler, key)))
            self.assertEqual(expected_data[key], response.data[key])

    def test_delete(self):
        name = 'Richie'
        response = self.client.post(
            '/api/v1/robotmonkeybutlers/',
            {
                'name': name,
            },
            format='json',
        )
        response = self.client.delete(
            '/api/v1/robotmonkeybutlers/{}/'.format(response.data['id']),
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(RobotMonkeyButler.objects.exists())

    def test_search(self):
        # Todo: Add factories
        goku = RobotMonkeyButler.objects.create(name="Songoku")
        RobotMonkeyButler.objects.create(name="Muten Roshi")
        response = self.client.get(
            '/api/v1/robotmonkeybutlers/',
            {
                'search': 'goku',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], str(goku.id))

    def test_name_is_monkey_filter(self):
        # Todo: Add factories
        RobotMonkeyButler.objects.create(name="Muten Roshi")
        mike = RobotMonkeyButler.objects.create(name="Monkey Mike")
        response = self.client.get(
            '/api/v1/robotmonkeybutlers/',
            {
                'name_is_monkey': 'Mike',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], str(mike.id))
