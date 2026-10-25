#!/usr/bin/env bash
set -e
for host in $(cat hosts); do
  rsync -az --delete ./app/ "$host:/srv/app/"
  ssh "$host" 'sudo systemctl restart app'
done
