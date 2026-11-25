"""Read Oracle's published roadmap object as data, without executing JavaScript.

Usage: python3 scripts/read_roadmap.py --source-file snapshot.js --output data.json
Omit --source-file to retrieve the current page and discover its data script.
"""
import argparse, ast, hashlib, json, re, urllib.parse, urllib.request
from pathlib import Path

PAGE='https://www.java.com/en/jre-jdk-cryptoroadmap.html'
TOKEN=re.compile(r'\s+|//[^\n\r]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|[A-Za-z_$][\w$]*|-?\d+(?:\.\d+)?|[{}\[\]:,]',re.M)

def parse_object(script):
    start=re.search(r'\bvar\s+roadmap\s*=\s*',script)
    if not start:raise ValueError('Oracle roadmap object not found; review source schema.')
    pos=start.end()
    def token():
        nonlocal pos
        while True:
            m=TOKEN.match(script,pos)
            if not m:raise ValueError(f'Unsupported source syntax near offset {pos}')
            pos=m.end();v=m[0]
            if not v.isspace() and not v.startswith(('//','/*')):return v
    look=token()
    def take(expected=None):
        nonlocal look
        value=look
        if expected is not None and value!=expected:raise ValueError(f'Expected {expected}, got {value}')
        # Stop at the end of the outer object; the remaining script is never run.
        look=token() if pos<len(script) and not (value=='}' and depth[0]==0) else None
        return value
    depth=[0]
    def value():
        nonlocal look
        if look=='{':
            depth[0]+=1;take('{');obj={}
            while look!='}':
                key=take();key=json.loads(key) if key.startswith('"') else ast.literal_eval(key) if key.startswith("'") else key
                take(':');obj[key]=value()
                if look!=',':break
                take(',')
            depth[0]-=1;take('}');return obj
        if look=='[':
            take('[');arr=[]
            while look!=']':
                arr.append(value())
                if look!=',':break
                take(',')
            take(']');return arr
        v=take()
        if v.startswith('"'):return json.loads(v)
        if v.startswith("'"):return ast.literal_eval(v)
        if re.fullmatch(r'-?\d+(?:\.\d+)?',v):return float(v) if '.' in v else int(v)
        if v in ['true','false','null']:return {'true':True,'false':False,'null':None}[v]
        raise ValueError(f'Non-data expression rejected: {v}')
    result=value()
    if not isinstance(result,dict) or not all(isinstance(result.get(k),list) for k in ('roadmap','completed')):
        raise ValueError('Expected roadmap and completed arrays; review source schema.')
    return result

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    with urllib.request.urlopen(req,timeout=60) as response:return response.read()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-file');p.add_argument('--output',required=True);args=p.parse_args()
    source_url=None
    if args.source_file:raw=Path(args.source_file).read_bytes()
    else:
        html=fetch(PAGE).decode('utf-8')
        paths=re.findall(r'<script\b[^>]*src=["\x27]([^"\x27]+)',html,re.I)
        candidates=[urllib.parse.urljoin(PAGE,v) for v in paths if 'cryptrmap' in v]
        if len(candidates)!=1:raise ValueError('Roadmap data script changed; inspect official page before continuing.')
        source_url=candidates[0];raw=fetch(source_url)
    data=parse_object(raw.decode('utf-8-sig'))
    result={'source_page':PAGE,'data_script':source_url,'source_sha256':hashlib.sha256(raw).hexdigest(),'roadmap':data}
    Path(args.output).write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'last_updated':data['lastUpdate'],'released_rows':len(data['completed']),'planned_rows':len(data['roadmap'])}))

if __name__=='__main__':main()
