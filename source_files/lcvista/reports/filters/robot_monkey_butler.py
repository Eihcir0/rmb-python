from lcvista.learning.models import (
    RobotMonkeyButler,
)
from lcvista.reports.core.filters import (
    Filters,
    TextFilter,
)


class NameFilter(TextFilter):
    name = 'Name'
    attr = 'name'


class RobotMonkeyButlerFilters(Filters):
    model = RobotMonkeyButler
    filters = [
        NameFilter,
    ]
