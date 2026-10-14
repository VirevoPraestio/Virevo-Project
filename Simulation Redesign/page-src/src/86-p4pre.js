/* page 4: a full six picked (Tojo's balanced six), and refresh on every change */
S3.sel = suggest3();
p4listeners.push(() => refresh(null));
