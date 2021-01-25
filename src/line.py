import re


class Line(object):
    def __init__(self, value, monkey):
        self.value = value
        self.monkey = monkey
        self.skip_line = False
        if self.value is None:
            import pdb; pdb.set_trace()

    @property
    def has_monkey(self):
        return self.monkey.project.rmb in self.value

    def update_line(self, value):
        if value is None:
            return self
        self.value = value
        return self

    def replace(self, from_value, to_value):
        # Default behavior, if you pass in a list with replaces, then it will replace that entire
        # line (not just the matched part) and add any additional lines
        if type(to_value) == list:
            self.monkey.skip_current = True
            for item in to_value:
                self.monkey.outfile.write(Line(item, self.monkey).process_replaces().value)
                self.monkey.project.stats['lines_added'] += 1
            self.skip_line = True
        else:
            new_line = (re.sub(from_value, to_value, self.value))
            return new_line

    def process_replaces(self):
        for a, b in self.monkey.combined_env['replaces'].items():
            if a in self.value:
                self.update_line(self.replace(a, b))
        return self

    def write(self, update_stats=True, replace=True):
        #  If editing, even though we write the line we aren't actually adding
        if replace:
            self.process_replaces()
        if not self.skip_line:
            self.monkey.outfile.write(self.value)
            if update_stats:
                self.monkey.project.stats['lines_added'] += 1
