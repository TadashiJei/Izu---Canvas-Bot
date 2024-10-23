import math
from typing import List, Dict, Tuple
from timeconverter import time_to_word
from classassignments import get_course_name

def print_todolist(assignments: List[str], page: int) -> Tuple[str, str]:
    if (page - 1) * 10 >= len(assignments):
        return "Such page does not exist within your to-do list", 'sowwy :('
    
    temp_str = ''
    with open("bleh2.txt") as file:
        crossed_out = file.read().split("\n")
    
    start_idx = (page - 1) * 10
    end_idx = min(page * 10, len(assignments))
    
    for idx, assignment in enumerate(assignments[start_idx:end_idx], start=start_idx):
        course_id, assignment_info = assignment.split('|', 1)
        course_name = get_course_name(int(course_id)).split(' ', 2)
        time_split = assignment_info.rsplit(' ', 2)
        get_time = f"{time_split[1]} {time_split[2]}"
        ass_name = assignment_info.rsplit(' ', 3)[0][6:]
        
        assignment_str = f"**({idx + 1})** *{time_to_word(get_time)}* - {course_name[0]} {course_name[1]} {ass_name}"
        if "~~" in crossed_out[idx]:
            assignment_str = f"~~{assignment_str}~~"
        
        temp_str += f"{assignment_str}\n"
    
    max_pages = math.ceil(len(assignments) / 10)
    footer = f"Page {page} of {max_pages}"
    
    return temp_str, footer