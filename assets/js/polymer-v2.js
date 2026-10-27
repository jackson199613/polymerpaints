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
