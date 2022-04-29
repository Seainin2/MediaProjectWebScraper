from ast import parse
from calendar import month
from datetime import date

def parse_date(unformatted_date):
    try:
        months = {
            'January':1,
            'February':2,
            'March':3,
            'April':4,
            'May':5,
            'June':6,
            'July':7,
            'August':8,
            'September':9,
            'October':10,
            'November':11,
            'December':12,
        }

        date_part = unformatted_date.replace(",","").split()

        date_part_year=1990
        date_part_month=1
        date_part_day=1

        throw = True

        for key, value in months.items():
            if date_part[0].casefold() == key.casefold():
                date_part_month = value
                date_part_day = date_part[1]
                date_part_year = date_part[2]
                throw = False
            elif date_part[1].casefold()[0:3] == key.casefold()[0:3]:
                date_part_month = value
                date_part_day = date_part[0]
                date_part_year = date_part[2]
                throw = False
        
        if throw:
            raise Exception
            
        return date(
            day = int(date_part_day),
            month = int(date_part_month),
            year = int(date_part_year)
        )

    except:
        return None
        
    

if __name__ == "__main__":

    print(parse_date("May 3, 2022"))
    print(parse_date("27 Apr, 2022"))
    print(parse_date("April 29, 2022"))
    print(parse_date(""))
