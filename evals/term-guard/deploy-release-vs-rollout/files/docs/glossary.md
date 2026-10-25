# Internal app deployment

How the internal app reaches its servers.

## Language

**Release**:
An immutable, versioned build of the app.
_Avoid_: Version, package, build

**Deploy**:
Making one release the running version on one host.
_Avoid_: Push, rollout, ship

**Host**:
A virtual machine that runs the app.
_Avoid_: Node, server, box
