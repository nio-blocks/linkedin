LinkedIn
========

Create a signal for each new discussion post, given a group ID. Official documentation [here](https://developer.linkedin.com/documents/groups-api#groupposts).

Properties
--------------

-   **queries**: List of group IDs to query.
-   **creds**: API credentials.
-   **polling_interval**: How often API is polled. When using more than one query, each query will be polled at a period equal to the `polling_interval` times the number of `queries`.
-   **retry_interval**: When a url request fails, how long to wait before attempting to try again.
-   **lookback**: On block start, look back this amount of time to grab old posts.
-   **limit**: Number of posts notified on each url request.

Commands
----------------
None

Input
-------
None

Output
---------
Creates a new signal for each LinkedIn Group Discussion Post. Every field in the Post will become a signal attribute. The following is a list of commonly include attributes, but note that not all will be included on every signal:

-   `id`
-   creator[`firstName`]
-   creator[`lastName`]
-   `title`
-   `summary`
-   `siteGroupPostUrl`
