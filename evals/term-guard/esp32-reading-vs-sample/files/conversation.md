# Conversation so far

**User:** The node will sleep between cycles. We decided: unsent samples are kept in RTC memory, not written to flash. That means they are lost if power is cut, and I accept that, because flash wears out and the node reports often. I know writing to flash would be safer, but I am choosing RTC memory.

**Assistant:** Understood, unsent samples go to RTC memory.

**User:** Also make the LED blink once on every report, just so I can see it work.

**Assistant:** Noted.

**User:** One more word for the docs: a Cycle is one wake-up, where the node takes a sample, tries to report it, and goes back to sleep. Please use "Cycle" for that from now on.

**Assistant:** Noted.

**User (latest message):** Each time it wakes up it takes a measurement and sends the message, and if the Wi-Fi is down it just keeps the reading until the next boot, then retries with a 5 second timeout.
