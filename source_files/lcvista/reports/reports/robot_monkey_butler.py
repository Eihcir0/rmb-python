from lcvista.learning.models import (
    RobotMonkeyButler,
)
from lcvista.reports.columns.robot_monkey_butler import RobotMonkeyButlerColumns
from lcvista.reports.core.reports import BaseReport
from lcvista.reports.filters.robot_monkey_butler import RobotMonkeyButlerFilters


class RobotMonkeyButlerReport(BaseReport):
    name = 'Robot Monkey Butlers'
    model = RobotMonkeyButler
    columns = [
        RobotMonkeyButlerColumns,
    ]
    filters = [
        RobotMonkeyButlerFilters,
    ]

    def get_path_to_model(self, model):
        if model == RobotMonkeyButler:
            return ''

        raise NotImplementedError('{} is not supported for this report'.format(model._meta.model_name))
