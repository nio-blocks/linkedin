LinkedIn
========
Create a signal for each new discussion post, given a group ID. Official [documentation](https://developer.linkedin.com/docs).

Properties
----------
- **creds**: Credentials to connect to LinkedIn API.
- **include_query**: Whether to include queries in request to LinkedIn.
- **limit**: Number of posts to come back on each url request to LinkedIn.
- **lookback**: On block start, look back this amount of time to grab old posts.
- **polling_interval**: How often LinkedIn is polled. When using more than one query. Each query will be polled at a period equal to the *polling interval* times the number of queries.
- **queries**: Queries to include on request to LinkedIn.
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Number if times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Creates a new signal for each LinkedIn Group Discussion Post. Every field in the Post will become a signal attribute.

Commands
--------
None

Dependencies
------------
requests_oauthlib

Output Example
--------------
The following is a list of commonly include attributes, but note that not all will be included on every signal:
```
{
  id: string,
  creator: {
    firstName: string,
    lastName: string
  },
  title: string,
  summary: string,
  siteGroupPostUrl: string
}
```

