/* ============================================================
   GENIE — the overlay menu and the side drawer, funnelled
   ------------------------------------------------------------
   The reference is the macOS minimise: a window is not scaled down
   into the Dock, it is POURED into it. Three things make that read,
   and all three have to be there or it looks like a scale:

     1. THE NECK IS AT THE BUTTON, not at the panel's own edge. The
        shape pinches to roughly the width of the thing you clicked,
        at exactly the point you clicked it.
     2. THE SIDES ARE CURVED. A straight-sided funnel is a trapezoid
        and reads as perspective; the S-curve is what reads as liquid.
     3. THE FAR EDGE LEAVES FIRST AND ARRIVES FIRST. The panel stretches
        on the way out and the tail catches up at the end. Move both
        edges together and it is a slide, not a genie.

   HOW IT IS BUILT
   A clip-path polygon draws the silhouette — sampled along a smoothstep
   so the sides curve — and a transform, with its origin pinned to the
   trigger, carries the stretch. The transform's origin is the one point
   that does not move under a scale, so putting it on the trigger is what
   keeps the neck welded to the button for free, at every size, without
   any per-frame correction.

   Clip alone would not do: the panel's contents would sit at full size
   inside a 30px neck and you would read a wide word through a slot. The
   transform shrinks the contents into the neck, which is what the real
   thing does to the window it is pouring.

   WHY A MUTATION OBSERVER AND NOT A CLICK HANDLER
   The open and close wiring lives in three different page scripts. This
   watches the .open class those scripts already toggle, so it needs no
   hook in any of them and cannot fall out of step with one that changes.
   ============================================================ */
(function(){
  "use strict";
  if(matchMedia("(prefers-reduced-motion:reduce)").matches) return;
  /* no clip-path — the CSS transitions underneath are a complete, sensible
     open and close on their own, so leave them be */
  if(!(CSS && CSS.supports && CSS.supports("clip-path","polygon(0 0,1px 0,1px 1px)"))) return;

  /* the flag the stylesheet keys on to stand its own transform transitions
     down; set from here so a page without this script keeps them */
  document.documentElement.setAttribute("data-genie","");

  /* samples per side of the funnel. The silhouette is a smoothstep, which
     is gentle enough that sixteen points per side already read as a curve;
     past that it is only more string to build and more path to rasterise
     on every one of the sixty frames a second this now runs at. */
  var N = 16;
  var OPEN_MS = 640, SHUT_MS = 430;
  /* the drawer's backdrop holds visibility for 500ms after .open goes, so
     the closing run has to be done inside that or it is cut off mid-pour */

  function lerp(a,b,t){ return a + (b-a)*t; }
  function clamp01(v){ return v<0?0:v>1?1:v; }
  function smooth(t){ return t*t*(3-2*t); }                 /* the curved side */
  function easeIO(t){ return t<.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2; }

  /* ---------- EVERY CURVE STARTS AND STOPS AT REST ----------
     The head used to run on 1-(1-k)^3, which is moving at three times the
     average rate at k=0: the panel left the button already at full speed,
     which is a flick, not a pour. The tail ran on k^2.6, whose slope at
     k=1 is 2.6 — it arrived at speed and stopped dead against its final
     position, and that was the knock at the end of the open.

     Both are now written as a smoothstep composed with a shaping power.
     smooth() is flat at 0 and at 1, and composing preserves that, so the
     head still leaves first and the tail still lags, but nothing in the
     run begins or ends with velocity to shed. */
  function headCurve(t){ var s = smooth(t); return 1 - Math.pow(1-s, 3); }
  function tailCurve(t){ return Math.pow(smooth(t), 2.5); }

  /* ---------- one frame of the pour ----------
     k is 0 at the button and 1 at the panel's resting shape. Everything
     below is in the panel's own coordinates, which is why the trigger can
     sit at a negative offset: it usually does, being outside the panel. */
  function frame(g, k){
    var W = g.w, H = g.h, vert = g.vert;
    var L = vert ? H : W;                 /* along the pour               */
    var X = vert ? W : H;                 /* across it                    */
    var tAlong = vert ? g.ty : g.tx;      /* the trigger, along the pour  */
    var tCross = vert ? g.tx : g.ty;      /* and across it                */
    /* the near edge is the one the button is on: the top of a panel that
       hangs below the bar, the right-hand edge of one that slides in from
       the right */
    var nearEnd = g.nearAtZero ? 0 : L;
    var farEnd  = g.nearAtZero ? L : 0;

    /* WHERE THE TWO EDGES ARE, AND THEN WHAT TRANSFORM PUTS THEM THERE.
       The first version set a scale and let the edges fall where they may,
       and the neck could never reach the button: a clip only REMOVES, so
       nothing can be drawn above the panel's own top edge, and the top
       edge was wherever a single scale had left it — a visible gap between
       the funnel and the burger for most of the run.

       So the edges are decided first. The tail stays welded to the button
       on a late power curve and comes home over the last quarter; the head
       leaves at once on an ease-out. Two edges moving at different rates
       is the stretch, and a single scale cannot do it — hence a scale AND
       a translation, solved from the two positions rather than guessed:

         map(q) = O + s(q - O) + d      with O at the trigger
         s = (far - near) / (farEnd - nearEnd)
         d = near - O - s(nearEnd - O)

       The clip then only has to draw the silhouette inside the box, and
       the apex is placed at whichever local point the transform maps onto
       the trigger — which is O - d/s, straight from the same equation. */
    var near = lerp(tAlong, nearEnd, tailCurve(k));
    var far  = lerp(tAlong, farEnd,  headCurve(k));
    var span = farEnd - nearEnd;
    /* A SOFT FLOOR, BECAUSE A HARD ONE IS A CORNER.
       The two edges start together, so this ratio starts at zero and the
       apex below divides by it. It used to be clamped with a min, and the
       moment the real value overtook that minimum the scale changed slope
       in one step — a single sharp knock a couple of frames into the open,
       which is exactly where it was measured. A hyperbola does the same
       job without the corner: it sits at the floor when the ratio is tiny
       and becomes the ratio itself once that is the larger of the two,
       with a continuous derivative all the way through. */
    var raw = (far - near) / span;          /* runs 0 -> 1, never negative */
    var sA = Math.sqrt(raw*raw + 4e-4);     /* floor of .02, smoothly      */
    var dA = near - tAlong - sA * (nearEnd - tAlong);
    var apex = tAlong - dA / sA;         /* the local point that lands on it */

    /* the width fills in behind the length, which is the taffy */
    var sC = lerp(.06, 1, easeIO(k));

    /* the last stretch resolves the funnel into the plain rectangle the
       panel actually is — without this the neck would still be pinched
       once the thing had finished arriving */
    var rect = smooth(clamp01((k - .55) / .45));
    /* the neck is stated in screen pixels, so it is divided by the scale it
       is about to be multiplied by — otherwise it pinches to nothing early
       on, when that scale is at its smallest */
    var neckHalf = g.neck / 2 / Math.max(sC, .06);

    var a = [], b = [];
    for(var i = 0; i <= N; i++){
      var u = i / N;                       /* 0 at the neck, 1 at the head */
      var along = lerp(apex, farEnd, u);
      var p = smooth(u);
      var half = lerp(lerp(neckHalf, X/2, p), X/2, rect);
      var mid  = lerp(lerp(tCross,  X/2, p), X/2, rect);
      var lo = mid - half, hi = mid + half;
      if(vert){ a.push([lo, along]); b.push([hi, along]); }
      else    { a.push([along, lo]); b.push([along, hi]); }
    }
    b.reverse();
    var pts = a.concat(b).map(function(q){
      return q[0].toFixed(1) + "px " + q[1].toFixed(1) + "px";
    });

    return {
      clipPath: "polygon(" + pts.join(",") + ")",
      transform: (vert ? "translateY(" + dA.toFixed(2) + "px)"
                       : "translateX(" + dA.toFixed(2) + "px)") +
                 " scale(" + (vert ? sC : sA).toFixed(4) + "," +
                             (vert ? sA : sC).toFixed(4) + ")",
      /* eased, not a clamped ramp: the straight ramp reached full opacity
         at k=.18 and simply stopped, and that corner in the fade was
         visible as a small pop under everything else that was still moving */
      opacity: smooth(clamp01(k / .26)).toFixed(4)
    };
  }

  function measure(panel, trigger, vert, nearAtZero, neck){
    var r = panel.getBoundingClientRect();
    if(!r.width || !r.height) return null;
    var t = trigger && trigger.getBoundingClientRect();
    /* no trigger on screen — the pull-tab is parked off-stage while the
       drawer is open — so fall back to the corner it lives in, which is
       where the reader last saw it */
    var cx = t && t.width ? t.left + t.width/2  : (nearAtZero ? r.left + r.width/2 : r.right);
    var cy = t && t.height? t.top  + t.height/2 : (vert ? r.top : r.top + 40);
    return {
      w:r.width, h:r.height, vert:vert, nearAtZero:nearAtZero,
      tx:cx - r.left, ty:cy - r.top,
      neck: Math.max(18, Math.min(t && t.width ? (vert ? t.width : t.height) : 34, 64))
    };
  }

  /* ---------- DRIVEN PER FRAME, NOT KEYFRAMED ----------
     This was a list of keyframes handed to the Web Animations API, and it
     was the wrong tool twice over.

     It stepped. Between two keyframes the engine interpolates the polygon's
     points in a straight line, so the pour was a piecewise-linear
     approximation of a curve and the velocity changed at every joint.
     Measured on the head's position, the acceleration spiked at exactly
     1/18, 2/18, 3/18 of the run — once per joint, all the way down. Raising
     the count to 72 shrank the steps but could not remove them, because the
     corners were in the geometry and no easing reaches those.

     And it stalled. 73 keyframes, each carrying a polygon of forty-odd
     points, is some sixty kilobytes of geometry to build and parse in the
     single frame where the button was clicked: a 233ms hitch right at the
     start, which is the worst possible place for one.

     Computing the shape each frame from the continuous function fixes both
     at once — there are no joints to step over, and there is nothing to
     build up front. The per-frame cost is one polygon instead of 73. */
  function apply(panel, f){
    panel.style.clipPath = f.clipPath;
    panel.style.webkitClipPath = f.clipPath;
    panel.style.transform = f.transform;
    panel.style.opacity = f.opacity;
  }

  function release(panel){
    panel.style.clipPath = panel.style.webkitClipPath = "";
    panel.style.transform = panel.style.opacity = "";
    panel.style.willChange = panel.style.boxShadow = "";
  }

  /* ---------- THE BLUR STANDS DOWN WHILE THE PANEL MOVES ----------
     Measured, because it was not the obvious answer. With the pour running,
     a throttled desktop dropped 31 frames in 64; with the backdrop's blur
     switched off and nothing else changed, it dropped none. A clip-path
     change is a repaint, the panel is a child of the blurred backdrop, and
     a backdrop-filter re-runs whenever anything above it repaints — over
     the whole viewport, sixty times a second, to blur a scene nobody is
     looking at. Promoting either element to its own layer was tried and
     changed nothing; the invalidation is in the paint order, not the
     compositing.

     What is actually seen through that backdrop is the DIM, not the blur:
     it is a 60%-opaque dark wash, and the blur under it is a refinement on
     an already obscured page. So the wash stays and the blur is suspended
     for the few hundred milliseconds of the pour, then restored. On close
     it never comes back into view at all, because the backdrop has faded
     out by the time it is restored.

     Set as an attribute on the root for the stylesheet to match, NOT
     written to element.style here. Both arrive at the same computed value
     — and over three runs each, the inline write still cost sixteen
     dropped frames while the attribute costs none, because the rule is
     picked up by the ordinary style pass instead of dirtying the backdrop
     root on its own in the middle of the animation. */
  var moving = 0;
  function blur(on){
    moving += on ? -1 : 1;
    if(moving < 0) moving = 0;
    if(moving) document.documentElement.setAttribute("data-genie-moving","");
    else document.documentElement.removeAttribute("data-genie-moving");
  }

  /* ---------- WHEN THE BLUR IS ALLOWED BACK ----------
     Restoring it the instant the pour stopped put it back into the middle
     of something else. The menu's links arrive on their own staggered
     animation which is still running for half a second after the panel has
     finished — seven elements animating inside the blurred backdrop, each
     frame re-running the blur over the whole viewport. The pour itself held
     a flat 60fps and then the half second AFTER it ran at thirty.

     So the blur waits for the panel to be completely still: every
     unfinished animation inside it, whatever a page happens to put there.
     Endless ones are skipped — they would never resolve — and a cap
     guarantees the blur comes back even if something never settles.

     Closing needs the opposite: hold it until the backdrop has gone. The
     pour is shorter than the backdrop's own fade, so restoring on time
     would repaint a full-viewport blur onto something still visible, for
     no one's benefit. Past the fade the element is not painted at all and
     the restore is free. */
  function settle(panel, opening){
    var once = false;
    function back(){ if(once) return; once = true; blur(true); }
    if(!opening){ setTimeout(back, 620); return; }
    var list = [];
    try{
      list = panel.getAnimations({subtree:true}).filter(function(a){
        var t = a.effect && a.effect.getTiming && a.effect.getTiming();
        return t && t.iterations !== Infinity;
      });
    }catch(e){}
    if(!list.length){ back(); return; }
    Promise.all(list.map(function(a){ return a.finished.catch(function(){}); })).then(back);
    setTimeout(back, 1600);
  }

  function run(panel, g, opening){
    var s = panel.__genie;
    if(s){ cancelAnimationFrame(s.raf); blur(true); }
    blur(false);

    /* a toggle mid-pour picks up where the last one had got to, rather than
       snapping to the end and running the other way from there */
    var from = s && s.k != null ? s.k : (opening ? 0 : 1);
    var to = opening ? 1 : 0;
    var dist = Math.abs(to - from);
    var dur = Math.max(120, (opening ? OPEN_MS : SHUT_MS) * dist);

    /* THE ONE LINE THE SHAPE RESTS ON.
       A scale leaves exactly one point where it is: the transform origin.
       Put that point on the button and the neck is welded there for the
       whole run, at any viewport, with no per-frame correction. */
    panel.style.transformOrigin = g.tx.toFixed(1) + "px " + g.ty.toFixed(1) + "px";
    /* promoted for the duration, so repainting the clip does not drag the
       blurred backdrop underneath it through a re-render every frame */
    panel.style.willChange = "transform, clip-path, opacity";
    /* and the drop shadow is stood down while it moves: an 80px blur
       re-rasterised on a changing silhouette, sixty times a second, costs
       more than the whole rest of the effect and cannot be seen during it */
    panel.style.boxShadow = "none";

    var t0 = 0;
    var st = {k: from, raf: 0};
    panel.__genie = st;

    function step(now){
      if(!t0) t0 = now;
      var p = clamp01((now - t0) / dur);
      var k = from + (to - from) * p;
      st.k = k;
      apply(panel, frame(g, k));
      if(p < 1){ st.raf = requestAnimationFrame(step); return; }
      /* handing the resting shape back to the stylesheet: the last frame
         and the CSS state are the same picture, so the swap is invisible,
         and holding it here would freeze the panel against a later change */
      panel.__genie = null;
      release(panel);
      settle(panel, opening);
    }
    /* the first frame is written now rather than waiting for the callback,
       so the panel is never shown at its CSS resting size for one frame */
    apply(panel, frame(g, from));
    st.raf = requestAnimationFrame(step);
  }

  function wire(host, panelSel, triggerSel, vert, nearAtZero){
    var root = document.querySelector(host);
    if(!root) return;
    var panel = root.querySelector(panelSel);
    if(!panel) return;
    var was = root.classList.contains("open");
    new MutationObserver(function(){
      var now = root.classList.contains("open");
      if(now === was) return;
      was = now;
      /* measured at the moment it is wanted, never cached: the panel's box
         moves with the viewport and the bar's own show/hide state */
      var g = measure(panel, document.querySelector(triggerSel), vert, nearAtZero);
      if(g) run(panel, g, now);
    }).observe(root, {attributes:true, attributeFilter:["class"]});
  }

  /* the card hangs below the bar, so it pours downward out of the burger */
  wire("#menu", ".menu-card", "#burger", true, true);
  /* the drawer comes in from the right, so it pours sideways out of the tab */
  wire("#sidePane", ".sd-inner", "#sideTab", false, false);
  /* the simulation's conversation pours sideways out of its own button,
     which is the whole reason that button sits where it does. wire()
     returns the moment the host is not on the page, so this costs the
     other pages nothing. */
  wire("#chatHost", "#chat", "#chatFab", false, false);
})();
