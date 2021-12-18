from utils import generate_valid_seasons

"""
Creates a parser.
"""


def create_parser(parser):
    """
    Creates and returns a Gooey parser.
    """

    parser.add_argument(
        '--database',
        dest='database_type',
        default='sqlite',
        choices=['mysql', 'postgres', 'sqlite'],
        help='The database flag specifies which database protocol to use.  Defaults to "sqlite", but also accepts "postgres" and "mysql".')

    parser.add_argument(
        '--database_name', 
        help="Database Name (Not Needed For SQLite)",
        default='nba')

    parser.add_argument(
        '--database_host', 
        help="Database Hostname (Not Needed For SQLite)",
        default=None)

    parser.add_argument(
        '--username',
        help="Database Username (Not Needed For SQLite)",
        default=None)


    parser.add_argument(
        '--create-schema',
        dest='create_schema',
        action="store_true",
        default=True,
        help='Flag to initialize the database schema before loading data. If the schema already exists then nothing will happen.')

    parser.add_argument(
        '--time-between-requests',
        dest='request_gap',
        default='.7',
        help='This flag exists to prevent rate limiting, and injects the desired amount of time inbetween requesting resources.')

    #To fix issue https://github.com/mpope9/nba-sql/issues/56
    parser.add_argument(
        '--batch_size',
        default='10000',
        type=int,
        help="Inserts BATCH_SIZE chunks of rows to the database. This value is ignored when selecting database 'sqlite'.")

    parser.add_argument(
        '--sqlite-path',
        dest='sqlite_path',
        default='nba_sql.db',
        help='Setting to define sqlite path.')

    parser.add_argument(
        '--quiet',
        dest='quiet',
        action='store_true',
        help='Setting to define stdout logging level. If set, only "ok" will be printed if ran successfully. This currently only applies to refreshing a db, and not loading one.')

    return parser
