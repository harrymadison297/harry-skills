# Conversation so far

**User:** For offline sync, I decided that notes get their ids on the device as UUIDs. I do not want to ever migrate ids again, and two devices must never hand out the same id. I know the server database is simpler with integer ids, but I am choosing UUIDs.

**Assistant:** Understood, UUIDs created on the device.

**User:** Also, show every date in the UI as ISO 8601, I just prefer it.

**Assistant:** Noted.

**User:** One more word for the docs: a Replica is one device's full copy of the notes. Please use "Replica" for that from now on.

**Assistant:** Noted.

**User (latest message):** Now the delete behaviour. When someone deletes a folder, its memos should sit in a trash for 30 days before they are really gone, and a sync retry should give up after a 30 second timeout. A page can sit in many folders, like a tag really.
