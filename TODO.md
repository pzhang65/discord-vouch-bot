# TODO LIST

### Urgent
- [ ] administrator role (able to edit user/vouches)
- [ ] check vouch -> grab discord picture too
- [ ] Dockerize project for deployment

### Features
- [ ] Extra tags i.e. Scammer, whale, etc.
- [ ] ranking list for most vouches/least vouches etc.


## Completed
- [x] Check for duplicate vouchers
- [x] Change vouch option
- [x] Vouching cooldowns

Vouching cooldowns:
- cooldown for receiving and giving?
- two columns, last_given, last_received
- check last_given when giving vouch and if time delta > 1 hr, return
- last_received same idea (maybe not good to have a received cooldown)
