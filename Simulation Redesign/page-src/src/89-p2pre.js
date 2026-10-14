/* page 2: open with the example user's own targets, and refresh on every target change */
Object.assign(TS.user, EXAMPLE_SET);
p2listeners.push(() => refresh(null));
