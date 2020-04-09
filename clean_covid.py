import pandas as pd
file_name = 'covid_file'

cols = []
rows = {}
with open(file_name,  encoding="utf8", errors='ignore') as fp:
    for i, line in enumerate(fp):
        row = line.split("|")
        if i == 0:
            cols = row
        else:
            rows[i] = row

pd.DataFrame.from_dict(rows, orient='index', columns=cols)
