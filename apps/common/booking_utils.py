from datetime import datetime, timedelta

def compute_interval(date_str, time_str, duration_str):
    # date:     `2025-12-21` (Year-Month-Day)
    # time:     `04:12:09`   (Hour-Min-Second)
    # duration: `1 12:20:00` (Day Hour:Min:second)
    # duration: `02:30:00`   (Hour:min:sec)

    from_str = f"{date_str} {time_str}"
    from_datetime = datetime.strptime(from_str, '%Y-%m-%d %H:%M:%S')

    parts_of_duration = duration_str.split() # ['1', 'day,', '12:20:00'] if we gave: '1 12:20:00'
    if len(parts_of_duration) == 3:
        day_part = int(parts_of_duration[0])
        time_part = parts_of_duration[2]
        hours, minutes, seconds = map(int, time_part.split(':'))
        duration = timedelta(days=day_part, hours=hours, minutes=minutes, seconds=seconds)
    else:
        hours, minutes, seconds = map(int, duration_str.split(':'))
        duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    to_datetime = from_datetime + duration
    return from_datetime, to_datetime


# start, end = compute_interval('2025-03-20', '18:59:51', '3 09:02:20')
# print(start) # 2025-03-20 18:59:51
# print(end)   # 2025-03-24 04:02:11