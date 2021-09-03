# :basketball: nba-sql

[![Github All Releases](https://img.shields.io/github/downloads/mpope9/nba-sql/total.svg)]()

An application to build a Postgres, MySQL, or SQLite NBA database from the public API.

For a Windows executable file: [the latest alpha can be found here](https://github.com/mpope9/nba-sql/releases/tag/v0.0.3).

To access the latest Postgres dump file [check the releases tab](https://github.com/mpope9/nba-sql/releases).

To use a PG dump from the releases, decompress using `xz`, then load with `psql`, like this:
```bash
xz -d nba.sql.xz
psql -U <USERNAME> <DBNAME> < nba.sql
```

This DB is still under construction and liable to schema changes. v0.1.0 will be the final schema before an official migration system is added. Until then, expect to rebuild the whole DB when trying to upgrade.

The default behavior is loading the current season into a SQLite database. There are flags provided use a Postgres or SQLite database, and to specify a specific season. See commandline reference below.

# Getting Started

* [A good place for more information is the wiki](https://github.com/mpope9/nba-sql/wiki).
* [Looking to contribute? Check the list of open issues!](https://github.com/mpope9/nba-sql/issues)

The following environment variables must be set. There are no commandline arguments to specify these. The following example are connection details for the provided docker-compose database:
```
DB_NAME="nba"
DB_HOST="localhost"
DB_USER="nba_sql"
DB_PASSWORD="nba_sql"
```

Here is an example query which can be used after building the database. Lets say we want to find Russell Westbrook's total Triple-Doubles:
```
SELECT SUM(td3) 
FROM player_game_log 
LEFT JOIN player ON player.player_id = player_game_log.player_id 
WHERE player.player_name = 'Russell Westbrook';
```

It will take an estimated 6 hours to build the whole database. However, some tables take much longer than others due to the amount of data: `play_by_play`, `shot_chart_detail`, and `pgtt` in particular. These can be skilled with the `--skip-tables` option. Most basic queries can use the `player_game_log` (which is unskippable).


## Commandline Reference
```
python stats/nba_sql.py -h
usage: nba_sql.py [-h]
                  [--seasons {1996-97,1997-98,1998-99,1999-00,2000-01,2001-02,2002-03,2003-04,2004-05,2005-06,2006-07,2007-08,2008-09,2009-10,2010-11,2011-12,2012-13,2013-14,2014-15,2015-16,2016-17,2017-18,2018-19,2019-20,2020-21}]
                  [--skip-base-tables] [--create-schema] [--database {mysql,postgres,sqlite}]
                  [--time-between-requests REQUEST_GAP]
                  [--skip-tables [{player_season,player_game_log,play_by_play,pgtt,shot_chart_detail} [{player_season,player_game_log,play_by_play,pgtt,shot_chart_detail} ...]]]

nba_sql application. The command loads the database with historic data from the 1996-97 / 2020-21 seasons. EX: python3
stats/nba_sql.py

optional arguments:
  -h, --help            show this help message and exit
  --seasons {1996-97,1997-98,1998-99,1999-00,2000-01,2001-02,2002-03,2003-04,2004-05,2005-06,2006-07,2007-08,2008-09,2009-10,2010-11,2011-12,2012-13,2013-14,2014-15,2015-16,2016-17,2017-18,2018-19,2019-20,2020-21}
                        The seasons flag loads the database with the specified season. The format of the season should be in
                        the form "YYYY-YY". The default behavior is loading the current season. Example usage: --seasons
                        2019-2020 2020-2021
  --skip-base-tables    Flag to skip loading the 'base' tables, which are player and team. Useful if one already has an
                        initialized database and only wants to fill/update a season.
  --create-schema       Flag to initialize the database schema before loading data.
  --database {mysql,postgres,sqlite}
                        The database flag specifies which database protocol to use. Defaults to "mysql", but also accepts
                        "postgres" and "sqlite". Example usage: --database postgres
  --time-between-requests REQUEST_GAP
                        This flag exists to prevent rate limiting, and we inject a sleep inbetween requesting resources.
  --skip-tables [{player_season,player_game_log,play_by_play,pgtt,shot_chart_detail} [{player_season,player_game_log,play_by_play,pgtt,shot_chart_detail} ...]]
                        Use this option to skip loading certain tables. Example: --skip-tables play_by_play pgtt
```

## :crystal_ball: Schema
#### Supported Tables
* player
* team
* game
* play_by_play
* player_game_log
* player_season
* team_game_log
* team_season
* player_general_traditional_total (Also referred to in short as pgtt)
* shot_chart_detail

An up-to-date ER diagram can be found in [`image/NBA-ER.jpg`](https://github.com/mpope9/nba-sql/blob/master/image/NBA-ER.jpg).

## :wrench: Building From Scratch

Requirements:

Python >= 3.8

### :scroll: Provided Scripts

In the `scripts` directory, we provide a way to create the schema and load the data for a Postgres database. We also provide a docker-compose setup for development and to preview the data.

```shell
# Required if you're on Debian based systems
sudo service postgresql stop

docker-compose -f docker/docker-compose-postgres.yml up -d

pip install -r requirements.txt

./scripts/create_postgres.sh
```

If you want to use MySQL, start it with:
```
docker-compose -f docker/docker-compose-mysql.yml up -d

./scripts/create_mysql.sh
```

### :snake: Directly Calling Python

The entrypoint is `stats/nba_sql.py`. To see the available arguments, you can use:
```bash
python stats/nba_sql.py -h
```

To create the schema, use the `--create-schema`. Example:
```bash
pyhton stats/nba_sql.py --create-schema
```

To enable a Postgres database, use the `--database` flag. Example:
```bash
python stats/nba_sql.py --database="postgres"
```

We have added a half second delay between making requests to the NBA stats API. To configure the amount of time use the `--time-between-requests` flag.
```bash
python stats/nba_sql.py --time-between-requests=.5
```

The script `nba_sql.py` adds several tables into the database. Loading these tables takes time, notably, the `play_by_play` table. 
Some of these tables can be skipped by using the `--skip-tables` CLI option. Example:

```bash
python stats/nba_sq.py --create-schema --database postgres --skip-tables play_by_play pgtt
```

### :computer: Local development

#### Setup
Create your virtual environment if you don’t have one already. In this case we use `venv` as the target folder for storing packages.

`python -m venv venv`

Then activate it:
`source venv/bin/activate`

Install dependencies using:
`pip install -r requirements.txt`

##### OSX Errors

If you try to setup on OSX and see an error like
```
Error: pg_config executable not found.
```

This can be resolved by installing `postgresql` through Homebrew:
```bash
brew install postgresql
```

# :pray: Acknowledgements
* [@avadhanij](https://github.com/avadhanij): For guidance and knowledge.
* [nba_api project](https://github.com/swar/nba_api): A great resource to reference for endpoint documentation.
* BurntSushi's [nfldb](https://github.com/BurntSushi/nfldb): The inspiration for this project.
