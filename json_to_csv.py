import datetime
import json


import pandas as pd

file_name = '/Users/anna/Downloads/builds.json'
new_obj = {
    'parallel': [],
    'start_time': [],
    'stop_time': [],
}

runtime = []

with open(file_name) as fp:
    for i, line in enumerate(fp):
        obj = json.loads(line)
        if not obj['start_time'] or not obj['stop_time']:
            continue
        for k, records in new_obj.items():
            if isinstance(obj[k], int):
                records.append(obj[k])
            elif isinstance(obj[k], dict):
                records.extend(obj[k].values())
        duration = datetime.datetime.fromisoformat(obj['stop_time']['$date'][:-1]) - datetime.datetime.fromisoformat(obj['start_time']['$date'][:-1])
        # print(type(duration))
        runtime.append(duration.total_seconds())

new_obj['duration'] = runtime
df = pd.DataFrame.from_dict(new_obj)

df.to_csv('/Users/anna/Downloads/builds.csv')