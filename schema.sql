PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_date TEXT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    addr TEXT,
    public BOOLEAN,
    url_status_ok BOOLEAN,
    url_code INT,
    priority_class INT,
    last_update TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (priority_class) REFERENCES priority_classes(id)
);

CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    report_date TEXT,
    url_status_ok BOOLEAN,
    url_code INT,
    FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE priority_classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class TEXT UNIQUE NOT NULL
);

CREATE INDEX idx_urls_user_id_id ON urls(user_id, id);
CREATE INDEX idx_reports_url_id_date ON reports(url_id, report_date DESC);
CREATE INDEX idx_reports_user_id_date ON reports(user_id, report_date DESC);
CREATE INDEX idx_reports_user_id ON reports(user_id);
CREATE INDEX idx_reports_user_id_url_id ON reports(user_id, url_id);
