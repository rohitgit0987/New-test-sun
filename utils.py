import random  # NIKHIL SAINI BOTS
import time  # NIKHIL SAINI BOTS
import math  # NIKHIL SAINI BOTS
import os  # NIKHIL SAINI BOTS
from vars import CREDIT  # NIKHIL SAINI BOTS
from pyrogram.errors import FloodWait  # NIKHIL SAINI BOTS
from datetime import datetime, timedelta  # NIKHIL SAINI BOTS


# Timer class
class Timer:  # NIKHIL SAINI BOTS
    def __init__(self, time_between=5):  # NIKHIL SAINI BOTS
        self.start_time = time.time()  # NIKHIL SAINI BOTS
        self.time_between = time_between  # NIKHIL SAINI BOTS

    def can_send(self):  # NIKHIL SAINI BOTS
        if time.time() > (self.start_time + self.time_between):  # NIKHIL SAINI BOTS
            self.start_time = time.time()  # NIKHIL SAINI BOTS
            return True  # NIKHIL SAINI BOTS
        return False  # NIKHIL SAINI BOTS


# Human readable byte size
def hrb(value, digits=2, delim="", postfix=""):  # NIKHIL SAINI BOTS
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KB", "MB", "GB", "TB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix


# Human readable time
def hrt(seconds, precision=0):  # NIKHIL SAINI BOTS
    pieces = []
    value = timedelta(seconds=seconds)

    if value.days:
        pieces.append(f"{value.days}day")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}hr")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}min")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}sec")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


# Avengers-style snake bar
def get_avenger_snake_bar(progress: int, total: int = 10):
    snake_head = "🐍"
    trail = "🟩"
    mid_trail = "🟨"
    empty = "⬜"

    bar = ""
    for i in range(total):
        if i == progress:
            bar += snake_head
        elif i < progress:
            bar += trail
        elif i < progress + 2:
            bar += mid_trail
        else:
            bar += empty
    return bar


# Avengers-style display message
def get_endgame_progress_display(progress_percent: int, speed: str, processed: str, total: str, eta: str):
    progress_units = progress_percent // 10
    snake_bar = get_avenger_snake_bar(progress_units)

    quotes = [
        '"Whatever it takes." – Captain America',
        '"I am... Iron Man." – Tony Stark',
        '"This is the fight of our lives." – Cap',
        '"Part of the journey is the end." – Tony',
        '"I went for the head." – Thor',
    ]

    quote = random.choice(quotes)

    return f"""
💥 Avenge the Fallen... Endgame Protocol Activated

🌀 Quantum Tunnel Progress  
{snake_bar}

🧤 Gauntlet Charge ➤ | {progress_percent}% |
🚀 Upload Speed ➤ | {speed} |
⚡ Power Source ➤ | {processed} / {total} |
⏳ Time Remaining ➤ | {eta} |

💬 {quote}
🔗 Powered by: {CREDIT}
"""


# Create timer
timer = Timer()  # NIKHIL SAINI BOTS


# Final async progress function using the Avengers UI
async def progress_bar(current, total, reply, start):  # NIKHIL SAINI BOTS
    if timer.can_send():  # NIKHIL SAINI BOTS
        now = time.time()
        diff = now - start
        if diff < 1:
            return

        perc = current * 100 / total
        perc_str = f"{perc:.1f}%"
        elapsed_time = round(diff)
        speed = current / elapsed_time
        remaining_bytes = total - current

        if speed > 0:
            eta_seconds = remaining_bytes / speed
            eta = hrt(eta_seconds, precision=1)
        else:
            eta = "-"

        sp = str(hrb(speed)) + "/s"
        tot = hrb(total)
        cur = hrb(current)

        display = get_endgame_progress_display(int(perc), sp, cur, tot, eta)

        try:
            await reply.edit(f"`{display}`")
        except FloodWait as e:
            time.sleep(e.x)
            
