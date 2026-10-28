(function(){
  var d=document, de=d.documentElement; de.classList.add('js');
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // reveal on scroll (content stays visible without JS or with reduced motion)
  var els=[].slice.call(d.querySelectorAll('.rv'));
  if(reduce||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')})}
  else{
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){io.observe(e)});
    setTimeout(function(){els.forEach(function(e){if(e.getBoundingClientRect().top<innerHeight)e.classList.add('in')})},1500);
  }

  // mobile navigation
  var b=d.querySelector('.burger'), m=d.getElementById('mnav');
  if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');d.body.classList.toggle('nav-open',o);b.setAttribute('aria-expanded',o)});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&m.classList.contains('open')){m.classList.remove('open');d.body.classList.remove('nav-open');b.setAttribute('aria-expanded','false');b.focus()}})}

  // prefill forms from the query string (?system=polyester&finish=sand&industry=...)
  var qs=new URLSearchParams(location.search);
  ['system','finish','industry','gloss','cure','topic'].forEach(function(k){
    var v=qs.get(k); if(!v)return;
    d.querySelectorAll('[data-prefill="'+k+'"]').forEach(function(f){
      if(f.tagName==='SELECT'){[].forEach.call(f.options,function(o){if(o.value===v||o.text.toLowerCase()===v.toLowerCase())f.value=o.value})}
      else if(!f.value){f.value=v}
    });
  });
  var need=d.querySelector('textarea[data-prefill-summary]');
  if(need&&!need.value&&(qs.get('system')||qs.get('finish'))){
    need.value='From the selector: '+['industry','system','finish','gloss','cure'].map(function(k){return qs.get(k)?k+' = '+qs.get(k):''}).filter(Boolean).join(', ')+'\n\nPart / substrate / environment / current product:\n';
  }

  // system selector
  var tool=d.getElementById('selector');
  if(tool){
    var data=JSON.parse(d.getElementById('sel-data').textContent);
    function val(n){var e=tool.querySelector('input[name="'+n+'"]:checked');return e?e.value:''}
    function upd(){
      var env=val('env'), ind=val('ind'), fin=val('fin'), gl=val('gl'), cu=val('cu');
      var rec=null, alts=[], why=[], warn='';
      if(ind&&data.ind[ind]){var r=data.ind[ind];
        if(env){rec=data.envSys[env];
          if(r.main.indexOf(rec)<0&&r.opt.indexOf(rec)<0){warn='For '+r.name+', '+data.sys[rec].name+' is not our usual recommendation. Send us the part so we can confirm.'}
        } else {rec=r.main[0]}
        alts=r.main.concat(r.opt).filter(function(s){return s!==rec});
        why.push('<b>Industry:</b> '+r.name+' · '+r.note);
        if(r.selective)warn=(warn?warn+' ':'')+'Automotive parts and wheels are selective projects, evaluated against your coating system and specification.';
      } else if(env){rec=data.envSys[env]}
      var out=d.getElementById('sel-out');
      if(!rec){out.innerHTML='<small>Recommendation</small><h3>Choose an environment or industry</h3><p class="alt-sys">The result updates as you select.</p>';return}
      var s=data.sys[rec];
      if(env)why.unshift('<b>Environment:</b> '+data.envName[env]);
      why.push('<b>System:</b> '+s.why);
      if(fin)why.push('<b>Finish:</b> '+data.fin[fin]+' is available in all three systems; confirmed on a panel.');
      if(gl)why.push('<b>Gloss:</b> '+data.gl[gl]);
      if(cu)why.push('<b>Cure:</b> '+data.cu[cu]);
      var q=new URLSearchParams();q.set('system',s.name);if(ind)q.set('industry',data.ind[ind].name);if(fin)q.set('finish',data.fin[fin]);if(gl)q.set('gloss',data.gl[gl]);if(cu)q.set('cure',cu==='low'?'Low-cure':'Standard cure');
      out.innerHTML='<small>Suggested system</small><h3>'+s.name+'</h3>'+(alts.length?'<p class="alt-sys">Also used: '+alts.map(function(a){return data.sys[a].name}).join(', ')+'</p>':'')+'<ul>'+why.map(function(w){return '<li>'+w+'</li>'}).join('')+'</ul>'+(warn?'<p class="warn">'+warn+'</p>':'')+'<a class="btn btn-primary" href="/request-sample/?'+q.toString()+'">Request a sample with these choices</a><p class="alt-sys" style="margin-top:14px"><a href="'+s.url+'" style="color:var(--accent-hi)">About '+s.name+' →</a></p>';
    }
    tool.addEventListener('change',upd);upd();
  }
})();

/* ---- update 15: motion polish (respects reduced motion) ---- */
(function(){
  var d=document, root=d.documentElement;
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  // scroll progress bar
  var bar=d.createElement('div'); bar.className='scroll-bar'; bar.setAttribute('aria-hidden','true'); d.body.appendChild(bar);
  var ticking=false;
  function onScroll(){ if(ticking) return; ticking=true; requestAnimationFrame(function(){
    var h=d.documentElement.scrollHeight-innerHeight; bar.style.transform='scaleX('+(h>0?Math.min(1,scrollY/h):0).toFixed(4)+')';
    if(heroImg&&!reduce){ sy=Math.min(scrollY,900)*0.04; setT(); }
    ticking=false; }); }
  var heroImg=d.querySelector('.hero-img img'), px=0, py=0, sy=0;
  function setT(){ if(heroImg) heroImg.style.translate=px.toFixed(1)+'px '+(py+sy).toFixed(1)+'px'; }
  addEventListener('scroll',onScroll,{passive:true}); onScroll();

  if(reduce) return;

  // count-up for proof figures (keeps the original text as the accessible label)
  function countUp(){
    d.querySelectorAll('.proof strong').forEach(function(el,i){
      var txt=el.textContent, m=txt.match(/[\d,]+/); if(!m) return;
      var target=parseInt(m[0].replace(/,/g,''),10), comma=m[0].indexOf(',')>-1, pre=txt.slice(0,m.index), post=txt.slice(m.index+m[0].length);
      var fmt=function(n){var s=String(n);return comma?s.replace(/\B(?=(\d{3})+(?!\d))/g,','):s};
      el.setAttribute('aria-label',txt); var t0=null, delay=150+i*90, dur=1300;
      el.textContent=pre+fmt(0)+post;
      function step(t){ if(t0===null) t0=t; var p=Math.min(1,Math.max(0,(t-t0-delay)/dur)), e=1-Math.pow(1-p,3);
        el.textContent=pre+fmt(Math.round(target*e))+post; if(p<1) requestAnimationFrame(step); }
      requestAnimationFrame(step);
    });
  }
  var proof=d.querySelector('.hero .proof');
  if(proof){
    var start=function(){ if('IntersectionObserver' in window){ var io=new IntersectionObserver(function(es){ if(es[0].isIntersecting){ io.disconnect(); countUp(); } }); io.observe(proof); } else countUp(); };
    if(root.classList.contains('pi-on')) d.addEventListener('pl:intro-done',start,{once:true}); else start();
  }

  // pointer spotlight on cards (desktop only)
  if(matchMedia('(hover:hover) and (pointer:fine)').matches){
    d.querySelectorAll('.card,.svc a,.cert,.region,.fq-cat details').forEach(function(c){
      c.classList.add('spot');
      c.addEventListener('pointermove',function(e){ var r=c.getBoundingClientRect(); c.style.setProperty('--mx',(e.clientX-r.left)+'px'); c.style.setProperty('--my',(e.clientY-r.top)+'px'); });
    });
    // gentle pointer parallax on the hero photo
    var hero=d.querySelector('.hero');
    if(hero&&heroImg){ hero.addEventListener('pointermove',function(e){ var r=hero.getBoundingClientRect(); var x=((e.clientX-r.left)/r.width-.5)*-10, y=((e.clientY-r.top)/r.height-.5)*-8; px=x; py=y; setT(); });
      hero.addEventListener('pointerleave',function(){ px=0; py=0; setT(); }); }
  }
})();

/* certificate lightbox (single image or multi-page report) */
(function () {
  var d = document, last = null;
  function close(lb) { lb.classList.remove('on'); d.documentElement.style.overflow = ''; setTimeout(function () { lb.remove(); }, 300); if (last) last.focus(); }
  d.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-lb]');
    if (!t) return;
    e.preventDefault(); last = t;
    var cap = t.getAttribute('data-lb-cap') || '';
    var pages = (t.getAttribute('data-lb-pages') || t.getAttribute('data-lb')).split('|'), i = 0, multi = pages.length > 1;
    var lb = d.createElement('div'); lb.className = 'lb' + (multi ? ' multi' : ''); lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', cap);
    lb.innerHTML = '<figure><img alt="" width="' + (t.getAttribute('data-lb-w') || '') + '" height="' + (t.getAttribute('data-lb-h') || '') + '"><figcaption></figcaption></figure>' +
      (multi ? '<button type="button" class="lb-nav prev" aria-label="Previous page">‹</button><button type="button" class="lb-nav next" aria-label="Next page">›</button>' : '') +
      '<button type="button" class="lb-x" aria-label="Close">×</button>';
    var im = lb.querySelector('img'), fc = lb.querySelector('figcaption');
    function show(n) {
      i = (n + pages.length) % pages.length; im.src = pages[i];
      im.alt = cap + (multi ? ' – page ' + (i + 1) : '');
      fc.textContent = cap + ' · Fujian Polymer Industry & Trade Co., Ltd.' + (multi ? '  ·  Page ' + (i + 1) + ' / ' + pages.length : '');
      if (multi) { var nx = new Image(); nx.src = pages[(i + 1) % pages.length]; }
    }
    show(0);
    d.body.appendChild(lb); d.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(function () { lb.classList.add('on'); });
    var x = lb.querySelector('.lb-x'); x.focus();
    lb.addEventListener('click', function (ev) {
      if (ev.target === lb || ev.target === x) close(lb);
      else if (ev.target.classList.contains('prev')) show(i - 1);
      else if (ev.target.classList.contains('next') || (multi && ev.target === im)) show(i + 1);
    });
    lb.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') close(lb);
      else if (multi && ev.key === 'ArrowRight') show(i + 1);
      else if (multi && ev.key === 'ArrowLeft') show(i - 1);
      else if (ev.key === 'Tab') { ev.preventDefault(); x.focus(); }
    });
  });
})();

/* motion v2: living backdrop in dark heroes/bands + staggered reveals */
(function () {
  var d = document;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  [].forEach.call(d.querySelectorAll('.hero, .phero, .sec.dark, .cta'), function (s) {
    if (s.querySelector(':scope > .fx')) return;
    var fx = d.createElement('span'); fx.className = 'fx'; fx.setAttribute('aria-hidden', 'true');
    fx.innerHTML = '<i class="fx-grid"></i><i class="fx-glow r"></i><i class="fx-glow b"></i>';
    var ref = s.querySelector(':scope > .bg-img'); s.insertBefore(fx, ref ? ref.nextSibling : s.firstChild);
  });
  var seen = [];
  [].forEach.call(d.querySelectorAll('.rv'), function (el) {
    var p = el.parentElement; if (!p || seen.indexOf(p) > -1) return; seen.push(p);
    var kids = [].filter.call(p.children, function (c) { return c.classList.contains('rv'); });
    if (kids.length < 2) return;
    kids.forEach(function (c, i) { if (c.classList.contains('in')) return; c.style.transitionDelay = Math.min(i, 7) * 85 + 'ms'; c.addEventListener('transitionend', function f(e) { if (e.target === c && e.propertyName === 'opacity') { c.style.transitionDelay = ''; c.removeEventListener('transitionend', f); } }); });
  });
})();
