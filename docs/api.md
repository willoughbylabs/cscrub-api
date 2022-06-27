# Cscrub API

Please note: This project is currently being built.

## Endpoints

### Meetings
GET`/api/meetings` </br>
GET `/api/meetings/{year}`
```
meetings: [
    {
    id
    type
    date
    time
    link
    },
    ...
]
```
POST `/api/meetings`

### Members (Alderpersons)
`/api/members`
```
members: [
    {
    id
    name
    },
    ...
]
```
POST `/api/members`

### Legislation
`/api/legislation`</br>
`/api/legislation?date=3%2F16%2F2022`
```
legislation: [
    {
    id
    record_num
    type
    title
    result
    action_text
    mtg_date
    },
    ...
]
```
POST `/api/legislation`

### Votes
`/api/votes`</br>
`/api/votes?member={member_id}`</br>
`/api/votes?record={record_num}`
```
votes: [
    {
    id
    record_num
    title
    member_name
    vote
    },
    ...
]
```
POST `/api/votes`
