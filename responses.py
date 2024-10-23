from typing import Union, Tuple
from usermethods import userobject
import classassignments
import todo
import todolist
import copy

def get_response(user_input: str) -> Union[str, Tuple[str, str]]:
    lowered = user_input.lower()
    
    if "help" in lowered:
        return (
            "**!guide** -> shows you how to get your Canvas API Token\n"
            "**!settoken (token)** -> sets your Canvas API token so we can access your classes and assignments\n"
            "**!todo** -> returns a list of assignments; you can swap pages using !todo (page number)\n"
            "**!check (assignment num)** -> crosses off the chosen assignment to mark that you've completed it\n"
            "**!reminder** -> DM's the user all the assignments that are due within 3 days every 6 hours\n"
            "**!cats** -> erm.. cats?!"
        )
    
    if "guide" in lowered:
        return "Head over to https://csulb.instructure.com/profile/settings and scroll down until you see New Access Token"
    
    if lowered.startswith("settoken"):
        return set_token(user_input[9:])
    
    if open("token_state.txt").read() == "1":
        if lowered.startswith("todo"):
            return handle_todo(user_input)
        if lowered.startswith("check"):
            return handle_check(user_input)
    
    return "Please use a valid command or set a valid canvas api token using !settoken (your token)"

def set_token(token: str) -> str:
    with open("user_token.txt", "w") as file:
        file.write(token)
    
    user = userobject(token)
    if not user.check_token():
        with open("token_state.txt", "w") as file:
            file.write('0')
        return "Invalid Access Token"
    
    save_assignments()
    with open("token_state.txt", "w") as file:
        file.write('1')
    return "success!"

def save_assignments() -> None:
    assignments = list(classassignments.get_assignment_list())
    with open("bleh.txt", "w") as f, open("bleh2.txt", "w") as f2:
        for i, assignment in enumerate(assignments):
            temp_string = f"{i}|{assignment}\n"
            f.write(temp_string)
            f2.write(temp_string)

def handle_todo(user_input: str) -> Tuple[str, str]:
    try:
        page = int(user_input[5:])
    except ValueError:
        page = 1
    assignments =   copy.copy(list(classassignments.get_assignment_list()))
    return todolist.print_todolist(assignments, page)

def handle_check(user_input: str) -> str:
    try:
        assignment_num = int(user_input[6:])
        assignments = list(classassignments.get_assignment_list())
        if assignment_num > len(assignments):
            return "Assignment doesn't exist"
        todo.checktodo(str(assignment_num))
        return f"Successfully checked out assignment {assignment_num}"
    except ValueError:
        return "Invalid assignment number"