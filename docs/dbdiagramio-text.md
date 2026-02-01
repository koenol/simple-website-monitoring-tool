Table users {
  id integer [pk, increment]
  username text [unique, not null]
  password_hash text [not null]
}

Table urls {
  id integer [pk, increment]
  user_id integer [not null]
  addr text
  public boolean
}

Table keywords {
  id integer [pk, increment]
  url_id integer [not null]
  keyword text
}

Table statistics {
  user_id integer [pk]
  creation_date timestamp
  last_login timestamp
  entries_created integer [default: 0]
}

Ref: urls.user_id > users.id [delete: cascade]
Ref: keywords.url_id > urls.id [delete: cascade]
Ref: statistics.user_id > users.id [delete: cascade]
