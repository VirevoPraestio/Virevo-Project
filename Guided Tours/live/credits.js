/* ============================================================
   CREDITS — one balance, four pages
   ------------------------------------------------------------
   Chat and Automation ALREADY wear this pill: .top-cr in their
   top bar, styled by chat.css, mobile size and all. So this file
   does not build a second one there — it drives the one that is
   already there. Discharge and Bed Management have no top bar of
   that kind, so for those two it builds the pill, in the two
   places each of them has room for it.

   That split is deliberate. A counter added beside an existing
   counter is two balances to keep in step, and the first time
   they disagree the page is lying about money.

   There is no auth backend yet. Signing in is login.js writing
   virevo:email into sessionStorage and sending you to /chat, so
   that key is what "signed in" means here and the counter shows
   only when it is there.

   Everything to do with the balance lives in this one file, so
   when a real meter arrives there is a single place to change:
   read() and write() are the seam. Swap their bodies for a fetch
   and no page has to know.

   sessionStorage rather than localStorage on purpose — the
   balance belongs to the signed-in session and should go when
   the session does, the way the email does.
   ============================================================ */
(function () {
  "use strict";

  var KEY     = "virevo:credits";
  var WHO     = "virevo:email";
  var START   = 24600;   /* what a session opens with, until a meter says otherwise */
  var PER_MSG = 50;      /* charged per message sent to Tojo */
  var UPGRADE = "/healthcare#pricing";

  /* ---------- the seam ---------- */
  /* try/catch on every storage touch: Safari's private mode throws rather
     than no-opping, and a credit balance is not worth taking a page down
     for. A session that cannot store simply starts fresh on each load. */
  var memory = null;

  function signedIn() {
    try { return !!sessionStorage.getItem(WHO); } catch (e) { return false; }
  }
  function read() {
    if (memory !== null) return memory;
    var v;
    try { v = sessionStorage.getItem(KEY); } catch (e) { v = null; }
    if (v === null || v === "" || isNaN(+v)) return write(START);
    return (memory = Math.max(0, Math.floor(+v)));
  }
  function write(n) {
    n = Math.max(0, Math.floor(n));
    memory = n;
    try { sessionStorage.setItem(KEY, String(n)); } catch (e) {}
    return n;
  }

  /* ---------- the pill, for the two pages that have none ---------- */
  var SPARK =
    '<svg class="cr-ic" viewBox="0 0 24 24" aria-hidden="true">' +
      '<path d="M12 3l3.2 5.6L21 12l-5.8 3.4L12 21l-3.2-5.6L3 12l5.8-3.4z"/>' +
    '</svg>';
  /* A chevron, not the word, at the smallest size: at 10px "Upgrade" is
     either unreadable or wider than the control beside it. */
  var CHEV =
    '<svg class="cr-u-ic" viewBox="0 0 24 24" aria-hidden="true">' +
      '<path d="M12 4.6l6 7h-3.6v7.8H9.6V11.6H6z"/>' +
    '</svg>';

  function pill(size) {
    var el = document.createElement("div");
    el.className = "cr" + (size ? " cr-" + size : "");
    /* The figure changes under the reader's feet, so it is announced —
       politely, after whatever they were being told rather than instead. */
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
    el.hidden = true;
    el.innerHTML =
      SPARK +
      '<span class="cr-n"><b class="cr-n-v"></b><span class="cr-n-w"> credits</span></span>' +
      '<a class="cr-u" href="' + UPGRADE + '">' +
        CHEV + '<span class="cr-u-t">Upgrade</span>' +
      "</a>";
    return el;
  }

  /* Every place a figure has to be kept current, whoever built it. Each
     entry is {el, set(txt)} so the one that chat.css owns and the ones
     built here can be written the same way. */
  var faces = [];

  function paint() {
    var txt = read().toLocaleString("en-IN");
    for (var i = 0; i < faces.length; i++) faces[i](txt);
  }

  /* ---------- spending ---------- */
  /* Guarded against being charged twice for one message. A composer's own
     handler and this one both run on the same submit, and on Discharge an
     "ask next" can send with no submit at all — so rather than reason about
     which paths can overlap, two charges inside the same beat are treated
     as the one message they came from. */
  var last = 0;
  function spend(n) {
    var t = Date.now();
    if (t - last < 400) return;
    last = t;
    write(read() - (n || PER_MSG));
    paint();
  }

  /* ---------- what counts as a message ---------- */
  /* CAPTURE, not bubble. All four pages clear the composer inside their own
     submit handler, so a bubble-phase listener would find an empty field
     and no way to tell a real message from a stray submit. Capture runs
     first, while the field still holds what is about to go.

     The condition mirrors what those handlers themselves do — they return
     early on an empty field unless a point is pressed, and so does this. A
     charge for a message the page declined to send would be the worst kind
     of bug here: money for nothing, and invisible. */
  function composerOf(form) {
    return form.querySelector(".ct-in, .comp-in, textarea, input[type='text']");
  }
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || form.nodeName !== "FORM") return;
    var box = composerOf(form);
    if (!box) return;
    var typed = (box.value || "").trim();
    var picked = document.querySelectorAll('.ct-pt[aria-pressed="true"]').length;
    if (!typed && !picked) return;
    spend();
  }, true);

  /* Discharge's "ask next" sends the question straight off, with no submit
     to catch — but on its first screen the same button only drops the words
     into the composer for you to edit, and Bed Management's always does.

     Rather than encode which screens send and which fill, the click is
     judged by what it did: if the composer is now holding the ask's own
     words, it was filled, not sent. One rule, and it stays true if either
     page ever changes its mind about a screen. */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".ct-ask");
    if (!b) return;
    var span = b.querySelector("span");
    var words = (span ? span.textContent : b.textContent).trim();
    var form = document.querySelector("#ctForm, .ct-foot, form");
    var box  = form && composerOf(form);
    setTimeout(function () {
      if (box && (box.value || "").trim() === words) return;   /* filled, not sent */
      spend();
    }, 0);
  });

  /* ---------- putting it on the page ---------- */
  function mount() {
    if (!signedIn()) {
      /* A counter is part of being signed in, so signed out it is not shown
         at all — including the one already in Chat's markup, which until now
         showed a hard-coded balance to anyone who opened the page.

         The stored balance goes with it. sessionStorage outlives a log-out
         within the same tab, so without this a second sign-in would resume
         the first one's spending as though it had never ended. */
      var had = document.querySelector(".top-cr");
      if (had) had.hidden = true;
      try { sessionStorage.removeItem(KEY); } catch (e) {}
      memory = null;
      return;
    }
    var mine = document.querySelector(".top-cr");
    if (mine) mine.hidden = false;

    /* 1 · Chat and Automation: the pill is already in the markup. Only the
       figure is taken over — the word "credits" beside it is a separate
       span the stylesheet drops at narrow widths, so the number is written
       into its own node rather than over the pair of them. */
    var own = document.querySelector(".top-cr .top-cr-n");
    if (own) {
      var w = own.querySelector(".top-cr-w");
      var v = document.createElement("b");
      v.className = "top-cr-v";
      v.style.fontWeight = "inherit";
      own.textContent = "";
      own.appendChild(v);
      if (w) own.appendChild(w);
      faces.push(function (t) { v.textContent = t; });

      /* The Upgrade button beside it did nothing at all. It goes where the
         pricing is, which is the question the number raises. */
      var up = document.querySelector(".top-cr .top-up");
      if (up) up.addEventListener("click", function () { location.href = UPGRADE; });
    }

    /* 2 · Discharge and Bed Management, wide: the chat panel header, beside
       Expand. That band already holds an avatar, two lines of type and a
       button, so the pill comes down to fit rather than making it taller. */
    var exp = document.querySelector(".ct-head .ct-exp");
    if (exp && exp.parentNode) {
      var sm = pill("sm");
      exp.parentNode.insertBefore(sm, exp);
      faces.push(mk(sm));
    }

    /* 3 · Discharge and Bed Management, phone: the top bar, before Tour.
       BOTH bars, not one. Discharge shows .dis-top.v1 on its landing and
       .dis-top.bar-2 once you are inside a section; a counter mounted to
       whichever happened to be up at load would vanish the moment you moved.

       Tour is moved INTO the wrapper rather than the pill dropped beside
       it: bar-2 is a grid of named areas and Tour owns the one on the
       right, so the pair travel together in that cell instead of the area
       map having to grow a column it only wants on a phone. */
    var tours = document.querySelectorAll(".dis-top .dis-tour");
    for (var i = 0; i < tours.length; i++) {
      var tour = tours[i];
      if (!tour.parentNode) continue;
      var xs = pill("xs");
      /* Only the grid bar needs the wrapper. On the landing bar Tour is
         simply the last item in a row, so the pill goes in front of it as a
         sibling — wrapping there would add a box that has to be taught the
         row's own alignment for no gain. */
      if (tour.parentNode.classList.contains("bar-2")) {
        var wrap = document.createElement("div");
        wrap.className = "cr-wrap";
        tour.parentNode.insertBefore(wrap, tour);
        wrap.appendChild(xs);
        wrap.appendChild(tour);
      } else {
        tour.parentNode.insertBefore(xs, tour);
      }
      faces.push(mk(xs));
    }

    if (faces.length) paint();
  }

  function mk(el) {
    var v = el.querySelector(".cr-n-v");
    return function (t) { v.textContent = t; el.hidden = false; };
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }

  /* The seam, named, so the console and a later backend have one way in. */
  window.Credits = {
    get: read,
    set: function (n) { write(n); paint(); return read(); },
    spend: function (n) { last = 0; spend(n); return read(); },
    rate: PER_MSG
  };
})();
