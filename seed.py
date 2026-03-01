import sqlite3

db = sqlite3.connect("database.db")

website_count = 10**6
report_count = 10**7

for i in range(1, website_count + 1):
    db.execute("""INSERT INTO urls (user_id, addr, public, url_status_ok, url_code, priority_class, last_update)
                  VALUES (1, ?, 1, 1, 200, 1, datetime('now'))""",
               ["https://testi" + str(i) + ".fi"])

for i in range(1, report_count + 1):
    url_id = (i % website_count) + 1
    db.execute("""INSERT INTO reports (url_id, user_id, report_date, url_status_ok, url_code)
                  VALUES (?, 1, datetime('now'), 1, 200)""",
               [url_id])

db.commit()
db.close()
