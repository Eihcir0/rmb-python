class Robot(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'Robot Process')
        self.id = kwargs.get('id', 'Robot Id')
        self.project = kwargs.get('project')
        self.todo_list = kwargs.get('todo_list')
        self.project.stats['robots_used'] += 1
        self.env = {
            'sections': kwargs.get('sections', {}),
            'replaces': kwargs.get('replaces', {}),
            'inserts': kwargs.get('inserts', {}),
            'paths': kwargs.get('paths', {}),
        }
        self.inherited_env = kwargs.get('inherited_env')
        self.combined_env = {
            'sections': {
                **self.inherited_env['sections'],
                **self.env['sections'],
            },
            'replaces': {
                **self.inherited_env['replaces'],
                **self.env['replaces'],
            },
            'inserts': {
                **self.inherited_env['inserts'],
                **self.env['inserts'],
            },
            'paths': {
                **self.inherited_env['paths'],
                **self.env['paths'],
            },
        }

    def dance(self):
        from src.butler import Butler
        self.project.log(self, 'Environment initialized, beginning process {}'.format(self.id))
        Butler(project=self.project, calling_process=self).handle_list(self.todo_list)
        self.project.log(self, 'Completed process {}'.format(self.id))
        self.project.stats['completed_processes'] += 1
