import json
import os
from typing import Optional
from dotenv import load_dotenv
import discord
from discord import Intents, Client, Message, User, Embed
from discord.ext import tasks
import responses
import datetime
from timeconverter import time_to_word
from classassignments import get_assignment_list, get_courses, Assignment, Course
import asyncio
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TENOR_KEY = os.getenv('TENOR_KEY')

# Set up Discord client
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Store the last known assignments
last_known_assignments: dict[int, set[int]] = {}

@client.event
async def on_ready() -> None:
    logger.info(f"{client.user} is now running")
    create_default_files()
    check_for_new_assignments.start()

def create_default_files() -> None:
    with open("token_state.txt", "w") as file:
        file.write('0')
    with open("user_token.txt", "w") as file:
        file.write('NULL')

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        return
    
    if user_message == '!reminder' and is_token_valid():
        reminder.start(message)
    elif user_message.startswith('!'):
        await process_command(message, user_message[1:])

async def process_command(message: Message, command: str) -> None:
    try:
        response = responses.get_response(command)
        if command.lower().startswith("todo") and is_token_valid():
            await send_todo_list(message, response)
        elif command.lower() == "help":
            await send_help_message(message)
        elif command.lower() == "guide":
            await send_guide_message(message)
        elif command.lower() == "cats":
            await send_cat_gif(message)
        else:
            await message.channel.send(response)
    except Exception as e:
        logger.error(f"Error processing command: {e}")
        await message.channel.send("An error occurred while processing your command.")

async def send_todo_list(message: Message, response: tuple[str, str]) -> None:
    embed = Embed(title="To-Do List", description=response[0], color=discord.Color.purple())
    embed.set_footer(text=response[1])
    await message.channel.send(embed=embed)

async def send_help_message(message: Message) -> None:
    helpembed = Embed(title="List of Commands", description=responses.get_response("help"), color=discord.Color.purple())
    helpembed.set_footer(text="NOTE: !settoken is **REQUIRED** to access other commands apart from !help and !guide... and !cats")
    await message.channel.send(embed=helpembed)

async def send_guide_message(message: Message) -> None:
    guideembed = Embed(title="How To Get Your Access Token", description=responses.get_response("guide"), color=discord.Color.purple())
    image1, image2, image3 = Embed(), Embed(), Embed()
    image1.set_image(url='https://cdn.tadashijei.com/discord/canvas/bot/step-1.png')
    image2.set_image(url='https://cdn.tadashijei.com/discord/canvas/bot/step-2.png')
    image3.set_image(url='https://cdn.tadashijei.com/discord/canvas/bot/step-3.png')
    await message.channel.send(embeds=[guideembed, image1, image2, image3])

async def send_cat_gif(message: Message) -> None:
    try:
        r = await asyncio.to_thread(lambda: requests.get('https://api.thecatapi.com/v1/images/search?format=json&mime_types=gif'))
        cats = json.loads(r.text)
        await message.channel.send(cats[0]['url'])
    except Exception as e:
        logger.error(f"Error fetching cat GIF: {e}")
        await message.channel.send("Sorry, I couldn't fetch a cat GIF at the moment.")

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    await send_message(message, str(message.content))

@tasks.loop(hours=6)
async def reminder(message: Message) -> None:
    next_three_day = datetime.date.today() + datetime.timedelta(days=3)
    output_string = ''
    assignments_list = list(get_assignment_list())
    for assignment in assignments_list:
        due_date = assignment.rsplit(' ', 2)
        if "Date" in due_date[2]:
            continue
        year, month, day = due_date[1].split('|')[1].split('-')
        type_date = datetime.date(int(year), int(month), int(day))
        if type_date <= next_three_day:
            output_string += f"*{time_to_word(str(due_date[1].split('|')[1] + ' ' +  due_date[2]))}* - {due_date[0][6:]} \n"
    embed = Embed(title="DUE WITHIN 3 DAYS", description=output_string, color=discord.Color.purple())
    await message.author.send(embed=embed)

@tasks.loop(minutes=30)
async def check_for_new_assignments() -> None:
    global last_known_assignments
    courses = get_courses()
    
    for course in courses:
        current_assignments = set(assignment.id for assignment in course.get_assignments())
        if course.id not in last_known_assignments:
            last_known_assignments[course.id] = current_assignments
            continue
        
        new_assignments = current_assignments - last_known_assignments[course.id]
        if new_assignments:
            for assignment_id in new_assignments:
                assignment = course.get_assignment(assignment_id)
                await notify_new_assignment(course, assignment)
        
        last_known_assignments[course.id] = current_assignments

async def notify_new_assignment(course: Course, assignment: Assignment) -> None:
    embed = Embed(
        title=f"New Assignment in {course.name}",
        description=f"**{assignment.name}**\nDue: {time_to_word(assignment.due_at)}",
        color=discord.Color.green()
    )
    embed.add_field(name="Description", value=assignment.description[:1000] + "..." if len(assignment.description) > 1000 else assignment.description)
    embed.set_footer(text=f"Assignment ID: {assignment.id}")
    
    for user_id in get_users_with_token():
        user = await client.fetch_user(user_id)
        await user.send(embed=embed)

def get_users_with_token() -> list[int]:
    # Placeholder implementation
    # In a real scenario, you'd fetch this from a database
    return [12345678]  # Replace with actual user IDs

def is_token_valid() -> bool:
    return open("token_state.txt").read() == "1"

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()