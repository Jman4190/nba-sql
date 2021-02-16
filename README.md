# :basketball: nba-sql

An application to build a Postgres or MySQL NBA database from the public API.

The default behavior is collecting seasons 1996-86 to 2019-20 and inserting them into a MySQL databse. There are flags provided to change to a Postgres database, and to specify a specific season.

The following environment variables must be set. There are no commandline arguments to specify these. The following example are connection details for the provided docker-compose database:
```
DB_NAME="nba"
DB_HOST="localhost"
DB_USER="nba_sql"
DB_PASSWORD="nba_sql"
```

## Usage

Requirements:

Python >= 3.6

### :scroll: Provided Scripts

In the `scripts` directory, we provide a way to create and load the schema for a Postgres database. We also provide a docker-compose setup for development and to preview the data.

```bash
# Required if you're on Debian based systems
sudo service postgresql stop
docker-compose up -d

pip install -r requirements.txt

./scripts/create_postgres.sh
```

### :snake: Directly Calling Python

The entrypoint is `stats/nba_sql.py`. To see the available arguments, you can use:
```bash
python stats/nba_sql.py -h
```

To create the schema, use the `--create_schema`. Example:
```bash
pyhton stats/nba_sql.py --create_schema=True
```

To enable a Postgres database, use the `--database` flag. Example:
```bash
python stats/nba_sql.py --database="postgres"
```

### Local development

##### The manual way
Create your virtual environment if you don’t have one already. In this case we use `venv` as the target folder for storing packages.

`python -m venv venv`

Then activate it:
`source venv/bin/activate`

Install dependencies using:
`pip install -r requirements.txt`
