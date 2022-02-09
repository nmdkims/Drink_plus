import csv

from .my_settings import MY_DATABASES
import pymysql

DATABASES = MY_DATABASES

conn = pymysql.connect(DATABASES)

try:
    with conn.cursor() as cursor:
        data = []
        sql = 'select '
        cursor.execute(sql)

        rows = cursor.fetchall()
        for row in rows:
            data.append(row)
finally:
    cursor.close()
    conn.close()

headers = []
rows = data

with open('drink.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
