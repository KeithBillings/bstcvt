
import argparse
from datetime import datetime, timedelta
import pytz


def add_space_before_ampm(time_str):
    if "am" in time_str and " am" not in time_str:
        time_str = time_str.replace("am", " am")
    elif "pm" in time_str and " pm" not in time_str:
        time_str = time_str.replace("pm", " pm")
    return time_str


def parse_time(time_str):
    try:
        if ":" in time_str and ("am" in time_str or "pm" in time_str):
            return datetime.strptime(time_str, "%I:%M %p").time()
        elif ("am" in time_str or "pm" in time_str) and ":" not in time_str:
            new_time = add_space_before_ampm(time_str)
            return datetime.strptime(new_time, "%I %p").time()
        elif time_str.count(":") == 2 and ("am" not in time_str or "pm" not in time_str):
            return datetime.strptime(time_str, "%H:%M:%S").time()
        elif ":" in time_str and ("am" not in time_str or "pm" not in time_str):
            return datetime.strptime(time_str, "%H:%M").time()
        elif ":" in time_str and "am" not in time_str and "pm" not in time_str:
            return datetime.strptime(time_str, "%H:%M:%S").time()
        elif len(time_str) == 4:
            return datetime.strptime(time_str, "%H%M").time()
        elif len(time_str) == 6:
            return datetime.strptime(time_str, "%H%M%S").time()
        elif len(time_str) == 1 or len(time_str) == 2:
            return datetime.strptime(time_str, "%H").time()
    except ValueError:
        return None


def bst_to_utc(bst_time):
    # Create a datetime object with today's date and the parsed BST time
    today = datetime.now().date()
    bst_datetime = datetime.combine(today, bst_time)

    # Make it timezone-aware (BST is UTC+1)
    bst = pytz.timezone('Europe/London')
    # is_dst=True indicates Daylight Saving Time
    bst_datetime = bst.localize(bst_datetime, is_dst=True)

    # Convert to UTC
    utc_datetime = bst_datetime.astimezone(pytz.UTC)

    return utc_datetime


def utc_to_local(utc_time):
    local_tz = pytz.timezone('America/Los_Angeles')  # Pacific Time
    local_time = utc_time.astimezone(local_tz)
    return local_time


def convert_bst_to_local(time_str):
    # Step 1: Parse the time string to a datetime.time object
    bst_time = parse_time(time_str)
    if bst_time is None:
        return "Invalid time format"

    # Step 2: Convert BST to UTC
    utc_time = bst_to_utc(bst_time)

    # Step 3: Convert UTC to Pacific Time
    local_time = utc_to_local(utc_time)

    return local_time.time()


def main():
    parser = argparse.ArgumentParser(description='Convert BST to local time.')
    parser.add_argument(
        'time', type=str, help='Time in BST to convert to local time.')

    args = parser.parse_args()
    bst_time_str = args.time

    local_time = convert_bst_to_local(bst_time_str)
    print(f"Local time: {local_time}")


if __name__ == '__main__':
    main()
