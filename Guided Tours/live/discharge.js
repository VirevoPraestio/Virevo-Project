/* ============================================================
   discharge.js — the discharge screen, before the animation
   ------------------------------------------------------------
   Deliberately small. This is the static clone, and everything
   here is the behaviour a control implies just by looking the
   way it does: a pill that looks pressed can be pressed, a
   counter that says "none marked yet" counts, a textarea that
   grows with what you type.

   The animation passes come later and will attach to the same
   hooks rather than replace them.
   ============================================================ */
(function () {
  "use strict";

  var $  = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- pill groups ----------
     One pressed at a time, and the group is whatever [role=group]
     encloses them — so a third group added later needs no JS. */
  $$('.pills[role="group"]').forEach(function (grp) {
    var pills = $$(".pill", grp);
    pills.forEach(function (p) {
      p.addEventListener("click", function () {
        pills.forEach(function (o) { o.setAttribute("aria-pressed", o === p ? "true" : "false"); });
      });
    });
  });

  /* ---------- the two counted lists ----------
     aria-pressed is the state; the count reads it rather than keeping
     a tally of its own, so the two can never disagree. */
  function counter(scope, out, none, one, many) {
    var box = $(scope), el = $(out);
    if (!box || !el) return;
    var btns = $$(".row-b", box);
    function tell() {
      var n = btns.filter(function (b) { return b.getAttribute("aria-pressed") === "true"; }).length;
      el.textContent = n === 0 ? none : (n === 1 ? one : many.replace("%", n));
    }
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
        tell();
      });
    });
    tell();
  }
  counter("#diagnosis",   "#diagCount", "None marked yet",  "1 marked",      "% marked");
  counter("#automations", "#planCount", "Nothing added yet", "1 added to plan", "% added to plan");

  /* ---------- the composer ---------- */
  var input = $("#ctIn"), form = $("#ctForm");
  if (form) {
    var setFootH = function () {
      var d = document.getElementById("dis");
      if (d) d.style.setProperty("--foot-h", Math.round(form.offsetHeight) + "px");
    };
    setFootH();
    window.__dgFoot = setFootH;
    if (window.ResizeObserver) new ResizeObserver(setFootH).observe(form);
    else window.addEventListener("resize", setFootH, { passive: true });
  }
  if (input) {
    var grow = function () {
      input.style.height = "auto";
      input.style.height = Math.min(input.scrollHeight, 190) + "px";
    };
    input.addEventListener("input", grow);
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey && form) { e.preventDefault(); form.requestSubmit ? form.requestSubmit() : form.dispatchEvent(new Event("submit", {cancelable:true})); }
    });
  }
  /* ---------- from the first screen to the second ----------
     Sending the first message is what starts the walk. What was typed is
     echoed into the panel rather than thrown away, so the screen that
     arrives is answering the question that was actually asked.

     The whole opening sequence is replayed by taking .go off and putting it
     back. The reflow between the two is not optional: without reading a
     layout property in between, the browser coalesces the removal and the
     addition into no change at all and nothing restarts. */
  var dis0 = $("#dis");

  /* ---------- the foot, and bringing a thing into view ----------
     On a phone the worksheet and the conversation are one scrolling column
     with the composer pinned under them, so two things change. The composer
     grows as you type and the column above has to know how tall it currently
     is — measured, not guessed. And "show me this" is a different sum
     depending on which layout you are in, so it is asked by measurement
     rather than told by a breakpoint, which goes stale when the CSS moves. */
  function scrollerEl() {
    var m = document.getElementById("disMain");
    if (!m) return null;
    var ov = getComputedStyle(m).overflowY;
    return (ov === "auto" || ov === "scroll") ? m : null;
  }
  function revealEl(el) {
    if (!el) return;
    var s = scrollerEl(), r = el.getBoundingClientRect();
    if (s) {
      var m = s.getBoundingClientRect();
      if (r.bottom > m.bottom - 20) s.scrollTop += r.bottom - m.bottom + 28;
      return;
    }
    /* the floor is the pinned composer, not the window edge */
    var f = document.getElementById("ctForm");
    var floor = (f && getComputedStyle(f).position === "fixed")
      ? f.getBoundingClientRect().top : window.innerHeight;
    if (r.bottom > floor - 14) window.scrollBy(0, Math.round(r.bottom - floor + 22));
    else if (r.top < 0) window.scrollBy(0, Math.round(r.top - 14));
  }
  function toTopEl() {
    var s = scrollerEl();
    if (s) s.scrollTop = 0; else window.scrollTo(0, 0);
  }

  function replayIntro() {
    var root = document.documentElement;
    if (!root.classList.contains("intro")) return;
    root.classList.remove("go");
    void root.offsetWidth;          /* the reflow that makes it a change */
    root.classList.add("go");
  }

  /* The points picked, rendered as the tags that ride along with the message. */
  function tagsInto(host, picked) {
    if (!host) return;
    host.innerHTML = "";
    picked.forEach(function (b) {
      var t = document.createElement("span");
      t.className = "ct-tag";
      t.textContent = "@" + b.querySelector(".ct-pt-n").textContent.trim().replace(/^P/, "Point");
      host.appendChild(t);
    });
  }

  /* The screens are a chain, so advancing is one function with a table rather
     than a branch per step. Each entry says which view it moves to, where the
     message it carries is written, and where the tags go. */
  var CHAIN = {
    "2": { to: "3", said: "#ctSaidT3", tags: "#ctTags3", echo: "#wrEcho" },
    "3": { to: "4", said: "#ctSaidT4", tags: "#ctTags4", echo: "#fxEcho" }
  };

  function advanceFrom(view, said) {
    var step = CHAIN[view];
    if (!dis0 || !step) return false;
    var picked = pickedPoints();
    var names = picked.map(function (b) {
      return "@" + b.querySelector(".ct-pt-n").textContent.trim().replace(/^P/, "Point");
    });
    tagsInto($(step.tags), picked);
    if (said) {
      var t = $(step.said);
      if (t) t.textContent = said;
    }
    var m = $(step.echo);
    if (m) m.textContent = names.concat(said ? [said] : []).join(" ");
    dis0.dataset.view = step.to;
    dis0.classList.remove("chat-open");
    /* the picks have been carried onto the next screen as its tags, so the
       composer lets them go — left in the field they would ride along with
       whatever you sent next as well */
    if (window.__dgPicks) window.__dgPicks();
    toTopEl();
    var body = $("#ctBody");
    if (body) body.scrollTop = 0;
    replayIntro();
    return true;
  }

  function toNumbers(said) {
    if (!dis0 || dis0.dataset.view === "3") return;
    var picked = pickedPoints();
    tagsInto($("#ctTags3"), picked);
    if (said) {
      var t = $("#ctSaidT3");
      if (t) t.textContent = said;
      var m = $("#wrEcho");
      if (m) {
        m.textContent = picked.map(function (b) {
          return "@" + b.querySelector(".ct-pt-n").textContent.trim().replace(/^P/, "Point");
        }).concat([said]).join(" ");
      }
    }
    dis0.dataset.view = "3";
    dis0.classList.remove("chat-open");
    if (window.__dgPicks) window.__dgPicks();
    toTopEl();
    var body = $("#ctBody");
    if (body) body.scrollTop = 0;
    replayIntro();
  }

  function toRouteMap(said) {
    if (!dis0 || dis0.dataset.view === "2") return;
    var echo = $("#ctSaid");
    if (echo && said) echo.textContent = said;
    dis0.dataset.view = "2";
    /* On a phone the message was sent from inside the sheet. The answer is the
       map behind it, so the sheet steps back out of the way rather than
       leaving you to dismiss it before you can see what you asked for. */
    dis0.classList.remove("chat-open");
    if (main) main.scrollTop = 0;
    var body = $("#ctBody");
    if (body) body.scrollTop = 0;
    replayIntro();
  }

  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var said = input ? input.value.trim() : "";
      if (!said) return;
      if (input) { input.value = ""; input.style.height = ""; }
      /* Which screen the message moves you to depends on which one you sent it
         from. One handler, because there is one composer. */
      if (dis0 && CHAIN[dis0.dataset.view]) advanceFrom(dis0.dataset.view, said);
      else toRouteMap(said);
    });
  }
  /* A chip on the first screen is the same act as typing one of its lines,
     so it goes the same way. */
  $$(".v1 .ct-chip").forEach(function (c) {
    c.addEventListener("click", function () {
      if (dis0 && dis0.dataset.view === "1" && input && input.value.trim()) return;
    });
  });

  /* A chip fills the box rather than sending. Until the thread exists,
     putting the words where the person can edit them is the honest step. */
  $$(".ct-chip").forEach(function (c) {
    c.addEventListener("click", function () {
      if (!input) return;
      input.value = c.textContent.trim();
      input.focus();
      input.dispatchEvent(new Event("input"));
    });
  });

  /* ---------- walking the route ----------
     One stop is open at a time and the card shows that stop's body. The
     bodies are all in the markup; opening a stop is only a question of which
     one is not hidden, so nothing has to be built from a template and the
     content survives the script failing.

     The card itself MOVES. On a wide window it sits below the whole map; on a
     phone it belongs under the stop it describes. Two copies of it would be
     two things to keep in step, so there is one and it is re-parented — and
     because the phone lays the stops out with `order`, the card is given the
     open stop's order so it lands directly beneath it. */
  var card = $("#stopCard");
  var cardSlot = $("#cardSlot");
  var routeMap = $("#routeMap");
  var puck = $("#rmPuck");
  var narrow = window.matchMedia("(max-width:760px)");
  var openStop = "A";

  function stopEl(letter) {
    return document.querySelector('.rm-stop[data-stop="' + letter + '"]');
  }

  function placeCard() {
    if (!card || !cardSlot) return;
    var host = stopEl(openStop);
    if (narrow.matches && host) {
      /* Appended INSIDE the stop, so ordinary block flow puts it directly
         under that row and no order needs setting. */
      if (card.parentNode !== host) host.appendChild(card);
    } else {
      if (card.parentNode !== cardSlot) cardSlot.appendChild(card);
    }
  }

  /* Put the gold disc over a stop. Measured off the live boxes rather than
     computed from the grid, because the same function has to serve a row of
     seven and a column of thirteen, and measuring is the only thing that is
     true in both.

     `animate` false snaps: on load, on resize, and when the layout changes
     under it. Only a press makes it travel. */
  function movePuck(letter, animate) {
    if (!puck || !routeMap) return;
    var dot = document.querySelector('.rm-stop[data-stop="' + letter + '"] .rm-dot');
    if (!dot) return;
    var m = routeMap.getBoundingClientRect(), d = dot.getBoundingClientRect();
    /* zero width means it has not been laid out yet — wait rather than
       parking the disc in the corner */
    if (!d.width || !m.width) return;
    var x = d.left - m.left, y = d.top - m.top;

    if (animate) {
      var from = puck._at || { x: x, y: y };
      var dist = Math.sqrt(Math.pow(x - from.x, 2) + Math.pow(y - from.y, 2));
      /* 340ms to a neighbour, up to 700ms across the whole map */
      puck.style.transitionDuration = Math.min(700, 300 + dist * 0.55) + "ms";
    } else {
      puck.style.transition = "none";
    }
    puck.style.transform = "translate(" + x + "px," + y + "px)";
    puck._at = { x: x, y: y };
    if (!animate) {
      void puck.offsetWidth;            /* commit the jump before re-arming */
      puck.style.transition = "";
    }
    puck.hidden = false;
  }

  /* ---------- the chat follows the stop ----------
     The map and the conversation are two views of one walk. Pressing a stop
     used to change only the card, which left Tojo talking about the doctors
     while the map was on the bed desk. Now the answer, the note, the points
     and the questions all move with it.

     What does NOT move is the gold bubble: that is what the person said, and
     the page has no business rewriting it because they tapped somewhere. */
  var STOPCHAT = (function () {
    var tag = document.getElementById("stopChat");
    if (!tag) return null;
    try { return JSON.parse(tag.textContent); } catch (e) { return null; }
  })();

  var ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true">' +
              '<path d="M4 12h15"/><path d="M13.5 6.5L19.5 12l-6 5.5"/></svg>';

  function chatForStop(letter) {
    if (!STOPCHAT) return;
    var d = STOPCHAT[letter];
    if (!d) return;
    var msg = document.getElementById("ctMsg2"),
        note = document.getElementById("ctNote2"),
        pts = document.getElementById("ctPts2"),
        asks = document.getElementById("ctAsks2");
    if (msg) {
      msg.textContent = "";
      (d.msg || []).forEach(function (t) {
        var p = document.createElement("p"); p.textContent = t; msg.appendChild(p);
      });
    }
    if (note) note.textContent = d.note || "";
    if (pts) {
      pts.textContent = "";
      (d.pts || []).forEach(function (o, i) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "ct-pt";
        b.setAttribute("aria-pressed", "false");
        if (o[0]) b.dataset.go = o[0];
        var n = document.createElement("span");
        n.className = "ct-pt-n"; n.textContent = "P" + (i + 1);
        var t = document.createElement("span");
        t.className = "ct-pt-t"; t.textContent = o[1];
        b.appendChild(n); b.appendChild(t); pts.appendChild(b);
      });
    }
    if (asks) {
      asks.textContent = "";
      (d.asks || []).forEach(function (t) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "ct-ask";
        var s = document.createElement("span"); s.textContent = t;
        b.appendChild(s);
        b.insertAdjacentHTML("beforeend", ARROW);
        asks.appendChild(b);
      });
    }
  }

  /* swap is only true when the map itself was pressed. A point in the chat
     also opens its stop, but rewriting the point list out from under the
     press would throw away the points already picked — and picking several
     is the whole purpose of that list. */
  function openAt(letter, focus, swap) {
    if (!letter || !card) return;
    var body = card.querySelector('.rm-body[data-stop="' + letter + '"]');
    if (!body) return;
    openStop = letter;
    if (swap) chatForStop(letter);
    var no = document.getElementById("rmNo");
    if (no) no.textContent = String("ABCDEFGHIJK".indexOf(letter) + 1);
    $$(".rm-body", card).forEach(function (o) { o.hidden = (o !== body); });
    $$(".rm-stop").forEach(function (o) {
      var on = o.dataset.stop === letter;
      o.classList.toggle("is-open", on);
      var hit = o.querySelector(".rm-hit");
      if (hit) hit.setAttribute("aria-pressed", on ? "true" : "false");
    });
    placeCard();
    movePuck(letter, focus !== "snap");

    if (focus !== "snap") {
      /* The opening sequence's animation is taken off the card the first time
         a stop is opened by hand, if it has not come off already. Leaving it
         on means the next re-parent replays it from its delay. */
      card.classList.remove("rm-intro");

      /* Restart the arrival animation. Removing the class, reading a layout
         property and adding it back is what makes that a change the browser
         acts on — without the read it coalesces into nothing. */
      card.classList.remove("is-fresh");
      void card.offsetWidth;
      card.classList.add("is-fresh");
    }
    /* Scrolling is the phone's business: on a wide window the card never
       moves, so there is nothing to go and look at. */
    if (focus && focus !== "snap") bringIntoView(stopEl(letter));
  }

  /* Move only if the stop is not already comfortably in view, and move at
     once when it is needed. A smooth scroll here read as the content being
     slow to arrive, when the content was in fact already there. */
  function bringIntoView(host) {
    if (!host || !main) return;
    var h = host.getBoundingClientRect(), m = main.getBoundingClientRect();
    var above = h.top < m.top + 72;
    var below = h.bottom > m.bottom - 140;
    if (!above && !below) return;
    var to = main.scrollTop + (h.top - m.top) - 88;
    if (main.scrollTo) main.scrollTo({ top: Math.max(0, to), behavior: "auto" });
    else main.scrollTop = Math.max(0, to);
  }

  $$(".rm-hit").forEach(function (b) {
    b.addEventListener("click", function () {
      openAt(b.dataset.go, narrow.matches, true);
    });
  });

  /* The card changes home when the window crosses the breakpoint, not only
     when a stop is pressed — otherwise it is left orphaned in the layout it
     was put there for. */
  function relayout() { placeCard(); movePuck(openStop, false); }
  if (narrow.addEventListener) narrow.addEventListener("change", relayout);
  else if (narrow.addListener) narrow.addListener(relayout);
  window.addEventListener("resize", relayout, { passive: true });
  /* The map arrives animated, so its boxes are the wrong size until the
     opening has finished with them. Watching the map's own box catches that
     without having to know the sequence's timings here. */
  if (window.ResizeObserver && routeMap) {
    new ResizeObserver(function () { movePuck(openStop, false); }).observe(routeMap);
  }
  /* The stops arrive scaled up from nothing, so their boxes are the wrong
     size for most of a second and the disc placed against them lands short.
     The map's own box does not change while that happens, so the observer
     above never sees it — this does, because every stop's reveal ends with
     an animationend that bubbles to the map. */
  if (routeMap) {
    routeMap.addEventListener("animationend", function () {
      movePuck(openStop, false);
    });
  }
  /* and once the opening has finished with the card, it lets go of it */
  if (card) {
    card.addEventListener("animationend", function (e) {
      if (e.animationName === "dis-zoom") card.classList.remove("rm-intro");
      if (e.animationName === "rm-open") card.classList.remove("is-fresh");
    });
  }
  placeCard();
  chatForStop(openStop);   /* the chat opens on the stop the map opens on */
  movePuck(openStop, false);

  /* ---------- the points in the conversation ----------
     These are a selection, not navigation: you can name more than one place a
     delay lives, and more than one is usually the truth. What is picked is
     carried into the message you send, which is why the next screen opens
     with those points named in it.

     A point that also names a stop opens that stop as well, so the map keeps
     up with what you are talking about — but picking is the main act, and
     un-picking has to be possible, so the press toggles. */
  function pickedPoints() {
    return $$(".ct-pt").filter(function (o) {
      return o.getAttribute("aria-pressed") === "true" &&
             o.offsetParent !== null;               /* only the visible screen's */
    });
  }
  $$(".ct-pt").forEach(function (b) { b.setAttribute("aria-pressed", "false"); });

  /* The points picked show as chips in the composer, so what you are about
     to send is visible in the place you send it from. Drawn FROM the pressed
     buttons rather than kept in a list beside them: one source, and the two
     cannot come to disagree.

     pickedPoints() already filters to the screen you are on — the walk has
     four of them and each keeps its own points — so the chips follow you
     along the chain without being told to. */
  var pickBox = $("#ctPicks");
  function drawPicks() {
    if (!pickBox) return;
    var on = pickedPoints();
    pickBox.textContent = "";
    pickBox.hidden = !on.length;
    on.forEach(function (b) {
      var n = b.querySelector(".ct-pt-n"), t = b.querySelector(".ct-pt-t");
      var code = n ? n.textContent.trim() : "";
      var chip = document.createElement("span");
      chip.className = "ct-pick";
      chip.title = t ? t.textContent.trim() : code;
      var lab = document.createElement("b");
      lab.textContent = code;
      var x = document.createElement("button");
      x.type = "button";
      x.className = "ct-pick-x";
      x.setAttribute("aria-label", "Remove " + (t ? t.textContent.trim() : code));
      x.innerHTML = '<svg viewBox="0 0 10 10" aria-hidden="true">' +
                    '<path d="M1.5 1.5l7 7M8.5 1.5l-7 7"/></svg>';
      /* taking the chip off un-presses the point it came from, and the chips
         are then redrawn from that — never edited in place */
      x.addEventListener("click", function () {
        b.setAttribute("aria-pressed", "false");
        drawPicks();
        if (input) input.focus();
      });
      chip.appendChild(lab); chip.appendChild(x);
      pickBox.appendChild(chip);
    });
    if (window.__dgFoot) window.__dgFoot();
  }
  window.__dgPicks = drawPicks;
  /* Delegated, because the first screen's points are rewritten whenever the
     walk moves to another stop. Bound one by one, the handlers would go out
     with the buttons they were bound to and the new ones would be dead. */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".ct-pt");
    if (!b) return;
    var on = b.getAttribute("aria-pressed") === "true";
    b.setAttribute("aria-pressed", on ? "false" : "true");
    drawPicks();
    if (!on && b.dataset.go) openAt(b.dataset.go, false);
  });
  /* An "ask next" is a question already written out, so pressing it asks it
     — the same act as typing those words and sending them. On the first
     screen there is nowhere yet to advance to, so there it fills the box
     instead and waits for you. */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".ct-ask");
    if (!b) return;
    var said = b.querySelector("span").textContent.trim();
    if (dis0 && CHAIN[dis0.dataset.view]) {
      if (input) { input.value = ""; input.style.height = ""; }
      advanceFrom(dis0.dataset.view, said);
      return;
    }
    if (!input) return;
    input.value = said;
    input.focus();
    input.dispatchEvent(new Event("input"));
  });

  /* ---------- the parts of the fix ----------
     Ordinary disclosures. hidden carries the state so the content is really
     gone from the page rather than merely invisible, and aria-expanded on the
     button says so — the chevron is the decoration, not the signal. */
  $$(".fx-open").forEach(function (b) {
    b.addEventListener("click", function () {
      var body = b.parentNode.querySelector(".fx-body");
      if (!body) return;
      var open = b.getAttribute("aria-expanded") === "true";
      b.setAttribute("aria-expanded", open ? "false" : "true");
      body.hidden = open;
    });
  });

  /* ---------- the rail ----------
     Marks the section you are looking at. offsetTop against the scroller
     rather than getBoundingClientRect, so a transform on a card later
     cannot move the reading.

     Two wrinkles the obvious version gets wrong. Cards 01 and 02 sit in the
     same grid row and therefore share an offsetTop, so "the last one at or
     above the line" always picked the right-hand card and Resources could
     never light; ties go to the first in document order instead. */
  /* ---------- the diagnosis dial ----------
     A reading, not a picture. One JSON block says how many stages there
     are and where each one stands, and everything on the glass — the ring,
     the count, the finding, the list underneath — is drawn from it. Swap
     the block for a real feed and nothing here changes.

     The ring is the same circle five times over rather than five arc paths.
     An arc path means writing out sines and cosines for every endpoint, and
     every one of those numbers is wrong the moment the stage count changes;
     a dash pattern is arithmetic the browser does, so the only thing that
     has to be right is the circumference. It also gives the drawing for
     free: growing a dash from nothing IS the segment sweeping round.

     Chart.js was the obvious reach and the wrong one. The glass is one
     shape — ring, handle and lens in a single coordinate space — and a
     charting library would have had to sit underneath it as a second ring
     kept in step by hand, for 200KB and a network dependency, to draw
     five arcs this file draws in forty lines. */
  var DIAL = (function () {
    var R = 223, C = 2 * Math.PI * R, GAP = 23.25;
    var svgNS = "http://www.w3.org/2000/svg";
    var slow = window.matchMedia &&
               window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function read() {
      var live = window.VIREVO_DIAGNOSIS;          /* a real feed, if one is set */
      if (live && live.stages) return live;
      var tag = document.getElementById("dxData");
      if (!tag) return null;
      try { return JSON.parse(tag.textContent); }
      catch (e) { return null; }                   /* bad data shows the empty dial */
    }

    function arc(i, n, cls) {
      var c = document.createElementNS(svgNS, "circle");
      c.setAttribute("cx", 303); c.setAttribute("cy", 417); c.setAttribute("r", R);
      c.setAttribute("class", cls);
      c.style.strokeDasharray = (C / n - GAP) + " " + C;
      c.style.strokeDashoffset = -(C / n) * i;
      return c;
    }

    /* A redraw cancels the one before it. Without this, a second opening
       starts its own beats while the first is still writing numbers into the
       same element, and the two disagree. */
    var timers = [];
    function draw(animate) {
      var dial = document.getElementById("dxDial");
      var data = read();
      if (!dial || !data) return;
      timers.forEach(clearTimeout); timers = [];

      var stages = data.stages || [];
      var n = stages.length || 5;
      var track = document.getElementById("dxTrack");
      var arcs  = document.getElementById("dxArcs");
      var list  = document.getElementById("dxStages");
      var findEl = document.getElementById("dxFind");
      var nEl = document.getElementById("dxN"), tEl = document.getElementById("dxT");
      var done = stages.filter(function (s) { return s.state === "done"; }).length;

      track.textContent = ""; arcs.textContent = ""; list.textContent = "";
      for (var i = 0; i < n; i++) track.appendChild(arc(i, n, "dx-arc is-track"));

      /* The ring is a progress bar bent into a circle: an arc is drawn only
         for a stage that is finished, and the last of those is gold. So the
         gold arc is the frontier — how far the walk has got — and everything
         past it is the empty track still to be filled.

         The list and the ring are two readings of one thing, so they are
         built in the same pass and cannot fall out of step. */
      var lastDone = -1;
      stages.forEach(function (s, i) { if (s.state === "done") lastDone = i; });

      var lit = [];
      stages.forEach(function (s, i) {
        var a = null;
        var li = document.createElement("li");
        li.className = "dx-stage" + (s.state === "done" ? " is-done"
                                   : s.state === "now" ? " is-now" : "");
        li.innerHTML = '<span class="dx-n">' + (i + 1) + "</span>";
        li.appendChild(document.createTextNode(s.label || ""));
        list.appendChild(li);
        /* Every stage gets its arc once the walk has started, so the ring
           reads as a whole instrument rather than one with a piece missing.
           The count is carried by where the gold sits, not by how many arcs
           are coloured: gold is the last stage finished, so three dark
           behind it and itself is four done. The bare track shows only
           before anything has been finished at all. */
        if (lastDone > -1) {
          var a = arc(i, n, "dx-arc" + (i === lastDone ? " is-now" : ""));
          arcs.appendChild(a);
        }
        if (s.state !== "done" && s.state !== "now") return;
        lit.push({ el: (lastDone > -1 ? a : null), li: li,
                   counts: s.state === "done" });
      });

      if (tEl) tEl.textContent = n;
      if (findEl) findEl.textContent = done ? (data.finding || "") : (data.empty || "");
      if (findEl) findEl.classList.toggle("is-empty", !done);

      var seg = C / n - GAP;
      if (!animate || slow || !lit.length) {
        lit.forEach(function (o) {
          if (o.el) o.el.style.strokeDasharray = seg + " " + C;
          o.li.classList.add("is-lit");
        });
        if (nEl) nEl.textContent = done;
        return;
      }

      /* Starts at nothing and fills to what is actually known — so the
         number you watch climb is the number, not a flourish over it.

         The final value is written by its own beat from the data, not by
         whichever tick happened to run last. Read off the loop it depended
         on how the stages were ordered, so a walk whose last stage was the
         one in progress settled one short of the truth. */
      if (nEl) nEl.textContent = "0";
      var ticked = 0;
      lit.forEach(function (o, k) {
        if (o.el) o.el.style.strokeDasharray = "0 " + C;
        var delay = 780 + k * 190;
        timers.push(setTimeout(function () {
          if (o.el) o.el.animate(
            [{ strokeDasharray: "0 " + C }, { strokeDasharray: seg + " " + C }],
            { duration: 520, easing: "cubic-bezier(.32,.72,.3,1)", fill: "forwards" }
          );
          o.li.classList.add("is-lit");
          if (nEl && o.counts && ticked < done) nEl.textContent = String(++ticked);
        }, delay));
      });
      timers.push(setTimeout(function () {
        if (nEl) nEl.textContent = String(done);
      }, 780 + lit.length * 190 + 520));
    }

    return { draw: draw };
  })();
  /* So a page or a later script can push new numbers in without knowing
     anything about how the ring is drawn. */
  window.VirevoDiagnosis = { refresh: function () { DIAL.draw(true); } };
  DIAL.draw(false);      /* built once at load, so it is never empty markup */

  var dxGo = document.querySelector(".dx-refresh");
  if (dxGo) dxGo.addEventListener("click", function () { DIAL.draw(true); });

  /* ---------- the automations dial ----------
     A gauge, and the gauge is the point: the window runs from one clock time
     to another along half a circle, the night is the part of it already
     spent, and every automation is a time on that scale. Give it different
     times and it redraws — nothing here holds a coordinate.

     Chart.js was the obvious reach and the wrong one again. A gauge it can
     do; a gauge with six labelled pins parked off the arc, each on a leader
     back to its own minute, and the whole thing one drawing that scales with
     the column, it cannot — that would be a Chart.js ring with an SVG laid
     over it, kept in step by hand, for 200KB and a network dependency. */
  var AUDIAL = (function () {
    var NS = "http://www.w3.org/2000/svg";
    var CX = 262, CY = 252, R = 200, PIN = 17;
    var slow = window.matchMedia &&
               window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function mins(t) {
      var m = /^(\d{1,2}):(\d{2})$/.exec(String(t || ""));
      return m ? (+m[1] * 60 + +m[2]) : null;
    }
    function label(m) {
      var h = Math.floor(m / 60) % 24, ap = h < 12 ? "AM" : "PM";
      var h12 = h % 12; if (!h12) h12 = 12;
      return h12 + " " + ap;
    }
    function at(a, r) {
      var t = a * Math.PI / 180;
      return [CX + r * Math.cos(t), CY - r * Math.sin(t)];
    }
    function el(name, attrs) {
      var n = document.createElementNS(NS, name);
      for (var k in attrs) n.setAttribute(k, attrs[k]);
      return n;
    }
    function arcPath(a0, a1, r) {
      var p0 = at(a0, r), p1 = at(a1, r);
      return "M" + p0[0].toFixed(1) + " " + p0[1].toFixed(1) +
             " A" + r + " " + r + " 0 " + (Math.abs(a0 - a1) > 180 ? 1 : 0) +
             " 1 " + p1[0].toFixed(1) + " " + p1[1].toFixed(1);
    }

    function draw() {
      var host = document.getElementById("auDial");
      var tag = document.getElementById("autData");
      if (!host || !tag) return;
      var d; try { d = JSON.parse(tag.textContent); } catch (e) { return; }

      var from = mins(d.from), to = mins(d.to);
      if (from === null || to === null) return;
      var span = (to - from + 1440) % 1440 || 1440;   /* minutes across the dial */
      var deg = function (m) {                        /* a clock time to an angle */
        var into = (m - from + 1440) % 1440;
        return 180 - (into / span) * 180;
      };

      var arcs = document.getElementById("auArcs");
      var marks = document.getElementById("auMarks");
      var pins = document.getElementById("auPins");
      arcs.textContent = ""; marks.textContent = ""; pins.textContent = "";

      /* the two spans */
      var night = mins(d.nightEnds);
      var split = (night === null) ? 180 : deg(night);
      arcs.appendChild(el("path", { "class": "au-arc is-night", d: arcPath(180, split, R) }));
      arcs.appendChild(el("path", { "class": "au-arc is-day",   d: arcPath(split, 0, R) }));

      /* the hours, every everyHours from the start, plus both ends */
      var step = (d.everyHours || 4) * 60;
      for (var m = 0; m <= span; m += step) {
        var a = deg(from + m);
        var p0 = at(a, R - 9), p1 = at(a, R + 9);
        marks.appendChild(el("path", { "class": "au-tick",
          d: "M" + p0[0].toFixed(1) + " " + p0[1].toFixed(1) +
             "L" + p1[0].toFixed(1) + " " + p1[1].toFixed(1) }));
        var lp = at(a, R + 30);
        var anchor = a > 105 ? "end" : (a < 75 ? "start" : "middle");
        var dy = (a >= 175 || a <= 5) ? 5 : (a > 125 || a < 55 ? 0 : -2);
        var t = el("text", { "class": "au-hr", x: lp[0].toFixed(1),
                             y: (lp[1] + dy).toFixed(1), "text-anchor": anchor });
        t.textContent = label((from + m) % 1440);
        marks.appendChild(t);
      }

      /* Pins sit at their own time. Two automations at the same hour would
         land on top of each other, so a pin that clashes with one already
         placed steps inwards until it is clear — which is what stacks the
         evening cluster without any of it being positioned by hand. */
      var placed = [];
      (d.items || []).forEach(function (it, i) {
        var a0 = deg(mins(it.at)), r0 = R * 0.79, st = PIN * 1.15;
        /* Where a pin would like to sit, then the places it will settle for,
           nearest first. Stepping straight in alone would leave two pins on
           one ray and the inner one's leader would run under the outer pin;
           swinging alone would walk a pin off its hour. The list does a
           little of each and stops at nine degrees — an hour on this dial —
           so a pin never strays far enough to misreport its time. */
        /* Nine degrees is an hour on this dial and the swing stops there
           while it can. A real crowd — several automations booked to the
           same minute — cannot all sit near their hour and still be read,
           so past that the fan widens rather than letting pins stack. */
        var SWING = [0, 5, -5, 9, -9, 14, -14, 20, -20, 27, -27], STEPS = 6;
        var free = function (c) {
          return !placed.some(function (q) {
            return Math.hypot(c[0] - q[0], c[1] - q[1]) < PIN * 2 + 7;
          });
        };
        var a = a0, r = r0, xy = at(a0, r0), settled = false;
        /* Nearest slot first: a step inwards is cheaper than a swing, and no
           swing goes past nine degrees — an hour on this dial — so a pin
           cannot drift far enough to misreport its time. */
        for (var step = 0; step < STEPS && !settled; step++) {
          for (var w = 0; w < SWING.length && !settled; w++) {
            var ca = a0 + SWING[w], cr = r0 - step * st, c = at(ca, cr);
            if (free(c)) { a = ca; r = cr; xy = c; settled = true; }
          }
        }
        /* Nothing clear in the fan: go straight in until it is. Two pins on
           one ray reads worse than two pins on top of each other does not. */
        if (!settled) {
          r = r0;
          do { r -= st * 0.6; xy = at(a0, r); } while (!free(xy) && r > PIN * 1.2);
          a = a0;
        }
        placed.push(xy);

        var idea = it.state === "idea";
        var lead0 = at(a, r + PIN + 1), lead1 = at(a, R - 9);
        var ln = el("path", { "class": "au-lead" + (idea ? " is-idea" : ""),
          d: "M" + lead0[0].toFixed(1) + " " + lead0[1].toFixed(1) +
             "L" + lead1[0].toFixed(1) + " " + lead1[1].toFixed(1) });
        ln.style.setProperty("--n", i);
        arcs.appendChild(ln);

        var g = el("g", { "class": "au-pin" + (idea ? " is-idea" : "") });
        g.style.setProperty("--n", i);
        g.appendChild(el("circle", { cx: xy[0].toFixed(1), cy: xy[1].toFixed(1), r: PIN }));
        var tx = el("text", { x: xy[0].toFixed(1), y: (xy[1] + 6).toFixed(1) });
        tx.textContent = String(i + 1);
        g.appendChild(tx);
        pins.appendChild(g);
      });

      /* the sweep has to know how long the arc it is drawing actually is */
      var nightLen = Math.PI * R * ((180 - split) / 180);
      var dayLen = Math.PI * R * (split / 180);
      arcs.querySelector(".is-night").style.setProperty("--len", Math.ceil(nightLen + 4));
      arcs.querySelector(".is-day").style.setProperty("--len", Math.ceil(dayLen + 4));
      if (slow) host.classList.add("no-sweep");
    }

    return { draw: draw };
  })();
  window.VirevoAutomations = { refresh: function () { AUDIAL.draw(); } };
  AUDIAL.draw();

  var main = $("#disMain");
  /* The rail and the dock are the same navigation in two shapes, so they
     share the spy and the jump rather than each having their own. A section
     has a tab AND an icon, so the spy sets aria-current on both. That is
     right — they are never on screen together. */
  /* The dock is no longer part of this: on a phone those five icons are the
     other tools, real links to other pages, so the spy must not mark them
     and the jump handler must not swallow their clicks. */
  var tabs = $$(".rail-tab");

  if (main && tabs.length) {
    var targets = tabs.map(function (t) {
      var id = t.getAttribute("href").slice(1);
      var el = document.getElementById(id);
      return (el && main.contains(el)) ? { tab: t, el: el } : null;
    }).filter(Boolean);

    var spy = function () {
      var y = main.scrollTop + main.clientHeight * 0.3, best = null;
      targets.forEach(function (o) {
        var top = o.el.offsetTop;
        if (top <= y && (!best || top > best.el.offsetTop)) best = o;
      });
      tabs.forEach(function (t) { t.removeAttribute("aria-current"); });
      if (best) best.tab.setAttribute("aria-current", "true");
    };
    main.addEventListener("scroll", spy, { passive: true });
    spy();

    /* The rail's links point into a scrolling div, not the document, so the
       browser's own anchor jump would scroll the page — which does not
       scroll — and appear to do nothing. */
    /* Diagnosis is not a place on the worksheet, it is a different sheet.
       Its tab swaps the middle column for the landing and leaves data-view
       — and so the whole conversation — exactly where it was. Every other
       tab puts the worksheet back before it scrolls, because scrolling to
       a section still hidden behind the landing would look like a dead
       click. */
    var dis = $("#dis");
    /* The rail's desks, each a panel that replaces the middle column and
       leaves the conversation where it was. One table rather than a branch
       per tab, so adding the next desk is a line here and a wrap there. */
    var DESKS = {
      "#diagnosis": { panel: "dx",  wrap: "#dxWrap",  after: function () { DIAL.draw(true); } },
      "#solutions":   { panel: "sol", wrap: "#solWrap" },
      "#automations": { panel: "aut", wrap: "#autWrap",
                        after: function () { AUDIAL.draw(); } },
      "#processes":   { panel: "prc", wrap: "#prcWrap" }
    };

    function showDesk(panel) {
      if (!dis) return;
      if (panel) dis.setAttribute("data-panel", panel);
      else dis.removeAttribute("data-panel");
      toTopEl();
    }

    /* The rail and the phone's strip are the same navigation drawn twice, so
       they are marked together. Marking only the rail left the strip saying
       nothing on the one layout where it is the only navigation there is. */
    var strip = $$(".dock-i[href^='#']"), stripBack = $(".dock-back");

    /* The bar's address line. Only the last span is written; the tool's name
       in front of it and the wide-window wording are the stylesheet's. */
    var barW = document.getElementById("barW");
    var WORD = {
      "#diagnosis": "Diagnosis", "#solutions": "Solutions",
      "#automations": "Automations", "#processes": "Processes"
    };
    function sayWhere(key) {
      if (barW) barW.textContent = (key && WORD[key]) || "with Tojo";
    }
    function markStrip(key) {
      strip.forEach(function (i) {
        if (key && i.getAttribute("href") === key) i.setAttribute("aria-current", "page");
        else i.removeAttribute("aria-current");
      });
      /* with no desk open the way back is where you are, and it says so */
      if (stripBack) {
        if (key) stripBack.removeAttribute("aria-current");
        else stripBack.setAttribute("aria-current", "page");
      }
    }
    markStrip(null);

    /* The strip opens the same desks the rail does. A section with no desk
       behind it yet is stopped here as well: left alone the browser would go
       looking for #resources and scroll the page for no visible reason. */
    strip.forEach(function (i) {
      var key = i.getAttribute("href") || "";
      i.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        var desk = DESKS[key];
        if (!desk) return;                       /* not built yet */
        tabs.forEach(function (x) { x.removeAttribute("aria-current"); });
        var rail = tabs.filter(function (x) { return x.getAttribute("href") === key; })[0];
        if (rail) rail.setAttribute("aria-current", "true");
        markStrip(key);
        sayWhere(key);
        showDesk(desk.panel);
        var wrap = $(desk.wrap);
        if (wrap) {
          wrap.classList.remove("is-fresh");
          void wrap.offsetWidth;
          wrap.classList.add("is-fresh");
        }
        if (desk.after) desk.after();
      }, true);
    });

    /* The way back out of a desk. On the landing it is an ordinary link to
       the page; standing at a desk it only has to put the middle column
       back, which keeps the conversation where it was. */
    if (stripBack) stripBack.addEventListener("click", function (e) {
      if (!dis || !dis.hasAttribute("data-panel")) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      tabs.forEach(function (x) { x.removeAttribute("aria-current"); });
      markStrip(null);
      sayWhere(null);
      showDesk(null);
    }, true);

    tabs.forEach(function (t) {
      var desk = DESKS[t.getAttribute("href") || ""];
      if (!desk) return;
      t.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
        e.preventDefault();
        e.stopImmediatePropagation();
        tabs.forEach(function (x) { x.removeAttribute("aria-current"); });
        t.setAttribute("aria-current", "true");
        markStrip(t.getAttribute("href"));
        sayWhere(t.getAttribute("href"));
        showDesk(desk.panel);
        var wrap = $(desk.wrap);
        if (wrap) {
          wrap.classList.remove("is-fresh");
          void wrap.offsetWidth;      /* the reflow that makes it a change */
          wrap.classList.add("is-fresh");
        }
        if (desk.after) desk.after();
      }, true);
    });

    targets.forEach(function (o) {
      if (DESKS[o.tab.getAttribute("href") || ""]) return;
      o.tab.addEventListener("click", function (e) {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
        e.preventDefault();
        markStrip(null);
        sayWhere(null);
        showDesk(null);
        main.scrollTo({ top: Math.max(0, o.el.offsetTop - 24), behavior: "smooth" });
      });
    });

    /* While the landing is up the spy has nothing to follow, so it must not
       quietly move the mark off Diagnosis on the scroll it causes itself. */
    var baseSpy = spy;
    spy = function () { if (!dis || !dis.hasAttribute("data-panel")) baseSpy(); };
    main.removeEventListener("scroll", baseSpy, { passive: true });
    main.addEventListener("scroll", spy, { passive: true });
  }

  /* ---------- the opening sequence ----------
     The choreography is all in discharge.css; there are only two things
     it cannot do for itself.

     First, a dash animation needs the path's real length, and that is a
     measurement, not a constant — a hand-written number is right exactly
     once and silently wrong after any edit to the arrow. getTotalLength
     is asked at load and written back as a custom property.

     Second, the clock should not start until the fonts have landed. The
     title is Bebas Neue and the note is Caveat; if either swaps in mid
     flight the words change width while they are moving and the impact
     lands in the wrong place. document.fonts.ready waits for that, with
     a cap so a font server having a bad day delays the page by 600ms
     rather than indefinitely. */
  (function intro() {
    var root = document.documentElement;
    if (!root.classList.contains("intro")) return;

    $$(".dis-note svg path, .rm-turn path").forEach(function (path) {
      try {
        path.style.setProperty("--len", Math.ceil(path.getTotalLength()) + "");
      } catch (e) { /* no layout for it yet; the CSS fallback length stands */ }
    });

    var started = false;
    var start = function () {
      if (started) return;
      started = true;
      root.classList.add("go");
    };

    setTimeout(start, 600);
    if (document.fonts && document.fonts.ready && document.fonts.ready.then) {
      document.fonts.ready.then(start, start);
    } else {
      start();
    }
  })();

  /* ---------- the panel, on narrow windows ---------- */
  var dis = $("#dis"), fab = $("#disFab");

  if (dis && fab) {
    fab.addEventListener("click", function () { dis.classList.toggle("chat-open"); });
  }

  /* ---------- the conversation, as a screen ----------
     On a phone the panel is a sheet, and the strip at the foot is a button
     that raises it. The caret is moved into the real composer afterwards,
     because pressing something that looks like a text field and not being
     able to type is the one thing that would make it feel broken.

     The focus is deferred past the transition: focusing an input mid-slide
     makes the keyboard open against a moving element, which on iOS leaves
     the sheet scrolled into a corner it cannot get out of. */
  var dockOpen = $("#dockOpen"), ctBack = $("#ctBack");
  function openChat(focus) {
    if (!dis) return;
    dis.classList.add("chat-open");
    if (focus && input) setTimeout(function () { input.focus(); }, 380);
  }
  function closeChat() {
    if (!dis) return;
    dis.classList.remove("chat-open");
    if (input) input.blur();
    if (dockOpen) dockOpen.focus();
  }
  if (dockOpen) dockOpen.addEventListener("click", function () { openChat(true); });
  if (ctBack)   ctBack.addEventListener("click", closeChat);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeChat();
  });
  /* Pressing a section from inside the conversation should show you that
     section, not leave you reading the sheet you just navigated away from. */
  $$(".dock-i").forEach(function (i) {
    i.addEventListener("click", function () { if (dis) dis.classList.remove("chat-open"); });
  });
})();
