## Suurella tietomäärällä testaus -raporttti

Applikaation luonteesta johtuen sivutus on lisätty ennen suurella tietomäärällä testausta. Sivutus on myös website-tietorakenteiden kohdalla rajattu viiteen, koska sivustojen pingaus on hidasta. Website-tietorakenteisiin lisättiin vielä loppuvaiheessa last_update timestamp jonka avulla sivun pingausta rajoitettiin 5 minuuttiin. Tähän olisi hyvä jatkokehityksenä lisätä ping-force toiminto jolla se voitaisiin ohittaa, mutta nyt tavoitteena oli vain latausaikojen parantaminen ja siihen last_update toimi erinomaisesti. Raporttien sivutus on rajattu 10, koska nämä eivät vaadi pingausta, tätä voisi vaikka tarvittaessa nostaa.


Seuraavaksi sivun latausaikojen testaus suurella tietomäärällä.

seed.py
```
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
```

main.html (ennen indeksiä ja pingausta):
```
elapsed time: 0.39 s
127.0.0.1 - - [01/Mar/2026 16:22:37] "GET /main?page=3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:37] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:39] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:39] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:39] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:41] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:41] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:41] "GET /favicon.ico HTTP/1.1" 404 -
```

main.html (ennen indeksiä):
```
elapsed time: 0.39 s
127.0.0.1 - - [01/Mar/2026 16:22:37] "GET /main?page=3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:37] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:39] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:39] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:39] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:41] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:41] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:22:41] "GET /favicon.ico HTTP/1.1" 404 -
```

profile.html (ennen pingausta ja indeksiä):
```
elapsed time: 4.25 s
127.0.0.1 - - [01/Mar/2026 16:24:47] "GET /profile/1?page=2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:47] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:49] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:49] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:49] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:51] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:51] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:24:51] "GET /favicon.ico HTTP/1.1" 404 -
```

profile.html (ennen indeksiä):
```
elapsed time: 4.17 s
127.0.0.1 - - [01/Mar/2026 16:26:04] "GET /profile/1?page=2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:04] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:06] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:06] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:06] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:08] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:08] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:26:08] "GET /favicon.ico HTTP/1.1" 404 -
```

CREATE INDEX idx_urls_user_id ON urls(user_id);
CREATE INDEX idx_urls_priority_class ON urls(priority_class);
CREATE INDEX idx_urls_last_update ON urls(last_update);

CREATE INDEX idx_reports_url_id ON reports(url_id);
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_report_date ON reports(report_date);
CREATE INDEX idx_reports_url_date ON reports(url_id, report_date);

main.html (ennen pingausta):
```
elapsed time: 0.44 s
127.0.0.1 - - [01/Mar/2026 16:33:21] "GET /main HTTP/1.1" 200 -
elapsed time: 0.04 s
127.0.0.1 - - [01/Mar/2026 16:33:21] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:23] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:23] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:23] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:25] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:25] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:25] "GET /favicon.ico HTTP/1.1" 404 -
```

main.html (pingauksen jälkeen):
```
elapsed time: 0.34 s
127.0.0.1 - - [01/Mar/2026 16:33:57] "GET /main?page=2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:57] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:59] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:59] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:33:59] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:34:01] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:34:01] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:34:01] "GET /favicon.ico HTTP/1.1" 404 -
```

profile.html (ennen pingausta):
```
elapsed time: 4.45 s
127.0.0.1 - - [01/Mar/2026 16:40:36] "GET /profile/1?page=4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:36] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:38] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:38] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:38] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:40] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:40] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:40:40] "GET /favicon.ico HTTP/1.1" 404 -
```


profile.html (pingauksen jälkeen):
```
elapsed time: 4.37 s
127.0.0.1 - - [01/Mar/2026 16:39:55] "GET /profile/1?page=2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:55] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:57] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:57] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:57] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:59] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:59] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 16:39:59] "GET /favicon.ico HTTP/1.1" 404 -
```

Indeksin lisääminen ei parantanut suurella tietomäärällä sivujen latausaikaa. Tarkempi metodien tarkastelu osoitti että service.get_user_websites_reports_all aiheutti suurimman osan overheadia (3.2s). urls-taulun suodatus aiheutti hidastelua, mutta indeksin avulla r.user_id suodatus voidaan tehdä suoraan.

Päivitetty IDX:
CREATE INDEX idx_urls_user_id_id ON urls(user_id, id);
CREATE INDEX idx_reports_url_id_date ON reports(url_id, report_date DESC);
CREATE INDEX idx_reports_user_id_date ON reports(user_id, report_date DESC);
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_user_id_url_id ON reports(user_id, url_id);

main.html (korjausten jälkeen, ennen pingausta):
```
elapsed time: 0.44 s
127.0.0.1 - - [01/Mar/2026 18:12:43] "GET /main HTTP/1.1" 200 -
elapsed time: 0.04 s
127.0.0.1 - - [01/Mar/2026 18:12:43] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:12:45] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:12:45] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:12:45] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:12:47] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:12:47] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:12:47] "GET /favicon.ico HTTP/1.1" 404 -
```

main.html (pingauksen jälkeen):
```
elapsed time: 0.35 s
127.0.0.1 - - [01/Mar/2026 18:13:24] "GET /main?page=1 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:24] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:26] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:26] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:26] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:28] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:28] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:13:28] "GET /favicon.ico HTTP/1.1" 404 -
```

profile.html (ennen pingausta):
```
elapsed time: 1.31 s
127.0.0.1 - - [01/Mar/2026 18:14:01] "GET /profile/1?page=2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:01] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:03] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:03] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:03] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:05] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:05] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:05] "GET /favicon.ico HTTP/1.1" 404 -
```

profile.html (pingauksen jälkeen):
```
elapsed time: 1.3 s
127.0.0.1 - - [01/Mar/2026 18:14:26] "GET /profile/1?page=1 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:26] "GET /static/styles.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:28] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:28] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:28] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:30] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:30] "GET /favicon.ico HTTP/1.1" 404 -
elapsed time: 0.0 s
127.0.0.1 - - [01/Mar/2026 18:14:30] "GET /favicon.ico HTTP/1.1" 404 -
```

Huomattavimmat erot tulivat sql-kyselyn korjauksen jälkeen. Sivujen latauksessa on vieläkin turhan paljon overheadia. Tämä johtuu siitä että sivutukseen käytettävien sivujen määrän lasku on hidasta. Jatkokehitys-parannus olisi lisätä esimerkiksi statistics-taulu joka sisältäisi esim. arvot public_website_count, private_website_count. Tällöin sivustojen määrää ei tarvitsi laskea joka kerta. 