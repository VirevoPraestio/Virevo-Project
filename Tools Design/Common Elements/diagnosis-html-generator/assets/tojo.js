/* Tojo canvas runtime — vanilla JS, no dependencies.
   Handles: expanders, station picking (route-map), calculators, and the
   chat<->canvas point highlight used by the host app (window.tojoCanvas.lightPoints). */
(function () {
  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }

  // ---- expanders: <button data-tj-toggle="id" aria-expanded="false"> + <div id="id" hidden>
  function initToggles(root) {
    all(root, '[data-tj-toggle]').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = root.querySelector('#' + b.getAttribute('data-tj-toggle'));
        var open = b.getAttribute('aria-expanded') !== 'true';
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
        var lbl = b.querySelector('[data-open-label]');
        if (lbl) lbl.textContent = open ? lbl.getAttribute('data-open-label') : lbl.getAttribute('data-shut-label');
        if (t) t.hidden = !open;
      });
    });
  }

  // ---- station picking: buttons [data-tj-pick="group:id"], panels [data-tj-panel="group:id"]
  function initPick(root) {
    all(root, '[data-tj-pick]').forEach(function (b) {
      b.addEventListener('click', function () {
        var key = b.getAttribute('data-tj-pick'), grp = key.split(':')[0];
        all(root, '[data-tj-pick^="' + grp + ':"]').forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-tj-pick') === key ? 'true' : 'false'); });
        all(root, '[data-tj-panel^="' + grp + ':"]').forEach(function (p) { p.hidden = p.getAttribute('data-tj-panel') !== key; });
      });
    });
  }

  // ---- tiny safe expression evaluator: numbers, identifiers, + - * / ( ), unary minus, min/max/round
  function evaluate(expr, vars) {
    var toks = expr.match(/\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*|[-+*/(),]/g) || [], i = 0;
    function peek() { return toks[i]; } function next() { return toks[i++]; }
    function primary() {
      var t = next();
      if (t === '(') { var v = add(); next(); return v; }
      if (t === '-') return -primary();
      if (/^\d/.test(t)) return parseFloat(t);
      if (peek() === '(') { next(); var args = [add()]; while (peek() === ',') { next(); args.push(add()); } next();
        if (t === 'min') return Math.min.apply(null, args); if (t === 'max') return Math.max.apply(null, args);
        if (t === 'round') return Math.round(args[0]); throw new Error('unknown function ' + t); }
      if (!(t in vars)) throw new Error('unknown name ' + t);
      return vars[t];
    }
    function mul() { var v = primary(); while (peek() === '*' || peek() === '/') { var o = next(), r = primary(); v = o === '*' ? v * r : v / r; } return v; }
    function add() { var v = mul(); while (peek() === '+' || peek() === '-') { var o = next(), r = mul(); v = o === '+' ? v + r : v - r; } return v; }
    return add();
  }
  var fmt = {
    int: function (n) { return Math.round(n).toLocaleString('en-IN'); },
    dec1: function (n) { return String(Math.round(n * 10) / 10); },
    pct: function (n) { return (Math.round(n * 10) / 10) + '%'; },
    inr: function (n) { return '₹' + Math.round(n).toLocaleString('en-IN'); },
    inr_l: function (n) { return '₹' + (Math.round(n / 1e4) / 10) + ' lakh'; },
    inr_cr: function (n) { return '₹' + (Math.round(n / 1e6) / 10) + ' crore'; },
    days: function (n) { return (Math.round(n * 100) / 100) + (n === 1 ? ' day' : ' days'); },
    hours: function (n) { return (Math.round(n * 10) / 10) + (n === 1 ? ' hour' : ' hours'); },
    raw: function (n) { return String(n); }
  };
  window.tojoFormat = fmt;

  function initCalc(root) {
    all(root, '[data-tj-calc]').forEach(function (c) {
      var spec = JSON.parse(c.querySelector('script[type="application/json"]').textContent);
      function run() {
        var vars = {}, missing = false;
        spec.inputs.forEach(function (inp) {
          var el = c.querySelector('[data-in="' + inp.id + '"]');
          var raw = el ? el.value : '';
          if (raw === '' || raw === null) { missing = true; return; }
          vars[inp.id] = parseFloat(raw);
          var out = c.querySelector('[data-in-val="' + inp.id + '"]');
          if (out) out.textContent = (fmt[inp.format] || fmt.raw)(vars[inp.id]);
        });
        spec.steps.forEach(function (st) {
          var out = c.querySelector('[data-step="' + st.id + '"]');
          var v;
          try { v = evaluate(st.formula, vars); vars[st.id] = v; } catch (e) { v = null; }
          if (out) out.textContent = (v === null || isNaN(v)) ? '—' : (fmt[st.format] || fmt.raw)(v);
        });
        var w = c.querySelector('[data-tj-waiting]');
        if (w) w.hidden = !missing;
      }
      all(c, '[data-in]').forEach(function (el) { el.addEventListener('input', run); });
      run();
    });
  }

  function lightPoints(root, nums) {
    all(root, '[data-tj-point]').forEach(function (el) {
      var on = nums.indexOf(parseInt(el.getAttribute('data-tj-point'), 10)) !== -1;
      el.classList.toggle('tj-lit', on);
    });
  }

  function init(root) { root = root || document; initToggles(root); initPick(root); initCalc(root); }
  window.tojoCanvas = { init: init, lightPoints: lightPoints, evaluate: evaluate };
  if (document.readyState !== 'loading') init(document); else document.addEventListener('DOMContentLoaded', function () { init(document); });
})();
