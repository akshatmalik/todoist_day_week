

import todoist
import datetime

# Log user in; switch to OAuth eventually...
api = todoist.TodoistAPI("80e07f53c74dd016969a746ef90eb715582fd095")

api.reset_state()
response = api.sync()

def get_todays_tasks():
    tasks_today = []
    today = datetime.date.today()
    print()
    today = str(today)
    for item in response['items']:
        #     print(item.keys())
        #     print(item["due"])
        due = item.get('due')
        if due:
            print(f"{item['content']} - {due['date'][:10]} - {today == due['date'][:10]} - {item['project_id']}")
            #         print(f"")
            # Slicing :10 gives us the relevant parts
            if today == due['date'][:10]:
                tasks_today.append(item)

    label_list = set()
    for i in tasks_today:
        print(f"{i['content']} - {i['labels']}")
        label_list.update(set([x for x in i['labels']]))

    label_points = {}
    for i in label_list:
        label = api.labels.get_by_id(i)
        print(label['name'])
        if "tick" in label['name']:
            label_points[label["id"]] = int(label['name'].replace("_tick", ""))

    today_points = 0
    for i in tasks_today:
        for k in i["labels"]:
            today_points += label_points.get(k, 0)
    print(today_points)
    recommended = 7
    item = api.items.add(content=f"Ticks planned: {today_points} / {recommended} ",
                         **{"project_id": 1270498890, "priority": 4, "due": {"date": f"{today}T00:00:00Z"}})
    api.commit()

get_todays_tasks()