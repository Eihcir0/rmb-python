from src.robot import Robot
from src.monkey import (
    FileMonkey,
    ShellMonkey,
    CreateMigMonkey,
)

TASK = 'task'
PROCESS = 'process'


class Butler(object):
    def __init__(self, **kwargs):
        self.project = kwargs.get('project', None)
        self.calling_process = kwargs.get('calling_process')
        self.current_item_data = None
        self.current_item_type = None

    def validate_prop(self, prop):
        if prop not in self.current_item_data:
            say = "Error -- {} todo_list item {} missing required '{}' field.".format(
                self.calling_process.id,
                self.current_item_data['id'],
                prop)
            self.project.log(self, say, error=True)

    def validate(self):
        required_props = ['id', 'enabled']
        for prop in required_props:
            self.validate_prop(prop)

    def enabled(self):
        enabled = True
        if not self.current_item_data['enabled']:
            say = 'Skipping disabled process {} as part of {} todo_list'.format(
                self.current_item_data['id'],
                self.calling_process.id,
            )
            self.project.log(self, say)
            enabled = False
        return enabled

    def handle_list(self, items_id_list):
        self.items_id_list = items_id_list
        for item_id in items_id_list:
            self.handle(item_id)
        self.project.stats['lists_handled'] += 1
        self.project.log(
            self,
            'Handled {} todo_list'.format(self.calling_process.id,))

    def handle(self, item_id):
        if item_id in self.project.processes:
            self.current_item_type = PROCESS
            self.current_item_data = self.project.processes.get(item_id)
        elif item_id in self.project.tasks:
            self.current_item_type = TASK
            self.current_item_data = self.project.tasks.get(item_id)
        else:
            say = 'Error - Unknown id encountered {} while processing todo_list for {}'.format(
                item_id,
                self.calling_process.id,
            )
            self.project.log(self, say, error=True)
            return
        self.validate()
        if not self.enabled():
            return
        self.delegate()

    def get_monkey(self):
        monkey = None
        task_type = self.current_item_data.get('type')
        #  Use some sort of dict here
        if task_type == 'file':
            monkey = FileMonkey(project=self.project, **self.current_item_data, inherited_env=self.calling_process.combined_env)
        elif task_type == 'shell_command':
            monkey = ShellMonkey(project=self.project, inherited_env=self.calling_process.combined_env, **self.current_item_data)
        elif task_type == 'new_migration':
            monkey = CreateMigMonkey(project=self.project, inherited_env=self.calling_process.combined_env, **self.current_item_data)
        return monkey

    def get_robot(self):
        return Robot(project=self.project, inherited_env=self.calling_process.combined_env, **self.current_item_data)

    def get_delegatee(self):
        delegatee = None
        if self.current_item_type == TASK:
            delegatee = self.get_monkey()
        if self.current_item_type == PROCESS:
            delegatee = self.get_robot()
        return delegatee

    def delegate(self):
        delegatee = self.get_delegatee()
        if delegatee:
            self.log_successful_delegation(delegatee)
            delegatee.dance()
        else:
            self.log_failed_delegation()

    def log_successful_delegation(self, delegatee):
        self.project.log(
            self,
            'Delegating task {} from {} todo_list to {}'.format(
                self.current_item_data['id'],
                self.calling_process.id,
                delegatee.__class__.__name__))

    def log_failed_delegation(self):
        what = 'Unknown item type {} encountered while processing {} todo_list'.format(
            self.current_item_data['id'],
            self.calling_process.id)
        self.project.log(self, what, error=True)

