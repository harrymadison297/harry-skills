# Deep-module vocabulary

Use these words, and only these, for the same ideas.

- **Module.** Anything with an interface and an implementation: a function, a class, a package, a service.
- **Interface.** Everything a caller must know to use the module: signatures, ordering, error behavior, invariants. Not only the types.
- **Depth.** The ratio of behavior to interface. A deep module hides a lot behind a small interface. A shallow module's interface is nearly as complex as its body, so it adds a hop and no value.
- **Seam.** A place where behavior can change without editing the code at that place. A test seam is a public boundary where a test observes behavior.
- **Adapter.** Code that fits one side of a seam to the other, such as a real database versus an in-memory one.
- **Leverage.** What callers gain from depth: more behavior per thing they must learn.
- **Locality.** A change or a bug stays in one place.

## Deletion test

Imagine deleting the module. If the complexity vanishes, the module was a pass-through, so remove it. If the complexity reappears across many callers, the module earned its place.

## Applying it

- Prefer one deep module to several shallow ones that call each other.
- Put a seam where two things vary independently, such as the store and the transport. Do not put one inside a module just to make it testable.
- A test that needs to reach past the interface means the seam is in the wrong place.
