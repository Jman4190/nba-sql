#!/bin/bash
pyinstaller --windowed -n nba_sql --paths=stats stats/gui.py -F
