"""横浜市「保育所等の入所状況」から最新の受入可能数・入所待ち人数CSVを取得し data.json を作る。
使い方: python3 update.py <geo.json> <出力data.json>
geo.json = 施設番号 -> {n,w,a,lat,lng,ap} の位置キャッシュ（skip:true は位置不明で除外）。未登録の施設は data.json の unlocated に出る。
"""
import sys,re,csv,io,json,html,math,urllib.request
PAGE='https://www.city.yokohama.lg.jp/kosodate-kyoiku/hoiku-yoji/shisetsu/riyou/info/nyusho-jokyo.html'
HOME=(35.449089,139.637985)  # 距離の基準点
RADIUS_KM=5.05
WARDS={'中区','西区','南区','神奈川区','保土ケ谷区','磯子区','港南区'}
def get(u): return urllib.request.urlopen(u,timeout=30).read()
t=get(PAGE).decode('utf-8','replace')
links={}
for m in re.finditer(r'<a[^>]+href="([^"]+\.csv)"[^>]*>(.*?)</a>',t,re.S):
    lab=re.sub(r'<[^>]+>|\s+','',html.unescape(m.group(2)))
    for key in ('受入可能数','入所待ち人数'):
        if key in lab and '市内全区' in lab and key not in links:
            links[key]=urllib.request.urljoin(PAGE,m.group(1))
def rows(u):
    raw=get(u)
    for enc in ('cp932','utf-8-sig'):
        try: s=raw.decode(enc); break
        except UnicodeDecodeError: pass
    r=list(csv.reader(io.StringIO(s)))
    title=r[0][0]
    return title,[x for x in r[2:] if len(x)>10 and x[3].strip()]
num=lambda a: None if a.strip() in ('-','','－') else int(a)
title,K=rows(links['受入可能数'])
_,M=rows(links['入所待ち人数'])
wait={x[3].strip():[num(a) for a in x[4:10]] for x in M}
geo=json.load(open(sys.argv[1]))
items=[];unl=[]
for x in K:
    no=x[3].strip()
    if x[0] not in WARDS: continue
    g=geo.get(no)
    if not g: unl.append(dict(no=no,w=x[0],n=x[2])); continue
    if g.get('skip'): continue
    if math.hypot((g['lng']-HOME[1])*90.8,(g['lat']-HOME[0])*111.0)>RADIUS_KM: continue
    items.append(dict(no=no,n=x[2],w=x[0],a=g.get('a',''),lat=g['lat'],lng=g['lng'],ap=g.get('ap',False),
                      v=[num(a) for a in x[4:10]],q=wait.get(no,[None]*6)))
asof=re.search(r'【(.+?)時点】',title)
upd=K[0][11] if len(K[0])>11 else ''
out=dict(asof=asof.group(1) if asof else title,updated=upd,source=PAGE,csv=links,items=items,unlocated=unl)
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False)
print(out['asof'],upd,'items',len(items),'unlocated',len(unl))
for u in unl: print('  未登録:',u['w'],u['n'],u['no'])
