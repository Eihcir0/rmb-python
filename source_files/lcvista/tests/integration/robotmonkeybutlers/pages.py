from lcvista.tests.integration.utils import (
    BaseForm,
    BasePage,
    BasePageElement,
)


class Row(BasePageElement):
    @property
    def cells(self):
        return self.element.find_elements_by_css_selector('td,th')

    def __getitem__(self, index):
        return self.cells[index]

    @property
    def edit_button(self):
        return self.element.find_element_by_link_text('Edit')

    @property
    def delete_button(self):
        return self.element.find_element_by_link_text('Edit')


class RobotMonkeyButlerEditForm(BaseForm):
    def get_form_element(self, name):
        return super(RobotMonkeyButlerEditForm, self).get_form_element(name)


class RobotMonkeyButlersListFiltersForm(BaseForm):
    def get_form_element(self, name):
        return super(RobotMonkeyButlersListFiltersForm, self).get_form_element(name)


class DeleteRequestConfimationModal(BasePageElement):
    @property
    def delete_request_confirmation_button(self):
        return self.element.find_element_by_css_selector('button.btn-danger')


class RobotMonkeyButlerEditPage(BasePage):
    form_class = RobotMonkeyButlerEditForm


class RobotMonkeyButlersListPage(BasePage):
    form_class = RobotMonkeyButlersListFiltersForm

    def get_url(self, organization):
        parts = [
            organization.slug,
            'robotmonkeybutlers',
        ]
        return '/'.join(parts)

    @property
    def rows(self):
        return [
            Row(row)
            for row in self.driver.find_elements_by_css_selector('.table-default tbody tr')
        ]
