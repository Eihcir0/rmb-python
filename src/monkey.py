import re
import os
import shutil
from src.line import Line
from src.helpers import run_command

empty_env = {
    'sections': {},
    'replaces': {},
    'inserts': {},
}


class Monkey(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Monkey Task')
        self.id = kwargs.get('task_id', 'Monkey Id')
        self.project = kwargs.get('project')
        self.project.stats['monkeys_used'] += 1
        self.inherited_env = kwargs.get('inherited_env', empty_env)
        self.env = {
            'sections': kwargs.get('sections', {}),
            'replaces': kwargs.get('replaces', {}),
            'inserts': kwargs.get('inserts', {}),
            'paths': kwargs.get('paths', {}),
        }
        self.combined_env = {
            'sections': {
                **self.inherited_env['sections'],
                **self.env.get('sections', {}),
            },
            'replaces': {
                **self.inherited_env['replaces'],
                **self.env.get('replaces', {}),
            },
            'inserts': {
                **self.inherited_env['inserts'],
                **self.env.get('inserts', {}),
            },
            'paths': {
                **self.inherited_env['paths'],
                **self.env.get('paths', {}),
            }
        }

    def main(self):
        raise Exception('main() must be implemented by sub-class')

    def dance(self):
        self.main()
        self.handle_success()

    def handle_success(self):
        self.project.stats['completed_tasks'] += 1


class FileMonkey(Monkey):
    def __init__(self, **kwargs):
        super(FileMonkey, self).__init__(**kwargs)
        self.configs = kwargs.get('configs', {})
        self.file_type = kwargs.get('file_type', '')
        self.source_file_full_name_with_extension = kwargs.get('source_file_full_name_with_extension', '')
        self.source_file_path = kwargs.get('source_file_path', '')
        self.target_file_path = kwargs.get('target_file_path', '')
        self.target_file_name = self.get_target_file_name(kwargs)

        target_without_file_extension = self.combined_env['paths']['target_base_path'] + self.target_file_path + self.target_file_name
        replaced = Line(target_without_file_extension, self).process_replaces().value
        self.target = replaced + '.' + self.file_type
        self.temp = replaced + '.tmp'
        if self.source_file_path == '(^_^)update':
            self.source = self.target
            self.updating = True
        else:
            self.source = self.combined_env['paths']['source_base_path'] + self.source_file_path + self.source_file_full_name_with_extension
        if self.target_file_name == '(^_^)update':
            self.target = self.source
        self.updating = self.target == self.source

        self.current_section = None
        self.monkey_processing = False
        self.config_section = False
        self.skip_current = False

    def get_target_file_name(self, kwargs):
        passed_in = kwargs.get('target_file_name', '')

        if "(^_^)latestmigration" in passed_in:
            return self.get_latest_migration_filename()

        return passed_in

    def get_latest_migration_filename(self, operand='max'):
        path_to_target = self.combined_env['paths']['target_base_path'] + self.target_file_path
        target_folder_filenames = os.listdir(path_to_target)
        filtered_filenames = [name for name in target_folder_filenames if name.startswith('0')]
        sorted_target_folder_file_names = sorted(filtered_filenames)
        last = sorted_target_folder_file_names[-1]
        extension_removed = re.sub('.py', '', last)
        replaced = Line(extension_removed, self).process_replaces().value
        return replaced

    def enabled_section(self):
        if not self.current_section:
            return True
        return self.combined_env['sections'].get(self.current_section, False)

    def process_config(self):
        for key, value in self.configs.items():
            self.current_line.replace(key, value)  # Later check for tokens

    def process_monkey(self):
        if self.config_section:
            self.process_config()

    def handle_monkey(self):
        pattern_string = re.escape(self.project.rmb) + "(.*?)" + re.escape(self.project.rmb)
        pattern = re.compile(pattern_string)
        results = pattern.findall(self.current_line.value)
        if len(results) == 0:
            self.project.log(self, 'Single monkey indicator {} found on a line -- ignoring '.format(self.project.rmb))
            return
        if len(results) > 1:
            self.project.log(self, 'Only one monkey indicator command per line. {} {}'.format(self.current_section, self.id), error=True)
        try:
            parts = results[0].split(':')
        except Exception as e:
            print(e)
            import pdb; pdb.set_trace()
        verb = parts[0]
        args = parts[1:]
        method = getattr(self, '_' + verb, None)
        if method is None:
            print('Unknown monkey command')
        else:
            method(verb, args)

    def _config(self, verb, args):  # Yeah these should be on the line, but the logic can live here?
        if args[0].strip() == 'start':
            self.monkey_processing = True
            self.config_section = True
            self.skip_current = True
        elif args[0].strip() == 'end':
            self.monkey_processing = False
            self.config_section = False
            self.skip_current = True

    def _section(self, verb, args):
        if args[0].strip() == 'end':
            self.current_section = None
            self.skip_current = True
        elif args[0].strip() == 'start':
            self.current_section = args[1]
            self.skip_current = True

    def _insert(self, verb, args):
        new = self.combined_env['inserts'].get(args[0].strip(), None)
        if new is None:
            return
        for line in new:  # Expects a list
            Line(line, self).write(update_stats=True)

    def handle_success(self):
        action = 'UPDATED' if self.updating else 'CREATED'
        what = 'FILE {} : {}'
        self.project.log(self, what.format(action, self.target))
        self.project.stats['files_{}'.format(action.lower())] += 1
        return super(FileMonkey, self).handle_success()

    def main(self):
        self.project.log(self, 'Starting task {}'.format(self.name))
        try:
            with open(self.temp, 'w+') as self.outfile:
                with open(self.source, 'r') as self.infile:
                    for line in self.infile:
                        self.current_line = Line(line, self)
                        if self.current_line.has_monkey:
                            self.handle_monkey()
                        elif self.monkey_processing:
                            self.process_monkey()
                        elif not self.enabled_section():
                            self.skip_current = True

                        if self.skip_current:
                            self.skip_current = False
                            continue
                        else:
                            self.current_line.write(update_stats=not self.updating)
                            continue
        except Exception as e:
            print('INSPECT ME!!')
            print(e)
            import pdb; pdb.set_trace()
        try:
            shutil.move(self.temp, self.target)
        except Exception as e:
            print(e)
            import pdb; pdb.set_trace()


class ShellMonkey(Monkey):
    def __init__(self, **kwargs):
        super(ShellMonkey, self).__init__(**kwargs)
        self.command = kwargs.get('command', None)
        self.success_message = kwargs.get('success_message', None)
        self.error = False

    def handle_success(self):
        if self.error:
            self.project.log(self, 'Received this error when runnning shell command: {}'.format(self.command), error=True)
        else:
            replaced = Line(self.success_message, self).process_replaces().value
            self.project.log(self, replaced, suppress_who=True)
        self.project.stats['shell_commands_executed'] += 1
        return super(ShellMonkey, self).handle_success()

    def main(self):
        what = 'Starting task {}'.format(self.name)
        self.project.log(self, what)
        if self.command:
            replaced = Line(self.command, self).process_replaces().value
            output, self.error = run_command(replaced)  # Can I get better output on this?
        # output = output.decode("utf-8")
        # self.project.log(self, output, suppress_who=True)


class CreateMigMonkey(ShellMonkey):
    # Migrate monkey is used to implement post-processing logic when CREATING A NEW MIGRATION FILE
    # For 'python manage.py migrate' just use a ShellMonkey as no processing is currently needed
    def __init__(self, **kwargs):
        super(CreateMigMonkey, self).__init__(**kwargs)

        # Process replaces in pathname
        path_to_migrations = kwargs.get('path_to_migrations', '')
        replaced = Line(path_to_migrations, self).process_replaces().value
        self.path_to_migrations = self.combined_env['paths']['target_base_path'] + replaced

        migration_filename = kwargs.get('migration_filename', None)
        if migration_filename is None:
            self.source = None
        else:
            replaced = Line(migration_filename, self).process_replaces().value
            self.source = self.path_to_migrations + replaced

        self.command = kwargs.get('command', None)
        rename = kwargs.get('rename', None)
        if rename is not None:
            rename = Line(rename, self).process_replaces().value
        self.rename = rename
        self.created_filename = None

    def rename_migration(self):
        target = self.path_to_migrations + self.rename
        shutil.move(self.source, target)
        self.created_filename = self.path_to_migrations + self.rename

    def log_file_created(self, created_filename=None):
        self.project.stats['files_created'] += 1
        what = 'FILE CREATED : {}'.format(created_filename or self.created_filename)
        self.project.log(self, what)

    def handle_success(self):
        if self.source is not None:
            with open(self.source, 'r') as new_migration_file:
                for line in new_migration_file:
                    self.project.stats['lines_added'] += 1
            self.created_filename = self.source
        if self.rename is not None:
            self.rename_migration()
        self.log_file_created('Permissions migration')

        return super(CreateMigMonkey, self).handle_success()
