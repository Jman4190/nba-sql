description = """
    nba_sql application.
    
    The command loads the database with historic data from the 1996-97 / 2019-20 seasons.
    EX:
        python3 stats/nba_sql.py
    """

from settings import Settings
from constants import season_list, team_ids
import argparse
import time

from team import TeamRequester
from player import PlayerRequester
from player_season import PlayerSeasonRequester
from player_game_log import PlayerGameLogRequester
from player_general_traditional_total import PlayerGeneralTraditionalTotalRequester

def main():
    """
    Main driver for the nba_sql application.
    """

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--season', dest='season', default='all', 
        help="""
            The season flag loads the database with the specified season. 
            The format of the season should be in the form "YYYY-YY".
            """)

    parser.add_argument('--base_tables', dest='do_base_tables', default=True,
        help="""
            Flag to designate filling the 'base' tables, which are player and team.
            Useful if one already has an initialized database and only wants to fill/update
            a season.
            """)

    parser.add_argument('--create_schema', dest='create_schema', default=False, 
        help="""
            The create_schema flag is used to initialize the database schema before loading data.
            """)

    parser.add_argument('--database', dest='database', default='mysql', 
        help="""
            The dtatbase flag specifies which database protocol to use. 
            Defaults to "mysql", but also accepts "postgres".
            """)

    parser.add_argument('--time_between_requests', dest='request_gap', default='.5',
        help="""
            This flag exists to prevent rate limiting, and we inject a sleep inbetween requesting
            resources.
            """)

    args = parser.parse_args()

    ## CMD line args.
    database = args.database
    create_schema = args.create_schema
    request_gap = float(args.request_gap)
    do_base_tables = args.do_base_tables

    settings = Settings(database)


    player_requester = PlayerRequester(settings)
    team_requester = TeamRequester(settings)

    player_season_requester = PlayerSeasonRequester(settings)
    player_game_log_requester = PlayerGameLogRequester(settings)
    pgtt_requester = PlayerGeneralTraditionalTotalRequester(settings)

    if create_schema:
        do_create_schema(
            settings, 
            player_requester, 
            player_season_requester, 
            player_game_log_requester,
            pgtt_requester,
            team_requester
        )

    populate_base_tables(do_base_tables, team_requester, player_requester, request_gap)

    season_bar = progress_bar(
        season_list, 
        prefix='Loading Main Data',
        suffix='This one will take a while...',
        length=len(season_list))

    # Load seasonal data.
    print('Populating seasonal data.')
    for season_id in season_bar:

        player_season_requester.populate_season(season_id)
        time.sleep(request_gap)

        player_game_log_requester.populate_season(season_id)
        time.sleep(request_gap)

        pgtt_requester.populate_season(season_id)
        time.sleep(request_gap)

def do_create_schema(settings, player_requester, player_season_requester, 
    player_game_log_requester, pgtt_requester, team_requester):
    """
    Function to initialize database schema.
    """
    print("Initializing schema.")

    # Base Tables
    player_requester.create_ddl()
    team_requester.create_ddl()

    player_season_requester.create_ddl()
    player_game_log_requester.create_ddl()
    pgtt_requester.create_ddl()

def populate_base_tables(do_base_tables, team_requester, player_requester, request_gap):
    """
    Populates base tables.
    """

    if not do_base_tables:
        return

    team_bar = progress_bar(
        team_ids, 
        prefix='team Table Loading', 
        suffix='', 
        length=len(team_ids))

    player_bar = progress_bar(
        season_list, 
        prefix='player Table Loading',
        suffix='',
        length=len(season_list))

    # Load team data.
    print('Populating team data')
    for team_id in team_bar:
        team_requester.add_team(team_id)
        time.sleep(request_gap)
    team_requester.populate()

    # Load player data.
    print('Populating player data')
    for season_id in player_bar:
        player_requester.add_player(season_id)
        time.sleep(request_gap)
    player_requester.populate()

def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    Call in a loop to create terminal progress bar
    @params:
    iteration   - Required  : current iteration (Int)
    total       - Required  : total iterations (Int)
    prefix      - Optional  : prefix string (Str)
    suffix      - Optional  : suffix string (Str)
    decimals    - Optional  : positive number of decimals in percent complete (Int)
    length      - Optional  : character length of bar (Int)
    fill        - Optional  : bar fill character (Str)
    printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()

if __name__ == "__main__":
    main()
