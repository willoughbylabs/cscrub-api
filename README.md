# Cscrub API
## Chicago City Council Votes at Your Fingertips

Please note: This project is currently being built.</br>

## Summary
The bot extracts council members, legistlation, meetings, and votes from the Chicago City Clerk's website. This data is then used to power this API. For bot documentation, please visit [/docs/bot.md](./docs/bot.md). For API documentation, please visit [/docs/api.md](./docs/api.md).

## What For
To convert this:
![City Clerk website](/img/chi_clerk.png)
Into this:
![PostgreSQL database with City Clerk data](/img/psql.png)

City Council vote data is publicly available on the [City Clerk's website](https://chicago.legistar.com/Calendar.aspx), but formulating an overview of a council member's voting record is difficult. Additionally, this information is not yet available on the [Open Data Portal](https://data.cityofchicago.org/).

## Caveats
- Only fetches the last 100 City Council meetings (through 9/14/2016).
- Only fetches first 200 legislation for each meeting.

## Resources
A shoutout to these folks for the assists!</br>
[resources.md](/docs/resources.md)
[/docs/resources.md](/docs/resources.md)
