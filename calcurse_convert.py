import re
import dateutil.parser
import datetime


def next_day_from_str(date):
    return dateutil.parser.parse(date) + datetime.timedelta(days=1)


def convert_ics(infile, outfile):
    with open(infile) as fs:
        content = fs.readlines()

    p = re.compile('^DTSTART:[0-9]{8}$')
    new_content = []
    for line in content:
        if p.match(line):
            day = line.split(':')[1]
            new_content.append('DTSTART;VALUE=DATE:' + day)

            # not needed?
            # next_day = next_day_from_str(day)
            # new_line = 'DTEND;VALUE=DATE:' + next_day.strftime("%Y%m%d") + '\n'
            # new_content.append(new_line)
        else:
            new_content.append(line)

    with open(outfile, 'w') as fs:
        fs.write(''.join(new_content))


if __name__ == '__main__':
    infile = 'calcurse_cal.ics'
    outfile = 'cal.ics'
    convert_ics(infile, outfile)
