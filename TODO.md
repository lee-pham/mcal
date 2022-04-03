# TODO:

## Bugs

- [x] if current day of multiday event is between the start and end day, event does not show up on timeline
- [x] Fix ordering of multiday events in calendar view
- [x] If four events in a day, don't show 3 events and a 1more event overflow, display all 4 instead
- [ ] If multiday event is on maxevents + 1 of previous, the current event gets displayed on the maxevent + 1 line
- [ ] If multiday event spans across weeks, it takes the lane of the previous week, which isn't consistent with how gcal
  handles it
## UI

### Calendar

- [x] year and time font need to be slightly smaller than the calendar day font
- [x] overflow in red, event in gray
- [x] long line for multi day events
- [x] multiday line in red
- [x] show event label again on new week start for continuity
- [x] bullet point is all day event indicator for single day
- [ ] fix year and time margins
- [ ] match weekday font size to calendary number days font size
- [ ] gap between multiday events that end and start consecutively 
- [ ] bullet point to be red
- [ ] increase width between columns
- [ ] noto serif
- [ ] roboto slab
- [ ] bitter (font)
- [ ] If less than four events, display max lines if event name long

### Timeline

- [x] thinner line for timeline line
- [x] filled black circle while event is going on
- [x] all day event as 00:00 event
- [x] all day multi day italics surrounded by bullet
- [x] all day single day is italics no bullet
- [ ] text start aligns with dot
- [ ] fix overlapping as it's not perfected yet