# Running the Twitter API

### Install Required Packages
`pip install --user lxml`

The following may need to run if lxml isn't installing

>sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev

>sudo apt-get install libxml2-dev libxslt-dev python-dev

`pip install --user pyquery`

`pip install peewee`

`pip install --user pymysql`

### Credentials File
In the same directory as pulltweets.py, a file named **creds.txt** must be created. It contains the DB Username, DB Password and Email Password each on their own line.

### Running
Max tweets may either be not set, or set to zero, setting no limit on the number of tweets collected.

The until date must be at least one day after the since date. To collect all data for July 10, 2017: `since: 2017-07-10` `until: 2017-07-11`
