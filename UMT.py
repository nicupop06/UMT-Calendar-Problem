# need this for using regex to get numbers from input string
import re

# Declaring the input for the problem
# I could read this from console, but it's easier to check from here
# The B in calendar1B and calendar2B stands for Booked, and represents the intervals when the two people are busy in that day
# The R in calendar1R and calendar2R stands for Range, and represents the intervals when the two are working in that day
# meeting_time represents for how long they need to meet
calendar1B = "[['9:00','10:30'], ['12:00','13:00'], ['16:00','18:00]]"
calendar1R = "['9:00','20:00']"

calendar2B = "[['10:00','11:30'], ['12:30','14:30'],['14:30','15:00], ['16:00','17:00']]"
calendar2R = "['10:00','18:30']"

meeting_time = 30

# we create lists of integers, so we can find time intervals for the meetings
calendar1B = [int(s) for s in re.findall(r'\d+', calendar1B)]
calendar1R = [int(s) for s in re.findall(r'\d+', calendar1R)]
calendar2B = [int(s) for s in re.findall(r'\d+', calendar2B)]
calendar2R = [int(s) for s in re.findall(r'\d+', calendar2R)]

i = 0
j = 0

# The F in calendar1F and calendar2F stands for Free, and represents when the two people are free in that day
calendar1F = []
calendar2F = []

# we create the Free list for the first person, using the list we have from input
if calendar1B[0] > calendar1R[0]:
    calendar1F.append(calendar1R[0])
    calendar1F.append(calendar1R[1])
    calendar1F.append(calendar1B[0])
    calendar1F.append(calendar1B[1])

if calendar1B[0] == calendar1R[0] and calendar1R[1] < calendar1B[1]:
    calendar1F.append(calendar1R[0])
    calendar1F.append(calendar1R[1])
    calendar1F.append(calendar1B[0])
    calendar1F.append(calendar1B[1])

i = 2
while i < len(calendar1B) - 4:
    calendar1F.append(calendar1B[i])
    calendar1F.append(calendar1B[i + 1])
    calendar1F.append(calendar1B[i + 2])
    calendar1F.append(calendar1B[i + 3])
    i += 4

if calendar1B[-2] != calendar1R[-2]:
    calendar1F.append(calendar1B[-2])
    calendar1F.append(calendar1B[-1])
    calendar1F.append(calendar1R[2])
    calendar1F.append(calendar1R[3])

# -----------------------------------------
# we do the same for the second person

if calendar2B[0] > calendar2R[0]:
    calendar2F.append(calendar2R[0])
    calendar2F.append(calendar2R[1])
    calendar2F.append(calendar2B[0])
    calendar2F.append(calendar2B[1])

if calendar2B[0] == calendar2R[0] and calendar2R[1] < calendar2B[1]:
    calendar2F.append(calendar2R[0])
    calendar2F.append(calendar2R[1])
    calendar2F.append(calendar2B[0])
    calendar2F.append(calendar2B[1])

i = 2
while i < len(calendar2B) - 4:
    calendar2F.append(calendar2B[i])
    calendar2F.append(calendar2B[i + 1])
    calendar2F.append(calendar2B[i + 2])
    calendar2F.append(calendar2B[i + 3])
    i += 4

if calendar2B[-2] != calendar2R[-2]:
    calendar2F.append(calendar2B[-2])
    calendar2F.append(calendar2B[-1])
    calendar2F.append(calendar2R[2])
    calendar2F.append(calendar2R[3])

# I noticed that how I implemented takes (14:00 to 14:00) as a free time if one is start time and one is end time
# so I need to remove that
for i in range(0, len(calendar1F) - 4):
    if calendar1F[i] == calendar1F[i + 2] and calendar1F[i + 1] == calendar1F[i + 3] and i % 4 == 0:
        del calendar1F[i:i + 4]
i = 0
n = len(calendar2F) - 4
while i < n:
    if calendar2F[i] == calendar2F[i + 2] and calendar2F[i + 1] == calendar2F[i + 3] and i % 4 == 0:
        del calendar2F[i:i + 4]
        n -= 4
    i += 1


# Here I convert the two lists so they contain lists of intervals instead of being a linear list
intervals1 = [(calendar1F[i], calendar1F[i + 1], calendar1F[i + 2], calendar1F[i + 3]) for i in
              range(0, len(calendar1F), 4)]
intervals2 = [(calendar2F[i], calendar2F[i + 1], calendar2F[i + 2], calendar2F[i + 3]) for i in
              range(0, len(calendar2F), 4)]

# This function returns the common interval given two time intervals
def get_common_intervals(interval1, interval2):
    start1, end1, start2, end2 = interval1[0] * 60 + interval1[1], interval1[2] * 60 + interval1[3], interval2[0] * 60 + \
                                 interval2[1], interval2[2] * 60 + interval2[3]
    common_start = max(start1, start2)
    common_end = min(end1, end2)
    if common_start < common_end:
        return common_start // 60, common_start % 60, common_end // 60, common_end % 60
    elif interval1[0] * 60 + interval1[1] > interval2[2] * 60 + interval2[3]:
        return get_common_intervals(interval2, interval1)
    else:
        return []

# This function returns the number of minutes that are in a time interval
def interval_minutes(interval):
    start_hour, start_minute, end_hour, end_minute = interval
    return (end_hour - start_hour) * 60 + (end_minute - start_minute)


# Now for each free time interval, we check if it has enough minutes and if so, we print it
for el1 in intervals1:
    for el2 in intervals2:
        common_intervals = get_common_intervals(el1, el2)
        if common_intervals and interval_minutes(common_intervals) >= meeting_time:
            print(str(common_intervals[0]) + ":" + str(common_intervals[1]) + " - " + str(common_intervals[2]) + ":" + str(common_intervals[3]))
            
