from datetime import datetime,date, timedelta
from todoist.api import TodoistAPI


today = date.today()
# today = date(2020, 2, 17)
day_diff = date(2018, 10, 31)
day = (today - day_diff).days
print(day)

week_diff = int(day) - 285
if week_diff % 7 == 0:
    print("new week")
week = int(week_diff/7)+35
print(week)

month = int(week_diff/28) + 10
if week_diff % 28 == 0:
    print("new month")
print(month)


api = TodoistAPI("7ef0dcf2d8c6a0cb21bfe5bdc5877f80a7ee8838")
api.sync()

project_id = None
projects = api.state['projects']
for project in projects:
    if project["name"] == "Tes":
        project_id = project["id"]

if project_id is None:
    raise Exception()

section = api.sections.add(f"Day {day}", project_id=project_id)
api.commit()

print(project_id)

# print(api.state['projects'])

if __name__ == "__main__":
    pass