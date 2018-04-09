import os, json
import pandas as pd
import sys
from datetime import datetime, timedelta

def main():
    date = '2018-03-31'
    print (type(date))
    date = str(datetime.strptime(date, "%Y-%m-%d").date()+timedelta(days=1))
    print (date)
if __name__ == "__main__":
	main()