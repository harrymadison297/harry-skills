---
type: llm
focus: trace
weight: 1
---

The Decisions section records at least five of these settled items, each with a reason: people use the app during the day; zero downtime means no user-visible failed request in a normal deploy; requests in flight get thirty seconds to finish; DNS round-robin stays with no new load balancer; hosts are deployed one at a time and the deploy stops at the first unhealthy host; migrations must work with the previous release and run once before the first host; one command rolls all hosts back; a host counts as updated only after it answers a health request; a person runs deploys by hand.
