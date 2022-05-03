import os

dates = []

### [ [Day of the week, [Time of day], [Line Jobs Available], [Total Jobs Available],
###   Line Jobs Daily Max, Total Jobs Daily Max]
daily_data = [ ['Sunday', [], [], [], 0, 0], ['Monday', [], [], [], 0, 0], ['Tuesday', [], [], [], 0, 0],
             ['Wednesday', [], [], [], 0, 0], ['Thusday', [], [], [], 0, 0], ['Friday', [], [], [], 0, 0],
             ['Saturday', [], [], [], 0, 0] ]

f = open('Rev_Job_Trends/rev_jobs.txt', 'r')

for row in f:
    row = row.split(' ')
    day = row[0] # First value from line of text file
    match day:
        case 'Sunday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])
            
            daily_data[0][1].append(row[2] + " " + row[3])
            daily_data[0][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[0][3].append(int(row[4]))
        case 'Monday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])

            daily_data[1][1].append(row[2] + " " + row[3])
            daily_data[1][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[1][3].append(int(row[4]))
        case 'Tuesday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])

            daily_data[2][1].append(row[2] + " " + row[3])
            daily_data[2][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[2][3].append(int(row[4]))
        case 'Wednesday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])

            daily_data[3][1].append(row[2] + " " + row[3])
            daily_data[3][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[3][3].append(int(row[4]))
        case 'Thursday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])

            daily_data[4][1].append(row[2] + " " + row[3])
            daily_data[4][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[4][3].append(int(row[4]))
        case 'Friday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])

            daily_data[5][1].append(row[2] + " " + row[3])
            daily_data[5][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[5][3].append(int(row[4]))
        case 'Saturday':
            daily_data[0][4] = max(daily_data[0][2])
            daily_data[0][5] = max(daily_data[0][3])

            daily_data[6][1].append(row[2] + " " + row[3])
            daily_data[6][2].append(int(row[5].rstrip(os.linesep).rstrip('\t#')))
            daily_data[6][3].append(int(row[4]))
    dates.append(row[1])

for day in daily_data:
    print(day)

'''
int_line_jobs = []
int_total_jobs = []
for item in daily_data[0][3]:
    int_line_jobs.append(int(item))
for item in daily_data[0][4]:
    int_total_jobs.append(int(item))
'''
# TODO: Will run into problem when weeks roll over -- I want the time of maximum jobs for THIS Sunday, not all Sundays, etc.
    # > Set up folders and files for year > month > week and start fresh with new text file each Monday
        # >> Add a method that will aggregate data over specified time period for larger than weekly graph

# TODO: Create UI for desktop that will pop up and update once every morning with current Dashboard stats

'''
    If it's Monday: (When is this determined, and by what program -- the script, the rev program?)
        - Use data from that month to create a graph and save the graph image to {.../Desktop/Rev_Job_Trends/Year/Month} directory
            - Append rev_jobs txt file to {.../Desktop/Rev_Job_Trends/Year/Month/jobs.txt}
                - After saving file successfully, delete all data from rev_jobs txt file to clear for new week and avoid mixing data

'''
