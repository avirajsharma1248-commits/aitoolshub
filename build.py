import os,re,sys,json,shutil
CSS="""
:root{--bg:#f6f6fb;--card:#fff;--ink:#17173a;--mute:#5b5b7a;--line:#dcdcec;--acc:#4338ca;--acc2:#e0e7ff;--r:10px}
:root[data-theme=dark]{--bg:#12122a;--card:#1b1b3a;--ink:#ececff;--mute:#a4a4c8;--line:#31315c;--acc:#a5b4fc;--acc2:#2a2a5c}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#12122a;--card:#1b1b3a;--ink:#ececff;--mute:#a4a4c8;--line:#31315c;--acc:#a5b4fc;--acc2:#2a2a5c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 "Avenir Next",Avenir,"Segoe UI",system-ui,sans-serif}
a{color:var(--acc)}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--acc);outline-offset:2px}
.w{max-width:1040px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);background:var(--card)}
header .w{display:flex;flex-wrap:wrap;gap:12px 22px;align-items:center;padding-top:12px;padding-bottom:12px}
.logo{font-weight:800;font-size:1.25rem;color:var(--ink);text-decoration:none;letter-spacing:-.02em}
nav{display:flex;flex-wrap:wrap;gap:4px 16px;flex:1}nav a{color:var(--mute);text-decoration:none;font-size:.95rem}nav a:hover,nav a[aria-current]{color:var(--ink);text-decoration:underline}
button.t{border:1px solid var(--line);background:none;color:var(--ink);border-radius:var(--r);padding:6px 12px;cursor:pointer;font:inherit;font-size:.9rem}
.hero{padding:64px 0 36px}.hero h1{font-size:clamp(2.2rem,6vw,3.8rem);line-height:1.05;letter-spacing:-.03em;margin:0 0 14px;max-width:16ch}
.hero p{color:var(--mute);max-width:56ch;margin:0 0 22px}
h1{letter-spacing:-.02em}h2{margin:36px 0 12px;letter-spacing:-.01em}
.s{width:100%;max-width:520px;padding:12px 14px;border:1px solid var(--line);border-radius:var(--r);background:var(--card);color:var(--ink);font:inherit}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;padding:0;list-style:none}
.c{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:16px}
.c h3{margin:0 0 4px;font-size:1.05rem}.c p{margin:0 0 10px;color:var(--mute);font-size:.95rem}
.tag{display:inline-block;background:var(--acc2);color:var(--acc);border-radius:99px;padding:1px 10px;font-size:.8rem;margin:0 4px 4px 0}
.cats{display:flex;flex-wrap:wrap;gap:10px}.cats a{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:8px 14px;text-decoration:none;color:var(--ink)}
.cats a:hover{border-color:var(--acc)}
table{border-collapse:collapse;width:100%;background:var(--card)}th,td{border:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}
.x{overflow-x:auto}main{padding-bottom:50px}.note{color:var(--mute);font-size:.9rem}
footer{border-top:1px solid var(--line);padding:24px 0;color:var(--mute);font-size:.9rem}
.hide{display:none}
"""
JS="""
(function(){var r=document.documentElement,s;try{s=localStorage.getItem('theme')}catch(e){}if(s)r.dataset.theme=s;
document.addEventListener('DOMContentLoaded',function(){
var b=document.getElementById('theme');if(b)b.onclick=function(){var d=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;
r.dataset.theme=d?'light':'dark';try{localStorage.setItem('theme',r.dataset.theme)}catch(e){}};
var q=document.getElementById('q');if(q)q.addEventListener('input',function(){var v=q.value.toLowerCase().trim(),n=0;
document.querySelectorAll('#list>li').forEach(function(li){var m=li.textContent.toLowerCase().indexOf(v)>-1;li.classList.toggle('hide',!m);if(m)n++});
document.getElementById('none').classList.toggle('hide',n>0)})})})();
"""
CSS+=".prose{max-width:68ch}.prose li{margin:6px 0}.meta{color:var(--mute);font-size:.9rem}footer a{color:var(--mute)}.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}"
BASE=(sys.argv[1] if len(sys.argv)>1 else os.environ.get("SITE_URL","https://YOUR-USERNAME.github.io/YOUR-REPOSITORY")).rstrip("/")
MAIL=sys.argv[2] if len(sys.argv)>2 else "your-email@YOUR-DOMAIN"
SITE="AIToolsHub"; TODAY="2026-10-04"
D=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(D,"site")
AFF={}  # tool name -> your affiliate URL; only these links get rel="sponsored"
T=[("ChatGPT","https://chatgpt.com","General assistant for writing, research, coding and analysis.","writing coding students free productivity money"),
("Claude","https://claude.ai","Assistant strong at long documents, careful writing and coding.","writing coding students free productivity"),
("Gemini","https://gemini.google.com","Google's assistant, connected to Search, Docs and Gmail.","writing students free productivity"),
("Perplexity","https://perplexity.ai","Answer engine that cites its sources, good for research.","students free productivity"),
("Midjourney","https://midjourney.com","High-quality artistic image generation.","image money"),
("Adobe Firefly","https://firefly.adobe.com","Image generation built into Adobe's creative tools.","image free"),
("Canva Magic Studio","https://canva.com","Design, presentations and AI image tools in one editor.","image students free money"),
("Runway","https://runwayml.com","Text and image to video, plus video editing tools.","video"),
("Pika","https://pika.art","Short AI video clips from text or images.","video free"),
("Synthesia","https://synthesia.io","Talking-avatar videos for training and explainers.","video money"),
("Jasper","https://jasper.ai","Marketing copy and brand-voice content for teams.","writing money"),
("Grammarly","https://grammarly.com","Grammar, tone and rewriting help as you type.","writing students free"),
("Notion AI","https://notion.com","Notes, docs and summaries inside your workspace.","productivity students"),
("Otter.ai","https://otter.ai","Meeting and lecture transcription with summaries.","productivity students free"),
("Cursor","https://cursor.com","Code editor with an AI assistant that edits your project.","coding"),
("GitHub Copilot","https://github.com/features/copilot","Code completion and chat inside your editor.","coding students"),
("Replit","https://replit.com","Build and host apps from a prompt in the browser.","coding money free"),
("Zapier","https://zapier.com","Connect apps and automate tasks with AI-built workflows.","productivity money")]
VER="Answers can be wrong, so verify important facts"
R={"ChatGPT":(["Chat, writing and analysis","Coding help","Upload files and images","Mobile and desktop apps"],["Handles many kinds of tasks","Large ecosystem of add-ons"],[VER,"Free plan has usage limits"],"Everyday tasks, drafting and learning",["Claude","Gemini","Perplexity"]),
"Claude":(["Reads and summarizes long documents","Writing and editing","Coding help","Upload files and images"],["Handles long inputs well","Clear, measured writing"],[VER,"Free plan has usage limits"],"Long documents, careful writing and coding",["ChatGPT","Gemini","Perplexity"]),
"Gemini":(["Chat and writing","Works with Google apps","Upload files and images"],["Fits people who live in Google Workspace","Easy to start with a Google account"],["Features can vary by plan and region",VER],"Google Docs, Gmail and Search users",["ChatGPT","Claude","Perplexity"]),
"Perplexity":(["Answers with source links","Follow-up questions","Research-focused search"],["Easy to check sources","Quick for research"],["Sources still need checking","Less suited to long creative writing"],"Research and fact-finding",["ChatGPT","Gemini","Claude"]),
"Midjourney":(["Text-to-image generation","Distinctive artistic style","Variation and style controls"],["Strong, recognizable image quality"],["Prompting takes practice","Check current access and plans on the official site"],"Artwork, concepts and mood boards",["Adobe Firefly","Canva Magic Studio"]),
"Runway":(["Text and image to video","Video editing tools","Motion and style controls"],["Broad set of video tools"],["Generation uses credits","Clips are short and results vary"],"Short clips and creative video experiments",["Pika","Synthesia"])}
slug=lambda n:re.sub(r"[^a-z0-9]+","-",n.lower()).strip("-")
CATS=[("ai-tools","All AI Tools","","Every tool we cover, in one searchable list."),("ai-tools-for-students","AI Tools for Students","students","Tools for studying, writing essays, and taking notes."),("ai-video-generators","AI Video Generators","video","Create clips and explainer videos from text or images."),("ai-image-generators","AI Image Generators","image","Generate images, designs and graphics from prompts."),("ai-writing-tools","AI Writing Tools","writing","Draft, edit and polish writing faster."),("ai-coding-tools","AI Coding Tools","coding","Assistants and editors that help you write software."),("free-ai-tools","Free AI Tools","free","Tools with a free plan. Check each site for current limits."),("ai-tools-to-make-money","AI Tools to Make Money","money","Tools freelancers and small businesses use to earn.")]
NAV=[("ai-tools","Tools"),("ai-tools-for-students","Students"),("free-ai-tools","Free"),("chatgpt-vs-claude","ChatGPT vs Claude"),("tutorials","Tutorials"),("reviews","Reviews"),("blog","Blog")]
FOOT=[("about","About"),("contact","Contact"),("privacy-policy","Privacy Policy"),("terms","Terms")]
POSTS=[("best-free-ai-tools","Best Free AI Tools","free","Free plans are a good way to try AI tools before paying. Limits change often, so confirm them on each tool's site."),("best-ai-tools-for-students","Best AI Tools for Students","students","These tools help with studying, note-taking and writing. Use them to learn faster, and follow your school's rules on AI use."),("best-ai-video-generators","Best AI Video Generators","video","AI video tools turn text or images into short clips or explainer videos. Test with a short project first, since generation can use credits."),("chatgpt-alternatives","ChatGPT Alternatives","writing","If ChatGPT isn't the right fit, these tools cover writing and everyday assistant tasks in different ways.")]
FAV="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%234338ca'/%3E%3Ctext x='16' y='22' font-size='16' text-anchor='middle' fill='white' font-family='sans-serif' font-weight='700'%3EAI%3C/text%3E%3C/svg%3E"
def tlink(t):
    n=t[0]; return f'<a href="{AFF.get(n,t[1])}" rel="{"sponsored " if n in AFF else ""}noopener" target="_blank">Official site</a>'
def card(t):
    n,u,d,tags=t
    tg="".join(f'<span class="tag">{x}</span>' for x in tags.split())
    rv=f' <a href="@@reviews/{slug(n)}/index.html">Read review</a>' if n in R else ""
    return f'<li class="c"><h3>{n}</h3><p>{d}</p>{tg}<br>{tlink(t)}{rv}</li>'
def grid(ts):
    return '<p><input class="s" id="q" type="search" placeholder="Search tools, e.g. video, coding, free" aria-label="Search tools"></p><ul class="g" id="list">'+"".join(card(t) for t in ts)+'</ul><p id="none" class="hide">No tools match. Try a shorter word like "video" or "free".</p>'
PAGES=[]
def page(path,title,desc,body,cur="",ld=None,err=False):
    parts=[p for p in path.split("/") if p]; root=BASE+"/" if err else ("../"*len(parts) or "./")
    nav="".join(f'<a href="{root}{h}/index.html"{" aria-current=page" if h==cur else ""}>{l}</a>' for h,l in NAV)
    foot=" · ".join(f'<a href="{root}{h}/index.html">{l}</a>' for h,l in FOOT)
    url=f"{BASE}/{path}/" if path else f"{BASE}/"
    cr=[("Home",f"{BASE}/")]
    if len(parts)==2: cr.append((parts[0].title(),f"{BASE}/{parts[0]}/"))
    if parts: cr.append((title,url))
    g=[{"@type":"WebSite","name":SITE,"url":url}] if not parts else [{"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":u} for i,(n,u) in enumerate(cr)]}]
    if ld: g.append(ld)
    jl=json.dumps({"@context":"https://schema.org","@graph":g})
    body=body.replace("@@",root); full=f"{title} | {SITE}"
    html=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><link rel="icon" href="{FAV}">
<meta property="og:title" content="{full}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website"><meta property="og:url" content="{url}"><meta property="og:site_name" content="{SITE}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{full}"><meta name="twitter:description" content="{desc}">
<script type="application/ld+json">{jl}</script><style>{CSS}</style><script>{JS}</script></head><body>
<header><div class="w"><a class="logo" href="{root}index.html">{SITE}</a><nav aria-label="Main">{nav}</nav><button class="t" id="theme" type="button">Light / dark</button></div></header>
<main class="w">{body}</main>
<footer><div class="w"><p>{foot}</p><p>Disclosure: if a link is an affiliate link, we may earn a commission at no extra cost to you. Plans and features change, so check each tool's site. <a href="{root}about/index.html">How we work</a>.</p></div></footer></body></html>"""
    if err: p=os.path.join(OUT,"404.html")
    else:
        os.makedirs(os.path.join(OUT,*parts),exist_ok=True); p=os.path.join(OUT,*parts,"index.html"); PAGES.append(path)
    open(p,"w").write(html)
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
cats='<div class="cats">'+"".join(f'<a href="@@{s}/index.html">{n}</a>' for s,n,_,_ in CATS[1:])+'</div>'
posts=lambda:'<ul class="g">'+"".join(f'<li class="c"><h3><a href="@@blog/{s}/index.html">{t}</a></h3><p>{i}</p></li>' for s,t,_,i in POSTS)+'</ul>'
page("","Find the right AI tool","Reviews, comparisons and guides to AI tools for students, creators, developers and freelancers.",
 f'<section class="hero"><h1>Find the right AI tool for the job</h1><p>Plain-language guides to AI tools for writing, images, video, coding and study. Search the list or start with a category.</p></section><h2>Browse by need</h2>{cats}<h2>All tools</h2>{grid(T)}<h2>Latest guides</h2>{posts()}')
for s,n,tag,d in CATS:
    page(s,n,d,f"<h1>{n}</h1><p class=note>{d}</p>{grid([t for t in T if not tag or tag in t[3].split()])}",s)
cmp=[("Best known for","Wide range of tasks, large tool ecosystem","Long documents, careful writing, coding"),("Writing style","Versatile, can be tuned with prompts","Often more measured and detailed"),("Coding","Strong general coding help","Strong coding help, popular with developers"),("Web search","Available in the app","Available in the app"),("Free plan","Yes, with limits","Yes, with limits")]
rows="".join(f"<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>" for a,b,c in cmp)
page("chatgpt-vs-claude","ChatGPT vs Claude","A practical comparison of ChatGPT and Claude for writing, coding and everyday use.",f'<h1>ChatGPT vs Claude</h1><p>Both are capable assistants and both improve often. Try the same prompt in each and keep the one whose answers you prefer.</p><div class="x"><table><tr><th></th><th><a href="@@reviews/chatgpt/index.html">ChatGPT</a></th><th><a href="@@reviews/claude/index.html">Claude</a></th></tr>{rows}</table></div><p class="note">Features and limits change. Verify on each product\'s site before choosing a paid plan.</p>',"chatgpt-vs-claude")
def lst(path,title,desc,items):
    page(path,title,desc,f'<h1>{title}</h1><p class=note>{desc}</p><ul class="g">'+"".join(f'<li class="c"><h3>{a}</h3><p>{b}</p></li>' for a,b in items)+'</ul>',path)
lst("tutorials","AI Tutorials and Prompts","Copy-ready prompts you can adapt.",[("Summarize a lecture","Prompt: Summarize these notes in 10 bullets, then list 5 questions I should be able to answer."),("Rewrite for clarity","Prompt: Rewrite this paragraph in plain language at a grade 9 reading level. Keep the meaning."),("Debug code","Prompt: Here is my code and the error. Explain the cause first, then show the smallest fix."),("Plan a study week","Prompt: I have 3 exams in 14 days. Build a daily plan with 2-hour blocks and review days.")])
page("reviews","AI Tool Reviews","Reviews of popular AI tools: features, pros, cons, pricing and who each suits.","<h1>AI Tool Reviews</h1><ul class=\"g\">"+"".join(f'<li class="c"><h3><a href="@@reviews/{slug(n)}/index.html">{n} review</a></h3><p>{next(t[2] for t in T if t[0]==n)}</p></li>' for n in R)+"</ul>","reviews")
for n,(feat,pro,con,best,alts) in R.items():
    t=next(x for x in T if x[0]==n); li=lambda a:"<ul>"+"".join(f"<li>{x}</li>" for x in a)+"</ul>"
    al=", ".join(f'<a href="@@reviews/{slug(a)}/index.html">{a}</a>' if a in R else a for a in alts)
    page(f"reviews/{slug(n)}",f"{n} Review",f"{n} review: what it does, features, pros, cons, pricing, free plan and best uses.",
     f'<article class="prose"><h1>{n} review</h1><p class="meta">Last updated: {TODAY}</p><h2>What is it?</h2><p>{t[2]}</p><h2>Features</h2>{li(feat)}<div class="two"><div><h2>Pros</h2>{li(pro)}</div><div><h2>Cons</h2>{li(con)}</div></div><h2>Pricing and free plan</h2><p>Pricing and free limits change often. See the official site for current plans.</p><h2>Best for</h2><p>{best}.</p><h2>Alternatives</h2><p>{al}</p><h2>Hands-on notes</h2><p>Our own test results and screenshots for {n} will be added here.</p><p>{tlink(t)}</p></article>',"reviews")
page("blog","Blog","Guides on choosing and using AI tools.",f"<h1>Blog</h1>{posts()}","blog")
for s,t,tag,intro in POSTS:
    ts=[x for x in T if tag in x[3].split() and not(s=="chatgpt-alternatives" and x[0]=="ChatGPT")]
    items="".join(f'<li><strong>{x[0]}</strong>: {x[2]} {tlink(x)}'+(f' · <a href="@@reviews/{slug(x[0])}/index.html">Review</a>' if x[0] in R else "")+"</li>" for x in ts)
    page(f"blog/{s}",t,f"{t}: a short guide with what each tool does and how to choose.",f'<article class="prose"><h1>{t}</h1><p class="meta">Last updated: {TODAY}</p><p>{intro}</p><ol>{items}</ol><h2>How to choose</h2><p>Pick the job first, such as research, writing or video. Try two tools on the same task and compare the results. Start on a free plan if one is offered, and check the official site for current pricing before you pay.</p></article>',"blog",{"@type":"BlogPosting","headline":t,"datePublished":TODAY,"dateModified":TODAY,"author":{"@type":"Organization","name":SITE},"mainEntityOfPage":f"{BASE}/blog/{s}/"})
page("about","About","How AIToolsHub picks, describes and updates AI tool listings.",f'<article class="prose"><h1>About {SITE}</h1><p>{SITE} helps people find AI tools for writing, images, video, coding and study.</p><h2>How we work</h2><p>We describe what each tool does, list its strengths and limits, and link to the official site. Pages show a last-updated date. Where we have tested a tool ourselves, we say so.</p><h2>Affiliate disclosure</h2><p>Some links may be affiliate links. If you buy through one, we may earn a commission at no extra cost to you. Affiliate links are marked as sponsored in the page code.</p><h2>Corrections</h2><p>Spot something outdated? <a href="@@contact/index.html">Tell us</a> and we will fix it.</p></article>')
page("contact","Contact","Contact AIToolsHub for corrections, tool submissions, advertising and partnerships.",f'<article class="prose"><h1>Contact</h1><p>Email: <a href="mailto:{MAIL}">{MAIL}</a></p><ul><li>Corrections and outdated information</li><li>Tool submissions</li><li>Advertising and sponsored reviews</li><li>Affiliate partnerships</li></ul></article>')
page("privacy-policy","Privacy Policy","How AIToolsHub handles visitor data.",f'<article class="prose"><h1>Privacy Policy</h1><p class="meta">Last updated: {TODAY}</p><p>This site does not ask for accounts or personal details. Your light or dark mode choice is saved in your own browser and is not sent to us.</p><p>The site is hosted by a third party, which may keep standard server logs such as IP address and pages requested. Links to other sites are governed by their own privacy policies.</p><p>If we add analytics, ads or a newsletter, we will update this page to say what is collected and why. Questions: <a href="@@contact/index.html">Contact</a>.</p></article>')
page("terms","Terms","Terms of use for AIToolsHub.",f'<article class="prose"><h1>Terms of Use</h1><p class="meta">Last updated: {TODAY}</p><p>Content on {SITE} is general information, not professional advice. Tool features, plans and prices change, so check the official site before you decide or pay.</p><p>We do our best to keep pages accurate but give no guarantee. We are not responsible for third-party sites we link to.</p></article>')
page("404","Page not found","The page you asked for does not exist.",f'<h1>Page not found</h1><p>Try the <a href="@@index.html">homepage</a> or <a href="@@ai-tools/index.html">all tools</a>.</p>',err=True)
open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{BASE}/{p}{'/' if p else ''}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)+"</urlset>")
open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
open(os.path.join(OUT,".nojekyll"),"w").write("")
print("built",len(PAGES),"pages for",BASE)
