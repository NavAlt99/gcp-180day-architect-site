(function(){'use strict';
const KEY='gcp-180day-architect-progress-v1', THEME='gcp-180day-architect-theme-v1';
function read(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback}catch(_){return fallback}}
function store(key,value){try{localStorage.setItem(key,JSON.stringify(value))}catch(_){}}
const progress=read(KEY,{});
function setTheme(value){document.documentElement.dataset.theme=value;store(THEME,value);const b=document.getElementById('theme-toggle');if(b)b.textContent=value==='dark'?'☀ Light mode':'☾ Dark mode'}
setTheme(read(THEME,'dark'));
document.getElementById('theme-toggle')?.addEventListener('click',()=>setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark'));
document.querySelectorAll('[data-progress]').forEach(input=>{input.checked=!!progress[input.dataset.progress];input.addEventListener('change',()=>{progress[input.dataset.progress]=input.checked;store(KEY,progress)})});
document.getElementById('day-jump')?.addEventListener('change',e=>{if(e.target.value)location.href=e.target.value});
document.querySelectorAll('pre > code, pre > kbd').forEach((code,index)=>{
  const pre=code.parentElement;
  const wrapper=document.createElement('div');wrapper.className='code-block';
  pre.replaceWith(wrapper);wrapper.appendChild(pre);
  const button=document.createElement('button');button.type='button';button.className='copy-code';
  button.textContent='Copy';button.setAttribute('aria-label','Copy code block '+(index+1));
  button.addEventListener('click',async()=>{
    const value=code.textContent;
    try{
      if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(value)}
      else{
        const temporary=document.createElement('textarea');temporary.value=value;
        temporary.style.position='fixed';temporary.style.opacity='0';document.body.appendChild(temporary);
        temporary.select();const copied=document.execCommand('copy');temporary.remove();if(!copied)throw Error('Clipboard unavailable');
      }
      button.textContent='Copied';setTimeout(()=>button.textContent='Copy',1800);
    }catch(_){button.textContent='Select code to copy';setTimeout(()=>button.textContent='Copy',3000)}
  });
  wrapper.appendChild(button);
});
const search=document.getElementById('day-search'),block=document.getElementById('block-filter'),type=document.getElementById('type-filter');
function filter(){if(!search)return;let shown=0;document.querySelectorAll('.day-card').forEach(card=>{const ok=card.dataset.search.includes(search.value.trim().toLowerCase())&&(!block.value||card.dataset.block===block.value)&&(!type.value||card.dataset.type===type.value);card.hidden=!ok;if(ok)shown++});document.querySelectorAll('[data-block-group]').forEach(group=>{group.hidden=!group.querySelector('.day-card:not([hidden])')});document.getElementById('result-count').textContent=shown+' of 180 days shown'}
[search,block,type].forEach(node=>node?.addEventListener(node===search?'input':'change',filter));filter();
document.getElementById('export-progress')?.addEventListener('click',()=>{const blob=new Blob([JSON.stringify({schema:'gcp-180day-progress-v1',progress},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='gcp-180day-progress.json';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000)});
document.getElementById('import-progress')?.addEventListener('change',async e=>{const status=document.getElementById('progress-status');try{const data=JSON.parse(await e.target.files[0].text());if(data.schema!=='gcp-180day-progress-v1'||!data.progress||typeof data.progress!=='object'||Array.isArray(data.progress))throw Error('Invalid progress file');for(const [key,value] of Object.entries(data.progress)){if(/^(read|artifact|lab)-\d{1,3}(?:-topic-\d{2})?$/.test(key)&&typeof value==='boolean')progress[key]=value}store(KEY,progress);document.querySelectorAll('[data-progress]').forEach(input=>input.checked=!!progress[input.dataset.progress]);status.textContent='Progress imported.'}catch(err){status.textContent='Import failed: '+err.message}});
document.addEventListener('keydown',e=>{const el=document.activeElement;if(e.altKey||e.ctrlKey||e.metaKey||/^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(el?.tagName||'')||el?.isContentEditable||el?.closest('[role=dialog]'))return;const main=document.querySelector('main[data-day]');if(!main)return;const key=e.key.toLowerCase();const path=key==='p'||key==='['?main.dataset.prev:key==='n'||key===']'?main.dataset.next:key==='i'?main.dataset.index:'';if(path){e.preventDefault();location.href=path}});
})();
