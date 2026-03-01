Table users {
  id integer [pk, increment]
  creation_date text
  username text [unique, not null]
  password_hash text [not null]
}

Table urls {
  id integer [pk, increment]
  user_id integer [not null]
  addr text
  public boolean
  url_status_ok boolean
  url_code integer
  priority_class integer
  last_update text
}

Table reports {
  id integer [pk, increment]
  url_id integer [not null]
  user_id integer [not null]
  report_date text
  url_status_ok boolean
  url_code integer
}

Table priority_classes {
  id integer [pk, increment]
  class text [unique, not null]
}

Ref: urls.user_id > users.id [delete: cascade]
Ref: urls.priority_class > priority_classes.id
Ref: reports.url_id > urls.id [delete: cascade]
Ref: reports.user_id > users.id [delete: cascade]