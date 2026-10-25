---
type: llm
focus: trace
weight: 1
---

The reply points out that deploy.sh overwrites /srv/app in place with rsync and keeps no previous release, which contradicts the user's claim that a rollback is just deploying the previous release.
