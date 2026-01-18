Table users {
  id integer [pk, increment]
  username text [unique, not null]
  password text [not null]
}

Table urls {
  id integer [pk, increment]
  user_id integer [not null]
  name text
}

Table keywords {
  id integer [pk, increment]
  url_id integer [not null]
  name text
}

Table statistics {
  id integer [pk, increment]
  user_id integer [not null]
  creation_date timestamp
  last_login timestamp
  entries_created integer
}

Table comments {
  id integer [pk, increment]
  sender_id integer [not null]
  receiver_id integer [not null]
  comment text
}

Ref: urls.user_id > users.id [delete: cascade]
Ref: keywords.url_id > urls.id [delete: cascade]
Ref: statistics.user_id > users.id [delete: cascade]
Ref: comments.sender_id > users.id [delete: cascade]
Ref: comments.receiver_id > users.id [delete: cascade]
