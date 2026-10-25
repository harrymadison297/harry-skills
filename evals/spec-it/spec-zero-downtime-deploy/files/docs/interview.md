# Interview: zero-downtime deploys

Round 1 (answered by the user)

**Q1 Is this worth solving, or can deploys wait for quiet hours?**
Worth solving. People use the app all day.

**Q2 Should zero downtime mean no user-visible failed request in a normal deploy, with in-flight requests getting thirty seconds to finish?**
Yes.

**Q3 Should DNS round-robin stay, with no new load balancer?**
Yes.

**Q4 Should a rollout deploy one host at a time and stop at the first host that is not healthy, putting that host back on the previous release?**
Yes.

**Q5 Should every migration work with the previous release too, and run once, before the first host?**
Yes.

**Q6 Should one command return all three hosts to the last good release?**
Yes.

**Q7 Should a host count as updated only after it answers a health request?**
Yes.

**Q8 Should a person keep running deploys by hand from one machine, with no CI?**
Yes.

Extra remark from the user: deploys should be quick.

Held back, never asked: how many past releases to keep on each host.
