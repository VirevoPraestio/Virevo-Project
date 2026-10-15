# Simulation redesign

Working folder for the rebuild of `Simulation Version 16.05/simulation.html`.

- `SIMULATION-LOGIC.md`: how the current page builds its formula, targets, "achievable" values and dream costs, and the faults found when it is run on the sample data.
- `out/sim-p1-options.html`: page 1 (Your data), four options (A Lights on, B One formula, C Records room, D The trace). Live: https://claude.ai/artifact/TJrgZ8jKviG5HGtWrsp8rE
- `page-src/`: sources. `python3 build.py` joins `src/00-head.html` (with the suites' shared CSS from `suite-base.css`), `10-data.js` (data families, files, measures, KPIs, links), `20-runtime.js` (intake, readings, hover peek, detail sheet, chat), the look files `3x-*.js` and `90-init.js`. Set `FONTS` to the font folder for the `.preview.html`.

The left panel of the old page is not designed here; it will be replaced.
