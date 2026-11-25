"""Build the production archive and portable, navigable review copy."""
import base64, gzip, io, json, re, zipfile
from pathlib import Path
from html import escape
from PIL import Image
from original_media import ORIGIN, UPLOADS, FILES
from build import DIST, ROOT, build, pages


WORKSPACE=ROOT.parent
JS=r"""
const payload=JSON.parse(document.querySelector('#site-data').textContent);
const photos=JSON.parse(document.querySelector('#site-photos').textContent);
let activeRoute=null;
function splitHash(){
  const text=location.hash.slice(1);
  if (!text.startsWith('/')) return ['', ''];
  const [path, params='']=text.slice(1).split('?');
  return [Object.hasOwn(payload,path)?path:'',new URLSearchParams(params).get('at')||''];
}
function renderPage(route, target='', initial=false){
  const data=payload[route];
  if (!data) return;
  if(activeRoute!==route){
    document.querySelector('#site').innerHTML=data[1];
    document.title=data[0]+'｜grace hair dressing 鷹匠';
    for(const image of document.querySelectorAll('img[data-photo]')) {
      image.src=photos[image.dataset.photo];
    }
    for(const image of document.querySelectorAll('img[data-original]')) {
      image.src=photos[image.dataset.original] || image.dataset.originalUrl;
    }
    activeRoute=route;
    if(typeof reconcileContactForm==='function')reconcileContactForm();
    if(!initial) document.querySelector('main').focus({preventScroll:true});
  }
  if(target){
    const element=document.getElementById(target);
    if(element) element.scrollIntoView({block:'start',behavior:'instant'});
  }else{window.scrollTo({top:0,behavior:'instant'});}
}
function go(route,target=''){
  const hash='#/'+route+(target?'?at='+encodeURIComponent(target):'');
  if(location.hash!==hash){try{location.hash=hash;}catch(error){}}
  renderPage(route,target);
}
document.addEventListener('click',event=>{
  const a=event.target.closest('a');
  if(!a || event.button!==0 || event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
  const href=a.getAttribute('href')||'';
  if(href.startsWith('#/')){
    event.preventDefault();
    const [route,params='']=href.slice(2).split('?');
    go(route,new URLSearchParams(params).get('at')||'');
  }else if(href.startsWith('#')&&href.length>1){
    event.preventDefault();go(activeRoute,href.slice(1));
  }
});
window.addEventListener('hashchange',()=>renderPage(...splitHash()));
renderPage(...splitHash(),true);
"""
def render_docs():
    out={}
    for route,(title,html) in pages.items():
        def anchor(match):
            tag=match.group()
            go=re.search(r'data-go="([^"]*)"',tag)
            if not go: return tag
            href=re.search(r'href="([^"]*)"',tag)
            fragment=href[1].partition('#')[2]
            value='#/'+go[1]+('?at='+fragment if fragment else '')
            return tag[:href.start(1)]+value+tag[href.end(1):]
        def photo(match):
            tag=match.group()
            original=re.search(r'data-original="([^"]+)"',tag)
            if original:
                return re.sub(r' src="[^"]*"', ' data-original-url="'+ORIGIN+original[1]+'"',tag,count=1)
            return re.sub(r' src="[^"]*"','',tag, count=1) if 'data-photo=' in tag else tag
        html=re.sub(r'<a\b[^>]*>',anchor,html)
        html=re.sub(r'<img\b[^>]*>',photo,html)
        out[route]=[title,html]
    return out
def photo_urls(compact):
    images={}
    for path in sorted((DIST/'assets').glob('*.webp')):
        if compact:
            with Image.open(path) as photo:
                w=420 if path.stem in ('style-2','style-3') else (345 if path.stem.startswith('style') else 195)
                photo.thumbnail((w,800))
                data=io.BytesIO()
                photo.save(data,'WEBP',quality=65,method=6)
                raw=data.getvalue()
        else:raw=path.read_bytes()
        images[path.stem]='data:image/webp;base64,'+base64.b64encode(raw).decode()
    for name in FILES:
        path=DIST/UPLOADS/name
        if path.is_file():
            if compact:
                with Image.open(path) as photo:
                    photo.thumbnail((300,150) if name=='rogo.jpg' else (320,230))
                    data=io.BytesIO()
                    photo.convert('RGB').save(data,'WEBP',quality=60,method=6)
                    images[name]='data:image/webp;base64,'+base64.b64encode(data.getvalue()).decode()
            else:
                images[name]='data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode()
    return images
def jsdata(data):
    return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
def make_preview(dest, compact, docs):
    icons=base64.b64encode((DIST/'favicon.svg').read_bytes()).decode()
    css=(DIST/'salon.css').read_text()
    behavior=(DIST/'salon.js').read_text()
    photos=photo_urls(compact)
    # Compress repeated page chrome in the private embedded version, leaving desktop preview synchronous.
    dataset=jsdata(docs)
    router=JS
    mode='application/json'
    if compact:
        dataset=base64.b64encode(gzip.compress(dataset.encode(),mtime=0)).decode()
        router=router.replace("const payload=JSON.parse(document.querySelector('#site-data').textContent);","const bytes=Uint8Array.from(atob(document.querySelector('#site-data').textContent),char=>char.charCodeAt(0)); const payload=JSON.parse(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).text());")
        router='(async()=>{'+router+"})().catch(()=>{document.getElementById('site').textContent='このプレビューを表示するには、新しいブラウザで開いてください。';});"
        mode='application/octet-stream'
    doc='<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>grace hair dressing 鷹匠</title><link rel="icon" href="data:image/svg+xml;base64,'+icons+'"><style>'+css+'</style></head><body><div id="site"></div><noscript>ZIPを展開してindex.htmlを開くと、JavaScriptを使わずにサイトをご覧いただけます。</noscript><script type="'+mode+'" id="site-data">'+dataset+'</script><script type="application/json" id="site-photos">'+jsdata(photos)+'</script><script>'+behavior+'</script><script>'+router+'</script></body></html>'
    dest.write_text(doc)
    return dest.stat().st_size
def archive():
    with zipfile.ZipFile(WORKSPACE/'grace-hair-website.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(DIST.rglob('*')):
            if path.is_file() and not any(n.startswith('.') for n in path.relative_to(DIST).parts):
                archive.write(path,path.relative_to(DIST))
if __name__=='__main__':
    build()
    docs=render_docs()
    local=make_preview(WORKSPACE/'grace-preview.html',False,docs)
    compact=make_preview(WORKSPACE/'work'/'compact-preview.html',True,docs)
    archive()
    print(f'{len(docs)} independent pages, local preview {local:,} bytes, private preview {compact:,} bytes')
