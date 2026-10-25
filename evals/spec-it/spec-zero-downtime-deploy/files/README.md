# Internal app

Runs on three Ubuntu 22.04 VMs (web1, web2, web3). DNS round-robin sends users to any of them. Deploy with ./deploy.sh.

Database changes: run migrations/ by hand on web1 before you deploy.
