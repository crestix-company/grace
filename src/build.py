from pathlib import Path
from html import escape
import json, os, re, posixpath, urllib.parse
from recruitment import BENEFITS, GROUPS, ROLES
from original_media import source as original_source
from content import BOOK, HPB, FORM, TEL, ADDRESS, STYLE, MENU, NEWS

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
WORK='https://work.beauty.hotpepper.jp/WC00005518/WS0000002591/'
MAP='https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote('grace hair dressing 鷹匠 '+ADDRESS)
nav=[('styles','Style','スタイル'),('menu','Menu','メニュー'),('staff','Staff','スタッフ'),('blog','News','お知らせ'),('job-offer','Recruit','採用情報'),('contact','Access','店舗・お問い合わせ')]
pages={}
current=''
def path(route):
    return posixpath.relpath((route+'/' if route else '')+'index.html', current or '.')
def asset(name): return posixpath.relpath(name,current or '.')
def link(route,body,cls='',frag=''):
    return f'<a href="{path(route)}{("#"+frag) if frag else ""}" data-go="{route}" class="{cls}">{body}</a>'
def out(url,body,cls=''):
    ext='' if url.startswith('tel:') else ' target="_blank" rel="noopener noreferrer"'
    return f'<a href="{escape(url,quote=True)}"{ext} class="{cls}">{body}</a>'
arrow='<i class="arrow" aria-hidden="true">↗</i>'
right='<i class="arrow" aria-hidden="true">→</i>'
def pic(name,alt,cls='',priority=False):
    from PIL import Image
    with Image.open(DIST/'assets'/(name+'.webp')) as f: w,h=f.size
    live='fetchpriority="high"' if priority else 'loading="lazy"'
    return f'<img src="{asset("assets/"+name+".webp")}" data-photo="{name}" alt="{escape(alt,quote=True)}" class="{cls}" width="{w}" height="{h}" decoding="async" {live}>'
def original_img(name,alt,cls,priority=False):
    url = original_source(name,DIST,asset)
    loading = 'fetchpriority="high"' if priority else 'loading="lazy"'
    return f'<img class="{cls}" data-original="{name}" src="{url}" alt="{escape(alt,quote=True)}" decoding="async" {loading}>'
def brand(footer=False):
    return link('',original_img('rogo.jpg','grace hair dressing トップへ','brand-logo',not footer),'brand')
def reserve(label='空席確認・WEB予約'):
    return out(BOOK,label+arrow,'cta')
def active(parent):
    return current==parent or (parent=='styles' and current.startswith('styles/')) or (parent=='job-offer' and current in ROLES)
def navitem(k,en,ja,footer=False):
    return f'<a data-go="{k}" href="{path(k)}"'+(' aria-current="page"' if current==k else '')+(' class="active"' if active(k) else '')+f'><span lang="en">{en}</span><small>{ja}</small></a>'
def header():
    return f'''<a class="skip" href="#main">本文へ移動</a><header class="mast" id="top"><div class="mast-in">{brand()}<nav class="wide-nav" aria-label="メインメニュー">{"".join(navitem(*v) for v in nav)}</nav><div class="actions">{reserve("WEB予約")}<details class="mobile-nav"><summary aria-label="サイトメニュー"><b></b><b></b></summary><nav aria-label="モバイルメニュー">{link('','トップ')}{''.join(navitem(*v) for v in nav)}</nav></details></div></div></header>'''
def crumb(name,parent=None):
    return '<nav class="crumb wrap" aria-label="パンくず">'+link('','Top')+'<span>/</span>'+(link(parent[0],parent[1])+'<span>/</span>' if parent else '')+f'<span aria-current="page">{name}</span></nav>'
def footer():
    return f'''<footer class="foot"><div class="wrap"><div class="foot-main"><div>{brand(True)}<p>静岡・鷹匠のヘアサロン</p></div><div><p>〒420-0839<br>{ADDRESS}</p>{out(TEL,'054-251-4600','foot-tel')}</div><nav aria-label="フッターメニュー">{''.join(link(k,ja) for k,en,ja in nav)}</nav></div><div class="foot-end"><span>© grace hair dressing</span>{link('','トップページへ '+right)}</div></div></footer>'''
def intro(en,ja,desc):
    return f'<div class="page-title wrap"><div><div class="over">{ja}</div><h1 lang="en">{en}</h1></div><p>{desc}</p></div>'
def heading(en,ja):
    return f'<div class="heading"><span class="over">{ja}</span><h2 lang="en">{en}</h2></div>'
def stylecard(i,priority=False):
    slug,en,ja,length,*_=STYLE[i-1]
    return link('styles/'+slug,pic('style-'+str(i),ja,priority=priority)+f'<div class="stylecap"><div><small>{length}</small><strong>{ja}</strong></div>{right}</div>','stylecard')
def newslist(n):
    return '<div class="newslist">'+''.join(out(HPB+'blog/'+key+'.html',f'<time datetime="{d.replace(".","-")}">{d}</time><span class="news-cat">{cat}</span><span class="news-name">{title}</span>{arrow}','newsrow') for d,cat,title,who,blurb,key in NEWS[:n])+'</div>'
def addr():
    return '<dl class="facts">'+''.join('<div><dt>'+a+'</dt><dd>'+b+'</dd></div>' for a,b in [('所在地','〒420-0839<br>'+ADDRESS),('営業時間','10:00 – 20:00'),('最終受付','カット 18:30 ／ カラー・パーマ 18:00 ／ ストレート 17:00'),('定休日','月曜日（祝日の場合は翌火曜日）'),('電話',out(TEL,'054-251-4600')),('駐車場','近隣の駐車場をご利用ください。')])+'</dl>'
def interior():
    return '<figure class="room"><div class="room-surface">'+original_img('IMG_9091-1.jpg','grace hair dressing 鷹匠の店内','original-photo')+'</div><figcaption><span>Salon interior</span>　grace hair dressing 鷹匠</figcaption></figure>'
def home():
    return f'''<section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="dash"></span> 静岡・鷹匠のヘアサロン</div><h1>横顔に、<br><em>似合う髪。</em></h1><p>頬をかすめる毛先も、耳にかけたときの丸みも。<br>あなたの髪の動きから、明日のスタイルを考えます。</p>{link('styles','スタイルを見つける '+right,'under')}</div><div class="hero-photos"><figure class="hero-main">{link('styles/nuance-bob',pic('style-2','柔らかなブラウンの外ハネニュアンスボブ',priority=True))}<figcaption><span>Nuance bob</span> / 外ハネニュアンスボブ</figcaption></figure><figure class="hero-side">{link('styles/round-short',pic('style-3','横から見たセンターパートショート',priority=True))}<figcaption>Round short</figcaption></figure></div></section>
    <div class="info-ribbon"><div class="wrap"><span><i class="dot"></i> 新静岡駅・セノバ鷹匠口の正面</span><span class="hours-ribbon">営業時間 10:00 – 20:00</span>{link('contact','アクセス・地図 '+right)}</div></div>
    <section class="wrap section"><div class="section-top">{heading('Style book','ヘアスタイル')}{link('styles','すべてのスタイル '+right,'under')}</div><div class="stylegrid picks">{''.join(stylecard(i) for i in (4,1,6))}</div></section>
    <section class="menu-home"><div class="wrap split"><div>{heading('Menu','メニュー・料金')}<p>長さを変える日も、手触りを整える日も。</p>{link('menu','料金表をすべて見る '+right,'under')}</div><div class="menu-teaser">{''.join(link('menu',f'<span>{ja}<small>{en}</small></span><span class="teaser-price">¥{price}</span>{right}',frag=k) for k,ja,en,price in [('cut','カット','Cut','5,490〜'),('color','グロスカラー','Color','8,990〜'),('care','トリートメント','Treatment','4,500〜')])}</div></div></section>
    <section class="wrap section philosophy">{interior()}<div><span class="over">graceの考え方</span><h2 class="jp-title">家に帰ってからが、<br>本当の仕上がり。</h2><p>朝、髪にかけられる時間。よく着る服の色。カウンセリングで交わす何気ない会話が、似合う髪への手がかりです。</p><p>サロンで見た形を、ご自宅でも楽しめるように。髪の乾かし方や顔まわりの整え方まで、担当のスタッフがお伝えします。</p>{link('staff','スタッフを知る '+right,'under')}</div></section>
    <section class="wrap news-home"><div class="section-top">{heading('Journal','サロンからのお知らせ')}{link('blog','記事一覧 '+right,'under')}</div>{newslist(3)}</section>
    <section class="visit"><div class="wrap split"><div>{heading('Visit us','ご来店案内')}<p>新静岡セノバの鷹匠口を出て、正面のビルの2階へ。</p></div><div class="visit-act">{reserve()}{link('contact','住所・営業時間・お問い合わせ '+right,'under')}</div></div></section>'''
def menu_page():
    index=''.join(f'<a href="#{k}">{ja}<i>↓</i></a>' for k,en,ja,desc,rows in MENU)
    sections=''
    for k,en,ja,desc,rows in MENU:
        items=''.join(f'<div class="price-row"><dt>{item}{("<small>"+note+"</small>") if note else ""}</dt><dd class="yen">{("" if price=="お問い合わせ" else "¥")+price}</dd></div>' for item,price,note in rows)
        extra=''
        if k=='color': extra='<div class="carenote"><strong>地肌に合わせた塗り方</strong><p>しっかり根元から染める方法のほか、根元ぎりぎりで塗るセミゼロテク、地肌から離して塗るゼロテクも選べます。</p></div>'
        if k=='care': extra='<div class="carenote"><strong>髪の状態を見て選ぶケア</strong><p>カラーを重ねた毛先、乾燥で広がる部分など、気になる手触りをカウンセリングで確認します。ホームケアも合わせてご相談ください。</p></div>'
        sections+=f'<section id="{k}" class="price-section"><h2><span>{en}</span>{ja}</h2><p>{desc}</p><dl class="prices">{items}</dl>{extra}</section>'
    return crumb('メニュー')+intro('Menu','メニュー・料金','仕上がりを想像しながら選べる、graceのメニューブック。<br>表示料金はすべて税込です。')+f'''<div class="menubody wrap"><aside><nav class="price-index" aria-label="料金の目次"><strong>施術から選ぶ</strong>{index}</nav></aside><div>{sections}<div class="endbook"><p>組み合わせメニューやご希望日の空き状況はこちら。</p>{reserve('メニューを選んで予約')}</div></div></div>'''
def styles():
    return crumb('ヘアスタイル')+intro('Style book','ヘアスタイル','顔まわりの長さ、毛先の動き、色のニュアンス。<br>気になる写真を開いて、横顔までご覧ください。')+'<div class="wrap shelf"><div class="filters" aria-label="髪の長さで表示を切り替える">'+''.join(f'<button type="button" data-filter="{s}" aria-pressed="{str(s=="すべて").lower()}">{s}</button>' for s in ('すべて','ショート','ボブ','ミディアム'))+'</div><div class="stylegrid gallery">'+''.join('<div data-length="'+STYLE[i-1][3]+'">'+stylecard(i,i<4)+'</div>' for i in [2,3,4,1,5,6])+'</div></div>'
def style_detail(i):
    slug,en,ja,length,desc,note,cat,catlink=STYLE[i-1]
    nxt=STYLE[i%len(STYLE)]
    return crumb(ja,('styles','ヘアスタイル'))+f'''<div class="wrap style-sheet"><div class="sheet-image">{pic('style-'+str(i),ja,priority=True)}</div><article><span class="over">{length} ／ Hair design</span><h1 lang="en">{en}</h1><h2>{ja}</h2><p class="lead">{desc}</p><div class="styletip"><h3>オーダーのヒント</h3><p>{note}</p></div>{link('menu',cat+'の料金を見る '+right,'under',catlink)}<div class="sheet-action">{reserve('このスタイルを相談・予約')}</div></article></div><nav class="wrap spread-foot" aria-label="スタイルナビゲーション">{link('styles','← スタイル一覧')}{link('styles/'+nxt[0],'次のスタイル　'+nxt[2]+' →')}</nav>'''
def staff():
    names=[('YUICHIRO','代表 ／ カラー＆ヘアケアソムリエ','横顔のバランスや、髪が乾いたときの形を見ながら、ご自宅で再現しやすいスタイルをつくります。','料理・お菓子作り・園芸'),('JUN','スタイリスト ／ カラー＆ヘアケアソムリエ','じっくりお話を伺い、ボブのラインやカラーの透明感など、なりたい雰囲気を一緒に形にします。','映画・パワースポット巡り'),('MAHO','ケアリスト ／ カラーソムリエ','丁寧なカウンセリングを通じて、カラーを楽しむ髪のツヤや手触りを整えるケアをご提案します。','音楽・韓国ドラマ・食べ歩き'),('ASAKI','ケアリスト','お客様が肩の力を抜いて過ごせるように。ご来店時のご挨拶からシャンプーまで、心地よい時間を大切にします。','レコード・サウナ・絵・古着屋巡り')]
    return crumb('スタッフ')+intro('Our team','スタッフ紹介','髪を切る人、色を考える人、地肌と向き合う人。<br>鷹匠でお迎えする、graceのチームです。')+'<div class="wrap"><div class="portraits" aria-label="graceのスタッフ写真">'+''.join(pic('team-'+str(i),'graceのスタッフ',priority=i<=2) for i in range(1,5))+'</div><div class="staff-profiles">'+''.join(f'<article><span class="over">{role}</span><h2>{name}</h2><p>{bio}</p><div class="hobby">休日の楽しみ　{hobby}</div></article>' for name,role,bio,hobby in names)+'</div><div class="endbook">'+out(HPB+'stylist/','担当者・出勤スケジュールを見る '+arrow,'cta')+'</div></div>'
def journal():
    return crumb('お知らせ')+intro('Journal','お知らせ・サロン日記','スタイルのご提案と、鷹匠のお店での日々。<br>スタッフが綴った記事をお届けします。')+'<div class="wrap journal">'+''.join(out(HPB+'blog/'+key+'.html',f'<div class="journal-meta"><time>{d}</time><small>{cat}</small></div><div><h2>{title}</h2><p>{blurb}</p><small>文　{who}</small></div>{arrow}','journal-row') for d,cat,title,who,blurb,key in NEWS)+'<div class="endbook">'+out(HPB+'blog/','スタッフブログの全記事へ '+arrow,'under')+'</div></div>'
def contact():
    return crumb('店舗・お問い合わせ')+intro('Access','店舗・お問い合わせ','新静岡駅で降りて、鷹匠口へ。<br>道路を挟んだ向かいのビル、2階がgraceです。')+f'''<div class="wrap access-grid"><div class="direction"><span class="over">新静岡駅からの道順</span><ol><li><small>静岡鉄道</small><strong>新静岡駅</strong></li><li><small>新静岡セノバ</small><strong>鷹匠口を出て正面へ</strong></li><li><small>サングリアの入るビル</small><strong>エスパシオ鷹匠 2階</strong></li></ol>{out(MAP,'Google マップで道順を開く '+arrow,'under')}</div><div>{heading('Salon info','店舗情報')}{addr()}</div></div>
    <div class="wrap salon-atmos">{interior()}<div><span class="over">店内のご案内</span><h2 class="jp-title">鷹匠の街から、<br>ひと息つける場所へ。</h2><p>茶色を基調にした店内に、穏やかな照明とBGM。外からの視線が届きにくい席で、ゆっくりとお過ごしいただけます。</p></div></div><section class="wrap contactbox"><div>{heading('Contact','ご予約・お問い合わせ')}<p>空席確認・ご予約はネットで。予約内容の変更や、<br>ご来店前のご相談は店舗へお電話ください。</p></div><div class="contact-actions">{reserve()}{out(TEL,'電話する　054-251-4600','stroke')}{out(FORM,'お問い合わせフォームを開く '+arrow,'under legacy-form')}</div></section>
    {(ROOT/'src'/'contact_form.html').read_text()}<section class="wrap faq"><h2>ご来店前のよくあるご質問</h2>{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in [('髪型が決まっていなくても相談できますか？','はい。普段のスタイリングや気になる部分を伺いながら形を決めていきます。気になる写真があればお持ちください。'),('前髪だけでも予約できますか？','前髪カットをご用意しています。店舗へお電話ください。'),('車で来店できますか？','専用駐車場はございません。お近くの駐車場をご利用ください。')])}</section>'''
def job_facts(rows):
    return '<dl class="facts role-facts">'+''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label,value in rows)+'</dl>'

def recruit_category(group):
    ja,en,photo,description,slugs = group
    jobs = []
    for slug in slugs:
        role = ROLES[slug]
        jobs.append(link(slug, f'<span><strong>{role["name"]}</strong><small>{role["pay"]}</small></span>{right}', 'jobrow'))
    return f'''<article class="position-group">
      {original_img(photo, ja+'の募集案内に掲載されたgraceの写真','position-photo')}
      <div class="position-copy"><span lang="en">{en}</span><h3>{ja}</h3><p>{description}</p></div>
      <div class="position-links">{''.join(jobs)}</div></article>'''

def entry_form():
    form = (ROOT/'src'/'contact_form.html').read_text()
    options = ''.join(f'<option>{r["name"]}</option>' for r in ROLES.values())
    form = form.replace('class="wrap enquiry"', 'class="enquiry entry-form"').replace('<details>', '<details open>')
    form = form.replace('Contact form', 'Entry form').replace('フォームで相談する', '応募・見学フォーム')
    form = form.replace('予約や当日の変更は店舗へお電話ください。','希望する職種と、応募・見学についてお聞かせください。')
    start = form.index('<label>ご相談の種類')
    end = form.index('</label>',start) + len('</label>')
    form = form[:start] + f'<input type="hidden" name="subject" value="採用・見学"><label>希望職種 <small>必須</small><select name="role" required><option value="">職種を選んでください</option>{options}<option>まずは見学を希望</option></select></label>' + form[end:]
    return form.replace('お問い合わせ内容','応募・見学のご希望').replace('maxlength="2000"','maxlength="1900"')

def recruit():
    benefits = ''.join(f'<div><h3>{title}</h3><p>{description}</p></div>' for title,description in BENEFITS)
    return crumb('採用情報') + f'''
    <section class="wrap hiring-hero"><div class="hiring-copy"><span class="over" lang="en">Recruit</span>
      <h1>鷹匠で、<br>美容師として働く。</h1><p>新卒のアシスタントから、次のサロンを探しているスタイリストまで。graceの仕事と、あなたに合う働き方をご紹介します。</p>
      <a class="under" href="#positions">職種と給与を見る <span aria-hidden="true">↓</span></a></div>
      <figure>{original_img('IMG_9091-2.jpg','grace hair dressing 鷹匠の採用ページのサロン写真','hiring-cover',True)}</figure></section>
    <nav class="hiring-nav" aria-label="採用ページの目次"><div class="wrap"><a href="#workplace">サロンを知る</a><a href="#positions">募集職種</a><a href="#benefits">福利厚生</a><a href="#entry">見学・応募</a></div></nav>
    <section class="wrap hiring-section" id="workplace"><div class="hiring-intro"><div>{heading('Life at grace','graceで働く')}</div><div>
      <h3>お客様を迎える時間も、技術を磨く時間も。</h3><p>朝礼では、その日の予約と施術の注意点をスタッフで共有。営業中はお客様の髪と向き合い、空いた時間にはウィッグで練習したり、先輩に手の動かし方を見てもらったりします。営業の終わりには施術内容を記録し、次の来店に備えます。</p>
      {link('staff','一緒に働くスタッフを見る '+right,'under')}</div></div>
      <dl class="hiring-numbers"><div><dt>スタッフの平均勤続年数</dt><dd>8.6<small>年</small></dd></div><div><dt>正社員の年間休日</dt><dd>110<small>日</small></dd></div><div><dt>パートの勤務日数</dt><dd><small>週</small>2〜6<small>日</small></dd></div></dl>
      <p class="source-note">勤続年数はサロン公表時点の実績です。</p></section>
    <section class="positions-band" id="positions"><div class="wrap hiring-section">{heading('Positions','職種別の募集要項')}
      <div class="position-grid">{''.join(recruit_category(group) for group in GROUPS)}</div>
      <p class="source-note">金額はサロンの募集要項に基づきます。最新の募集枠は応募窓口でご確認ください。各職種の詳細では、手当・勤務時間・応募資格をご覧いただけます。</p></div></section>
    <section class="wrap hiring-section" id="benefits"><div class="hiring-intro"><div>{heading('Benefits','福利厚生・休暇')}</div><div class="benefit-list">
      <div><h3>休日と休暇</h3><p>正社員は月8〜9日休み。年末年始のほか、年3日のリフレッシュ休暇、産前産後・育児・慶弔休暇があります。</p></div>
      <div><h3>社会保険</h3><p>正社員は社会保険を完備。パートの方は勤務条件に応じて適用されます。</p></div>{benefits}</div></div></section>
    <section class="entry-band" id="entry"><div class="wrap hiring-section"><div class="hiring-intro"><div>{heading('Entry','サロン見学・応募')}</div><div><h3>まずは、お店を見に来ませんか。</h3>
      <p>見学のご相談はお電話で承ります。希望職種とご都合のよい日時をお知らせください。オンライン応募は求人票から受け付けています。</p><div class="entry-actions">{out(WORK,'求人票を確認して応募 '+arrow,'cta')}{out(TEL,'電話で相談　054-251-4600','under')}</div></div></div>
      {entry_form()}</div></section>'''

def jobpage(slug):
    role = ROLES[slug]
    lead,detail = role['lead'],role['detail']
    group = next(g for g in GROUPS if slug in g[4])
    name = role['name']
    terms = [('給与',role['pay']+'（'+role['pay_basis']+'）')]
    if role.get('board_pay'):
        terms += [('求人媒体での掲載例', role['board_pay'])]
    terms += [('手当',role['allowance']),('賞与・昇給',role['bonus'])]
    schedule = [('勤務時間・日数',role['hours']),('残業',role['overtime']),('休日',role['days']),('休暇・家庭との両立',role['leave'])]
    benefits = [('保険',role['insurance'])]+list(BENEFITS)
    conditions = [('雇用形態',role['contract']),('資格・経験',role['qualification']),('試用期間','なし'),('勤務地','grace hair dressing 鷹匠<br>'+ADDRESS)]
    source_note = ('給与・手当の欄はサロンの公式募集要項に基づきます。HOT PEPPER Beauty WORKでは別条件の掲載例があります。応募時は希望する募集枠の求人票をご確認ください。' if 'board_pay' in role else '金額・制度はサロン公表の募集要項によります。募集状況と適用条件は、応募前にご確認ください。')
    example = ('<aside class="pay-example"><h3>'+('正社員登用' if slug=='assistant' else 'スタッフの支給例')+'</h3><p>'+role['example']+'</p></aside>') if role.get('example') else ''
    return crumb(name,('job-offer','採用情報'))+f'''
    <div class="wrap jobdetail"><aside class="role-summary"><span class="over">{role['group']} ／ {role['contract']}</span><h1>{name}</h1><p>{lead}</p>
      {original_img(group[2],group[0]+'のサロン写真','role-photo')}
      <div class="role-nav"><a href="#pay">給与・手当</a><a href="#hours">勤務・休暇</a><a href="#conditions">応募条件</a></div>
      {link('job-offer','見学・応募の窓口へ '+right,'cta','entry')}</aside>
      <article class="role-body"><section><h2>担当する仕事・研修</h2><p>{detail}</p><p>{role['training']}</p></section>
      <section id="pay"><h2>給与・手当</h2>{job_facts(terms)}<p class="source-note">{source_note}</p>{example}</section>
      <section id="hours"><h2>勤務時間・休日</h2>{job_facts(schedule)}</section>
      <section><h2>福利厚生</h2>{job_facts(benefits)}</section>
      <section id="conditions"><h2>応募条件</h2>{job_facts(conditions)}</section>
      <div class="entry-actions">{out(WORK,'最新の求人・応募受付 '+arrow,'cta')}{out(TEL,'採用担当へ電話する','under')}</div></article></div>
      <div class="wrap spread-foot">{link('job-offer','← すべての募集職種へ',frag='positions')}{link('job-offer','見学・応募 '+right,frag='entry')}</div>'''

def emit(route,title,desc,render):
    global current
    current=route
    body=header()+'<main id="main" tabindex="-1">'+render()+'</main>'+footer()
    pages[route]=(title,body)
    page_title=escape(title+'｜grace hair dressing 鷹匠')
    structured={'@context':'https://schema.org','@type':'HairSalon','name':'grace hair dressing 鷹匠','telephone':'+81-54-251-4600','address':{'@type':'PostalAddress','postalCode':'420-0839','addressRegion':'静岡県','addressLocality':'静岡市葵区','streetAddress':'鷹匠1-7-13 エスパシオ鷹匠2B','addressCountry':'JP'}}
    schema='<script type="application/ld+json">'+json.dumps(structured,ensure_ascii=False)+'</script>' if not route else ''
    html=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f8f6ef"><title>{page_title}</title><meta name="description" content="{escape(desc,quote=True)}"><meta property="og:type" content="website"><meta property="og:locale" content="ja_JP"><meta property="og:title" content="{page_title}"><meta property="og:description" content="{escape(desc,quote=True)}"><link rel="icon" href="{asset('favicon.svg')}"><link rel="stylesheet" href="{asset('salon.css')}"><script defer src="{asset('salon.js')}"></script>{schema}</head><body>{body}</body></html>'''
    dest=DIST/route/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(html)
def build():
    emit('','静岡・新静岡駅前の美容室','静岡市葵区鷹匠、新静岡セノバの鷹匠口正面。graceのヘアスタイル、料金、スタッフ、予約・アクセスのご案内。',home)
    emit('menu','メニュー・料金','カット、カラー、髪質改善、Aujuaトリートメント、ヘッドスパの料金と内容。',menu_page)
    emit('styles','ヘアスタイル','ショート、ボブ、ミディアムのスタイリング写真とオーダーのヒント。',styles)
    for i,style in enumerate(STYLE,1): emit('styles/'+style[0],style[2],style[4],lambda i=i:style_detail(i))
    emit('staff','スタッフ','grace hair dressingのスタイリストとケアリストをご紹介します。',staff)
    emit('blog','お知らせ・サロン日記','graceスタッフによるスタイル紹介や日々のサロンの記録。',journal)
    emit('contact','店舗・お問い合わせ','営業時間、最終受付、電話、オンライン予約、新静岡駅からの道順。',contact)
    emit('job-offer','採用情報','grace hair dressing 鷹匠の採用情報。職種別の募集要項と見学・応募窓口。',recruit)
    for slug,role in ROLES.items():
        emit(slug,role['name']+'の募集',role['lead'],lambda slug=slug:jobpage(slug))
if __name__=='__main__': build()
