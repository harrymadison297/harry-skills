# Conversation so far

**User:** We decided how releases are stored: each release goes in its own directory under /srv/app/releases/<id>, and a symlink called current points at the live one, switched atomically. We keep the last five. I know rsync over one directory is simpler, but I am choosing release directories so a rollback is instant.

**Assistant:** Understood, release directories with an atomic symlink.

**User:** Also put a timestamp on every line of the deploy log.

**Assistant:** Noted.

**User:** One more word for the docs: a Rollback is deploying an earlier release again on a host. Please use "Rollback" for that from now on.

**Assistant:** Noted.

**User (latest message):** When we push a new version it should roll out to each server one node at a time, and a rollback is just deploying the previous release. The health check gets a 10 second timeout.
