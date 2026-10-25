# Interview: battery node

Round 1 (answered by the user)

**Q1 Is a battery worth it, instead of a longer USB cable?**
Yes. There is no outlet where the node has to sit.

**Q2 Should the node run one cycle every five minutes?**
Yes.

**Q3 Should one battery last at least six months?**
Yes.

**Q4 Should the node give up after about ten seconds when the network is down, skip that report, and sleep until the next cycle, with no queue of old samples?**
Yes. A lost sample now and then is fine.

**Q5 Should every report also carry the battery level?**
Yes.

**Q6 Should the topic and the t and h fields stay exactly as they are?**
Yes. Home Assistant reads them.

**Q7 Should the firmware be updated over USB only, with no over-the-air update?**
Yes.

**Q8 Should the LED stay off during normal operation?**
Yes.

Extra remark from the user: the readings should be accurate.

Held back, never asked: what the node should do when the battery is nearly empty.
