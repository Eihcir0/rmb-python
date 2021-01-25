import datetime
from .constants import bcolors

empty_env = {
    'sections': {},
    'replaces': {},
    'inserts': {},
    'paths': {}
}


class Project(object):
    def __init__(self, feature=None, env={}, tasks={}, processes={}, go_list=[]):
        self.feature = feature
        self.start_time = datetime.datetime.now()

        self.tasks = tasks  # dict -- task_id: task
        self.processes = processes  # dict -- process_id: process
        self.go_list = go_list  # list of process or task id's
        self.env = {
            'sections': env.get('sections', {}),
            'replaces': {
                **env.get('replaces', {}),
                'MONKEY_DATE': self.start_time.strftime('%Y-%m-%d %H:%M')},
            'inserts': env.get('sections', {}),
            'paths': {
                'source_base_path': '',
                'target_base_path': '',
                **env.get('paths', {}),
            }
        }

        #  Implement logging verbosity 0,1,2
        self.log_with_colors = True
        self.rmb = "(^_^)"
        self.update_sections_with_processes()
        self.initialize_stats()

    def initialize_stats(self):
        self.stats = {
            'lists_handled': 0,
            'lines_added': 0,
            'files_created': 0,
            'files_updated': 0,
            'completed_tasks': 0,
            'completed_processes': 0,
            'shell_commands_executed': 0,
            'start_time': self.start_time,
            'robots_used': 0,
            'monkeys_used': 0,
            'monkeys_injured': 0,  # for fun
        }

    def update_sections_with_processes(self):
        for process_key in self.processes:
            self.env['sections'][process_key] = self.processes[process_key]['enabled']

    def handle_go_list(self):
        from src.robot import Robot

        # initialize the robot environment with the project env
        self.log(self, 'Programming robot with go_list instructions')
        Robot(**self.env, inherited_env=empty_env, id="go_list", todo_list=self.go_list, project=self, name='go_list').dance()

    def handle_success(self):
        # refactor
        self.log(self, r'')
        self.log(self, r'                        .="=.')
        self.log(self, r'                      _/.-.-.\_     _')
        self.log(self, r'                     ( ( o o ) )    ))')
        self.log(self, r'                      |/  "  \|    //')
        self.log(self, r'      .-------.        \ --- /    //')
        self.log(self, r'     _|~~ ~~  |_       / """ \\  ((')
        self.log(self, r'   =(_|_______|_)=    / /_,_\ \\  \\')
        self.log(self, r'     |:::::::::|      \_\\_|__/ \  ))')
        self.log(self, r'     |:::::::[]|       /`  /`~\  |//')
        self.log(self, r'     |o=======.|      /   /    \  /')
        self.log(self, r'jgs  `"""""""""`  ,--`,-- \/\    /')
        self.log(self, r"                   `-- '--'  '--'")
        self.log(self, r'')
        now = datetime.datetime.now()
        self.log(self, 'Completed project {}!'.format(self.feature))
        self.log(self, 'Completed the following tasks: {}'.format(', '.join(self.go_list)))
        self.log(self, 'Created {} new files'.format(self.stats['files_created']))
        self.log(self, 'Updated {} existing files'.format(self.stats['files_updated']))
        self.log(self, 'Added {} new lines of code'.format(self.stats['lines_added']))
        self.log(self, 'Executed {} shell commands'.format(self.stats['shell_commands_executed']))
        self.log(self, 'Butler handled {} lists employing {} robots and {} monkeys'.format(self.stats['lists_handled'], self.stats['completed_processes'], self.stats['completed_tasks']))
        self.log(self, '{} monkeys were injured due to error'.format(self.stats['monkeys_injured']))  # error
        self.log(self, 'Elapsed time: {} seconds'.format((now - self.stats['start_time']).total_seconds()))

    def go(self):
        self.handle_go_list()
        self.handle_success()

    LOG_COLORS = {
        'FileMonkey': bcolors.OKGREEN,
        'ShellMonkey': bcolors.VIOLET,
        'CreateMigMonkey': bcolors.NOTSURE,
        'Robot': bcolors.OKBLUE,
        'Butler': bcolors.YELLOW,
        'Project': bcolors.CWHITE
    }

    def log(self, who, what, error=False, suppress_who=False):
        # refactor
        who = who.__class__.__name__
        color = ""
        if self.log_with_colors:
            if error:
                color = bcolors.FAIL
            elif "CREATED" in what or "UPDATED" in what:
                suppress_who = True
                color = bcolors.BOLD
            else:
                color = self.LOG_COLORS[who]
            if len(who) > 13:
                who = who[0:13]
            elif len(who) < 13:
                who += (13 - len(who)) * ' '
            message = what
            if not suppress_who:
                message = '{}: {}'.format(who, what)
            try:
                message = color + message + bcolors.ENDC
            except:
                import pdb; pdb.set_trace()
        else:
            message = what  # Can do a better job cleaning up formatting when log_with_colors is False
        print(message)
        if error:
            raise Exception(message)
