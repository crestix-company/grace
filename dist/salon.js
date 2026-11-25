'use strict';
document.documentElement.classList.add('js');
document.addEventListener('click', event => {
  const filter = event.target.closest('button[data-filter]');
  if (filter) {
    const group = filter.closest('.filters');
    for (const button of group.querySelectorAll('button')) button.setAttribute('aria-pressed', String(button === filter));
    for (const item of document.querySelectorAll('[data-length]')) item.hidden = filter.dataset.filter !== 'すべて' && filter.dataset.filter !== item.dataset.length;
  }
  const menu = document.querySelector('.mobile-nav[open]');
  if (menu && (!menu.contains(event.target) || event.target.closest('a'))) menu.open = false;
});
document.addEventListener('keydown', event => {
  const menu = document.querySelector('.mobile-nav[open]');
  if (event.key === 'Escape' && menu) {
    menu.open = false;
    menu.querySelector('summary').focus();
  }
});
async function reconcileContactForm() {
  const section=document.querySelector('[data-enquiry]');
  if(!section) return;
  const form=section.querySelector('form');
  if(form.dataset.initialized) return;
  form.dataset.initialized='true';
  const button=form.querySelector('button[type="submit"]');
  const note=form.querySelector('[data-form-note]');
  const status=form.querySelector('[data-form-status]');
  const legacy=document.querySelector('.legacy-form');
  const demo=location.protocol==='file:' || Boolean(document.getElementById('site-data'));
  if(legacy && /(^|\.)grace-2012\.com$/i.test(location.hostname)) legacy.hidden=true;
  if(demo){
    note.textContent='プレビュー用です。入力内容は端末内で確認でき、店舗には送信されません。';
    button.textContent='入力内容を確認する';
  }else{
    try{
      const res=await fetch('/api/contact',{cache:'no-store'});
      if(!res.ok || (await res.json()).available!==true) return;
      if(legacy) legacy.hidden=true;
    }catch{ return; }
  }
  section.hidden=false;
  button.disabled=false;
  let ticket;
  form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(button.disabled || !form.reportValidity())return;
    if(demo){status.textContent='入力内容を確認しました。店舗には送信されていません。';return;}
    ticket ||= crypto.randomUUID();
    const data=Object.fromEntries(new FormData(form));
    data.ticket=ticket;
    data.consent=form.elements.consent.checked;
    button.disabled=true;status.textContent='送信中です。';
    try{
      const response=await fetch('/api/contact',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
      const result=await response.json();
      if(!response.ok || result.received!==true)throw new Error(String(response.status));
      form.reset();ticket=undefined;
      status.textContent='お問い合わせを受け付けました。受付番号 '+result.receipt+'。';
    }catch(error){
      status.textContent=error.message==='400'?'メールアドレス・電話番号・本文をご確認ください。':'受付完了を確認できませんでした。再送するか、店舗（054-251-4600）へお電話ください。';
    }finally{button.disabled=false;}
  });
}
reconcileContactForm();
