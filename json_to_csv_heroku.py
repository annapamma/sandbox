import csv
import json
from dateutil import parser

count = 0

with open('builds.tsv', 'w') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
  spamwriter.writerow(['parallel', 'start_time', 'stop_time', 'duration'])
  with open("builds.json") as fp:
    Lines = fp.readlines()
    for line in Lines:
      count += 1
      job = json.loads(line.strip())
      if isinstance(job["parallel"], int):
        parallel = job["parallel"]
      else:
        parallel = job["parallel"]["$numberLong"]
      if not job["start_time"] or not job["stop_time"]:
        continue
      start_time = job["start_time"]["$date"]
      stop_time = job["stop_time"]["$date"]
      # start_datetime = datetime.datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%SZ')
      start_datetime = parser.parse(start_time)
      stop_datimetime = parser.parse(stop_time)
      duration = (stop_datimetime - start_datetime).total_seconds()
      spamwriter.writerow([parallel, start_time, stop_time, duration])
      print(f'finished: {count}')
#

# with open('builds.json', newline='') as csvfile:
#   reader = csv.DictReader(csvfile)
#   for row in reader:
#     print(row)
# # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
# # print(data)
