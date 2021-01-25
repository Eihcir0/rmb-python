from lcvista.learning.models import (
    RobotMonkeyButler,
)
from lcvista.reports.core.columns import (
    Columns,
    TextColumn,
)


class Name(TextColumn):
    name = 'Name'
    attr = 'name'

    def get_value(self, instance):
        return instance.name


class RobotMonkeyButlerColumns(Columns):
    model = RobotMonkeyButler
    columns = [
        Name,
    ]
