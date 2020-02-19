from datetime import datetime, date, timedelta
from todoist.api import TodoistAPI


class DayInfo:
    day = None
    week = None
    month = None
    new_week = False
    new_month = False

    def __str__(self):
        return f"Day - {self.day} Week - {self.week} - New Week - {self.new_week} Month - {self.month}" \
               f" New Month - {self.new_month} "


class DayWeekMonthCalculator:
    def __init__(self, inception_date: date):
        if not isinstance(inception_date, date):
            raise Exception("inception date should be date time")
        self.inception_date = inception_date

    def compute_day_info(self, compute_date: date, week_calculation_offset: int = 0, month_calculation_offset: int = 0) -> DayInfo:
        if not isinstance(compute_date, date):
            raise Exception("compute date should be datetime")

        day_info = DayInfo()
        day_info.day = (compute_date - self.inception_date).days

        week = day_info.day - week_calculation_offset
        if week % 7 == 0:
            day_info.new_week = True
        day_info.week = int(week / 7)

        month = day_info.day - month_calculation_offset
        if month % 28 == 0:
            day_info.new_month = True
        day_info.month = int(month / 28)

        return day_info

PROJECTS_TO_MAP = ["Daily", "Office ToDo"]

day_week_month_calculator = DayWeekMonthCalculator(date(2018, 10, 31))
day_info = day_week_month_calculator.compute_day_info(compute_date = date.today(), week_calculation_offset = 40,
                                                 month_calculation_offset = 5)
# day_info = day_week_month_calculator.compute_day_info(compute_date = date(2020, 2, 24), week_calculation_offset = 40,
#                                                  month_calculation_offset = 5)

api = TodoistAPI("7ef0dcf2d8c6a0cb21bfe5bdc5877f80a7ee8838")
api.sync()

project_ids = []
projects = api.state['projects']
for project in projects:
    if project["name"] in PROJECTS_TO_MAP:
        project_ids.append(project["id"])

if len(project_ids) == 0:
    raise Exception("Could not found project")

for project_id in project_ids:
    if day_info.new_month:
        month_section = api.sections.add(f"Month {day_info.month}", project_id=project_id)

    if day_info.new_week:
        week_section = api.sections.add(f"Week {day_info.week}", project_id=project_id)

    day_section = api.sections.add(f"Day {day_info.day}", project_id=project_id)

api.commit()

if __name__ == "__main__":
    pass
