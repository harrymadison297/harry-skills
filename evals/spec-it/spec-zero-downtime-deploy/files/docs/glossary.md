# Internal app deployment

How the internal app reaches its servers.

## Language

**Release**:
An immutable, versioned build of the app.
_Avoid_: Version, package, build

**Deploy**:
Making one release the running version on one host.
_Avoid_: Push, ship

**Rollout**:
One release going through all hosts, one deploy after another.
_Avoid_: Wave, batch

**Rollback**:
Deploying an earlier release again on a host.
_Avoid_: Revert, undo

**Host**:
A virtual machine that runs the app.
_Avoid_: Node, server, box
