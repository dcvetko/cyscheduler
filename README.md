# cyscheduler

Creates polls to decide on "meetings" on strawpoll.me

Polls are created:
- From the next day onwards
- Every day or only on weekends (Friday, Saturday and Sunday)
- Times can wary for weekdays and weekends (Saturday and Sunday)

The script just prints the URL at the end, which can be piped into the clipboard.

## Examples

```
./cyscheduler.py -t "Among Us" --repeat 9 --weekdayoptions "18:00 - 19:00" --weekendoptions "14:00 - 15:00" "20:00 - 21:00"
```

- This creates a poll with the title "Among Us"
- Options on 9 days
- On Friday, Saturday and Sundays only
- Friday uses 18:00 - 19:00 as (only) option
- Saturday and Sunday have two options

```
./cyscheduler.py -t "Raid" --fullweek | pbcopy
```

- This creates a poll with the title "Raid"
- Options on 6 days (default)
- Weekdays use 19:30 - 22:00 as only option (default)
- Weekends use 14:00 - 17:00 and 19:30 - 22:00 as options (default)
- The resulting poll URL is copied into the clipboard (MacOS)
