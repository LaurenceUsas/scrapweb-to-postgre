# scrapweb-to-postgre
- Python
- Django
- Postgres
- BeautifulSoup4
- nginx
- gunicorn

Primary reason was to collect and analyze data as well as get familiar with the tools used.

check_deptford.py collects the data once a day and submits it to the server.

##### Server then stores:
- RawData - raw data with timestamp as unique key.
- UnitInformation - apartment specific data with apartment name as unique key.
- UnitHistory - unit name with price and status. [when status or price has changed]
