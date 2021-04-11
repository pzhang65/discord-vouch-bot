# TODO LIST

### Urgent
- [ ] Add regex to command recognition
- [ ] Change embed author to server nickname with no discriminator

### Features
- [ ] Add cooldown remaining time to cooldown messages
- [ ] Extra tags i.e. Scammer, whale, etc.
- [ ] ranking list for most vouches/least vouches etc.


## Completed
- [x] Check for duplicate vouchers
- [x] Users can change past vouches
- [x] Vouching cooldowns
- [x] administrator role (able to edit user/vouches)
- [x] check vouch -> grab discord picture too
- [x] Dockerize project for deployment
- [x] Deploy to an ec2 instance
- [x] change positive/negative to +1/-1
- [x] Vouches cannot be set for users who do are no in users table yet. (Create a user first then set vouch if not user)
- [x] Vouch history
- [x] Migrate user table primary key to discord ID **Discord nitro reverts discord username ID upon expiry so users may unexpectedly lose vouches
  * Alembic upgrade head to add new columns
  * $convertusers and $convertvouches
  * change PK args in model columns
  * reassign PKs in users and vouches table
