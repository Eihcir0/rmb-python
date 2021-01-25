from itertools import zip_longest

from django.test import TestCase

from lcvista.learning.models import (
    RobotMonkeyButler,
)
from lcvista.organizations.tests.factories import (
    OrganizationFactory,
    OrganizationPersonFactory,
    PersonFactory,
)
from lcvista.reports.reports.robot_monkey_butler import RobotMonkeyButlerReport


class RobotMonkeyButlerReportTest(TestCase):
    def setUp(self):
        self.organization = OrganizationFactory()
        self.user = PersonFactory(
            password='1',
            is_superuser=True,
        )
        self.organization_person = OrganizationPersonFactory(
            person=self.user,
            organization=self.organization
        )

        self.model = RobotMonkeyButler

        self.client.login(username=self.user.username, password='1')

    def test_get_available_columns(self):
        expected = [
            'robotmonkeybutler__name',
        ]
        organization = OrganizationFactory()
        report = RobotMonkeyButlerReport(organization=organization)
        self.assertEqual(list(report.get_available_columns().keys()), expected)

    def test_get_spec(self):
        expected = [
            {
                'name': 'Name',
                'key': 'robotmonkeybutler__name',
                'data_type': 'text',
            },
        ]
        report = RobotMonkeyButlerReport(organization=self.organization)
        self.assertEqual(list(report.get_spec()['available_columns']), expected)

    def test_report_data(self):
        expected_column_data = [
            {
                'name': 'Name',
                'key': 'robotmonkeybutler__name',
                'data_type': 'text',
            },
        ]

        expected_row_data = [
            ['my name'],
        ]

        RobotMonkeyButlerFactory(
            name='my name'
        )

        all_columns = RobotMonkeyButlerReport(organization=self.organization).get_available_columns()
        report = RobotMonkeyButlerReport(
            organization=self.organization,
            selected_columns=all_columns,
            report_access_as=self.organization_person,
        )
        self.assertEqual(report.get_column_data(), expected_column_data)
        for (result, expected_row) in zip_longest(report.get_row_data(report.get_queryset()), expected_row_data):
            self.assertEqual(result, expected_row)
