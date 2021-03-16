# TODO LIST

### Urgent


### Features
- [ ] Extra tags i.e. Scammer, whale, etc.
- [ ] ranking list for most vouches/least vouches etc.


## Completed
- [x] Check for duplicate vouchers
- [x] Change vouch option
- [x] Vouching cooldowns
- [x] administrator role (able to edit user/vouches)
- [x] check vouch -> grab discord picture too
- [x] Dockerize project for deployment
- [x] Deploy to an ec2 instance
- [x] change positive/negative to +1/-1
- [x] Vouches cannot be set for users who do are no in users table yet. (Create a user first then set vouch if not user)

Vouching cooldowns:
- cooldown for receiving and giving?
- two columns, last_given, last_received
- check last_given when giving vouch and if time delta > 1 hr, return
- last_received same idea (maybe not good to have a received cooldown)
