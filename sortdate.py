from typing import Tuple
import math

def sortdate(assignment: str) -> Tuple[int, int, int, int, int, int]:
    try:
        split_data = assignment.split('|')[2].split(' ')
        if split_data[1] == 'Date':
            return (math.inf,) * 6
        date, time = split_data[0], split_data[1]
        year, month, day = map(int, date.split('-'))
        hour, minute, second = map(int, time.split(':'))
        return year, month, day, hour, minute, second
    except (IndexError, ValueError):
        return (math.inf,) * 6