# cyscheduler

Creates polls to decide on "meetings" on strawpoll.me

Polls are created:
- From the next day onwards (can be overridden)
- Every day or only on weekends (Friday, Saturday and Sunday)
- Times can wary for weekdays and weekends (Saturday and Sunday)

The script just prints the URL at the end, which can be piped into the clipboard.

## Examples

```
./cyscheduler.py -t "A" --repeat 9 --weekdayoptions "18:00 - 19:00" --weekendoptions "14:00 - 15:00" "20:00 - 21:00" --fromdeltadays 2
```

- This creates a poll with the title "A"
- Options on 9 days
- On Friday, Saturday and Sundays only (default)
- Friday uses 18:00 - 19:00 as (only) option
- Saturday and Sunday have two options
- Starting from the day after tomorrow

```
./cyscheduler.py -t "B" --fullweek | pbcopy
```

- This creates a poll with the title "B"
- Options on 6 days (default)
- Weekdays use 19:30 - 22:00 as only option (default)
- Weekends use 14:00 - 17:00 and 19:30 - 22:00 as options (default)
- The resulting poll URL is copied into the clipboard (MacOS)

## .poll

If you keep using certain settings you can either create an alias or create a ".poll" file in this directoy (to avoid going through the trouble of having this script in $PATH).
.poll files are ignored via .gitignore.


Here's an example for amongus.poll:
```
#!/bin/bash

./cyscheduler.py -t "Among Us" --repeat 6 --weekdayoptions "20:00 - 23:00" --weekendoptions "14:00 - 17:00" "19:00 - 22:00" | pbcopy
```
