/* POLYMER homepage intro: charge → powder release → cure → colour → approved panel → into the hero.
   Plays once per session (force with ?intro=1), skippable (click / Esc / button), never with reduced motion.
   The <head> snippet adds html.pi-on before first paint; this file runs the timeline. */
(function () {
  var d = document, root = d.documentElement, el = d.getElementById('pi');
  if (!el) return;
  if (!root.classList.contains('pi-on')) { el.remove(); return; }
  try { sessionStorage.setItem('pl-intro', '1'); } catch (e) {}
  el.classList.add('pi-live');

  var Q = function (s) { return el.querySelector(s); };
  var L = { charge: Q('.pi-charge'), burst: Q('.pi-burst'), melt: Q('.pi-melt'), palette: Q('.pi-palette'), panels: Q('.pi-panels') };
  var small = Math.min(innerWidth, innerHeight) < 700 || innerWidth < 760;
  Object.keys(L).forEach(function (k) {
    var node = L[k], src = node.getAttribute(small ? 'data-sm' : 'data-src'), im = new Image();
    im.decoding = 'async'; im.src = src;
    var ok = function () { node.style.backgroundImage = 'url(' + src + ')'; node.classList.add('ok'); };
    if (im.decode) im.decode().then(ok, ok); else im.onload = ok;
  });

  /* ---------- canvas particles ---------- */
  var cv = Q('canvas'), ctx = cv.getContext('2d'), W = 0, H = 0, DPR = Math.min(devicePixelRatio || 1, 2);
  function size() { W = innerWidth; H = innerHeight; cv.width = W * DPR; cv.height = H * DPR; ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
  size(); addEventListener('resize', size);
  function rnd(a, b) { return a + Math.random() * (b - a); }
  function cl(x) { return x < 0 ? 0 : x > 1 ? 1 : x; }
  function eo(t) { return 1 - Math.pow(1 - t, 3); }
  function eio(t) { return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  var M = Math.min(W, H), charge = [], burst = [], n;
  n = small ? 420 : 900;
  for (var i = 0; i < n; i++) {
    var side = Math.random() < .5 ? -1 : 1;
    charge.push({ x: W / 2 + side * rnd(.18, .62) * W, y: rnd(-.1, 1.1) * H, cy: rnd(.35, .6) * H, tx: W / 2 + side * rnd(0, .07) * M, ty: H * rnd(.4, .62),
      dl: rnd(0, .45), s: rnd(.6, 1.8), c: Math.random() < .22 ? '#5aa2e8' : (Math.random() < .5 ? '#e8edf2' : '#9aa6b2') });
  }
  n = small ? 600 : 1300;
  for (i = 0; i < n; i++) {
    var a = rnd(0, 6.2832), ca = Math.cos(a), col = Math.abs(ca) < .16 ? (Math.random() < .7 ? '#f2f4f6' : '#b9c2cc') : (ca < 0 ? (Math.random() < .8 ? '#e1352a' : '#ff6a52') : (Math.random() < .8 ? '#2f7fd4' : '#7fb6f0'));
    burst.push({ a: a, r0: M * rnd(.16, .2), v: M * Math.pow(Math.random(), 1.7) * rnd(.35, .95), s: rnd(.7, 2.6), c: col, k: rnd(.8, 1.25) });
  }
  function drawCharge(t) { // 0..1
    ctx.globalCompositeOperation = 'lighter';
    for (var i = 0; i < charge.length; i++) {
      var p = charge[i], q = eio(cl((t - p.dl) / (1 - p.dl))), q0 = eio(cl((t - p.dl - .06) / (1 - p.dl)));
      if (q >= 1) continue;
      var bx = function (u) { return (1 - u) * (1 - u) * p.x + 2 * (1 - u) * u * (W / 2 + (p.x - W / 2) * .5) + u * u * p.tx; };
      var by = function (u) { return (1 - u) * (1 - u) * p.y + 2 * (1 - u) * u * p.cy + u * u * p.ty; };
      ctx.globalAlpha = (.25 + .75 * q) * (1 - Math.pow(q, 8));
      ctx.strokeStyle = p.c; ctx.lineWidth = p.s;
      ctx.beginPath(); ctx.moveTo(bx(q0), by(q0)); ctx.lineTo(bx(q), by(q)); ctx.stroke();
    }
  }
  function drawBurst(t) { // 0..1
    ctx.globalCompositeOperation = 'lighter';
    var X = W / 2, Y = H / 2;
    for (var i = 0; i < burst.length; i++) {
      var p = burst[i], k = cl(t * p.k), r = p.r0 + p.v * eo(k);
      ctx.globalAlpha = Math.max(0, (1 - k) * .9);
      ctx.fillStyle = p.c;
      var x = X + Math.cos(p.a) * r, y = Y + Math.sin(p.a) * r * .92 + k * k * 30;
      ctx.fillRect(x, y, p.s, p.s);
    }
  }

  /* ---------- timeline (ms) ---------- */
  var T = { burst: 1000, melt: 2150, palette: 3150, panels: 3850, out: 5050, end: 5800 };
  var CAPS = [['01', 'Charge', 'Electrostatic application'], ['02', 'Powder', 'Epoxy · Polyester · Hybrid'], ['03', 'Cure', 'Melt, flow, film'], ['04', 'Colour', 'RAL and custom shades'], ['05', 'Approved', 'Every batch true to the approved panel']];
  var cap = Q('.pi-cap'), bar = Q('.pi-bar i'), scene = -1, t0 = null, skip = 0, released = false, done = false;
  function setScene(i) {
    if (i === scene) return; scene = i;
    el.setAttribute('data-s', String(i + 1));
    cap.classList.remove('in'); void cap.offsetWidth;
    cap.innerHTML = '<span>' + CAPS[i][0] + '</span><b>' + CAPS[i][1] + '</b><em>' + CAPS[i][2] + '</em>'; cap.classList.add('in');
  }
  function release() {
    if (released) return; released = true;
    var hero = d.querySelector('.hero-img');
    el.classList.add('pi-out');
    if (hero && !skip) {
      var r = hero.getBoundingClientRect();
      if (r.width > 40 && r.top < innerHeight) el.style.clipPath = 'inset(' + Math.max(0, r.top) + 'px ' + Math.max(0, innerWidth - r.right) + 'px ' + Math.max(0, innerHeight - r.bottom) + 'px ' + Math.max(0, r.left) + 'px round 2px)';
    }
    root.classList.remove('pi-on');
    try { d.dispatchEvent(new CustomEvent('pl:intro-done')); } catch (e) {}
  }
  function finish() { if (done) return; done = true; el.remove(); }
  function goSkip() { if (skip || released) return; skip = performance.now(); el.classList.add('pi-skip'); release(); setTimeout(finish, 650); }
  el.addEventListener('click', goSkip);
  d.addEventListener('keydown', function (e) { if (!done && (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ')) goSkip(); });

  function frame(now) {
    if (done) return;
    if (t0 === null) t0 = now;
    var t = now - t0;
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.clearRect(0, 0, W, H);
    bar.style.transform = 'scaleX(' + cl(t / T.out).toFixed(4) + ')';
    if (t < T.burst) { setScene(0); drawCharge(t / T.burst); }
    else if (t < T.melt) { if (scene < 1) { el.classList.add('pi-flash'); } setScene(1); drawBurst((t - T.burst) / (T.melt - T.burst + 300)); }
    else if (t < T.palette) { setScene(2); if (t < T.melt + 300) drawBurst((t - T.burst) / (T.melt - T.burst + 300)); }
    else if (t < T.panels) setScene(3);
    else setScene(4);
    if (t >= T.out && !released) { release(); }
    if (t >= T.end) { finish(); return; }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  setTimeout(function () { if (!released) release(); setTimeout(finish, 900); }, 9000); // safety net
})();
