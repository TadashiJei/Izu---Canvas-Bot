from canvasapi import Canvas
from timeconverter import timeconverter
from sortdate import sortdate
from typing import List, Tuple

def set_user() -> Tuple[Canvas, Canvas]:
    API_URL = "https://csulb.instructure.com/"
    with open("user_token.txt") as file:
        API_KEY = file.read().strip()
    
    canvas = Canvas(API_URL, API_KEY)
    user = canvas.get_current_user()
    return user, canvas

def get_courses() -> List[Canvas.course.Course]:
    user, _ = set_user()
    courses = user.get_courses(enrollment_status='active')
    return [course for course in courses if hasattr(course, 'name') and course.enrollment_term_id == 117]

def get_assignment_list() -> List[str]:
    course_list = get_courses()
    assignment_list = []
    for course in course_list:
        for assignment in course.get_assignments(bucket="future"):
            assignment_list.append(f"{course.id}|{assignment}|{timeconverter(assignment.due_at)}")
    return sorted(assignment_list, key=sortdate)

def get_course_name(id: int) -> str:
    _, canvas = set_user()
    return canvas.get_course(id).name