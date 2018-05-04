# -*- coding: utf-8 -*-
import urllib2,urllib
import re,time
import time,json,base64
import cookielib,aes,os



BASEURL='http://www.sport365.live/pl/main'
UA='Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'

def fixForEPG(item):
    return(item)


def getUrl(url,data=None,header={},useCookies=True):
    if useCookies:
        cj = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    if not header:
        header = {'User-Agent':UA}
    req = urllib2.Request(url,data,headers=header)
    try:
        response = urllib2.urlopen(req, timeout=15)
        link = response.read()
        response.close()
    except:
        link=''
    return link

def getUrlc(url,data=None,header={},useCookies=True):
    cj = cookielib.LWPCookieJar()
    if useCookies:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    if not header:
        header = {'User-Agent':UA}
    req = urllib2.Request(url,data,headers=header)
    try:
        response = urllib2.urlopen(req, timeout=15)
        link = response.read()
        response.close()
    except:
        link=''
    c = ''.join(['%s=%s'%(c.name,c.value) for c in cj]) if cj else ''
    return link,c

def getChannels(addheader=False):
    ret=''
    content = getUrl(BASEURL)
    wrapper = re.compile('(http[^"]+/advertisement.js\?\d+)').findall(content)
    wrappers = re.compile('<script type="text/javascript" src="(http://s1.medianetworkinternational.com/js/\w+.js)"').findall(content)
    for wrapper in wrappers:
        wc = getUrl(wrapper)
        content=JsUnwiser().unwiseAll(wc)
        ret = content
        ret = re.compile('return "(.*?)"').findall(content)
        if ret:
            ret = ret[0]
            print 'key %s'%ret
            break
    url='http://www.sport365.live/pl/events/-/1/-/-/120'
    content = getUrl(url)
    ids = [(a.start(), a.end()) for a in re.finditer('onClick=', content)]
    ids.append( (-1,-1) )
    out=[]
   
    for i in range(len(ids[:-1])):
        #print content[ ids[i][1]:ids[i+1][0] ]
        subset = content[ ids[i][1]:ids[i+1][0] ]
        links=re.compile('\("([^"]+)", "([^"]+)", "[^"]+", 1\)').findall(subset)
        title2=re.compile('<img alt="(.*?)"').findall(subset)
        t=re.compile('>([^<]+)<').findall(subset)
        online = '[COLOR lightgreen]•[/COLOR]' if subset.find('/images/types/dot-green-big.png')>0 else '[COLOR red]*[/COLOR]'
        if links and title2:
            event,urlenc=links[0]
            url = 'http://www.sport365.live/en/links/%s/1@%s'%(event.split('_')[-1],ret)
            etime,title1= t[:2]
            lang = t[-1]
            quality =  t[-2].replace('&nbsp;',',') if len(t)==4 else ''
            title = '%s%s: [COLOR blue]%s[/COLOR] %s'%(online,etime,title1,title2[0])
            code=quality+lang
            out.append({'title':title,'tvid':'','url':url,'group':'','urlepg':'','code':code})
    return out

def getStreams(url):
    myurl,ret=url.split('@')
    content = getUrl(myurl)
    #sources=re.compile('__showWindow\([\'"](.*?)[\'"]').findall(content)
    sources=re.compile('<span id=["\']span_link_links[\'"] onClick="\w+\(\'(.*?)\'').findall(content)
    #s=sources[0]
    out=[]
    for i, s in enumerate(sources):
        enc_data=json.loads(base64.b64decode(s))
        ciphertext = 'Salted__' + enc_data['s'].decode('hex') + base64.b64decode(enc_data['ct'])
        src=aes.decrypt(ret,base64.b64encode(ciphertext))
        src=src.strip('"').replace('\\','')
        title = 'Link %d'%(i+1)
        out.append({'title':title,'tvid':title,'key':ret,'url':src,'refurl':myurl,'urlepg':''})
    return out

# out=getChannels()
# url = out[0].get('url')
# streams = getStreams(url)
#item=streams[0]
# url=streams[0].get('url')
#item['url']=
# link='http://www.realstream.pw/player/57e8fae5c0dcd381780526/4/13/57e9650473aff/AKBarsKazan-DinamoMinsk/768/432'
def getChannelVideo(item):
    content = getUrl(item.get('url'),useCookies=True)
    links=re.compile('(http://www.[^\.]+.pw/(?!&#)[^"]+)', re.IGNORECASE + re.DOTALL + re.MULTILINE + re.UNICODE).findall(content)
    link = [x for x in links if '&#' in x] 
    if link:
        link=re.sub(r'&#(\d+);', lambda x: chr(int(x.group(1))), link[0])
        header = {'User-Agent':UA,
                  'Referer':item.get('url')}
        data = getUrl(link,header=header,useCookies=True)
        f=re.compile('.*?name="f"\s*value=["\']([^"\']+)["\']').findall(data)
        d=re.compile('.*?name="d"\s*value=["\']([^"\']+)["\']').findall(data)
        r=re.compile('.*?name="r"\s*value=["\']([^"\']+)["\']').findall(data)
        action=re.compile('[\'"]action[\'"][,\s]*[\'"](http.*?)[\'"]').findall(data)
        srcs=re.compile('src=[\'"](.*?)[\'"]').findall(data)
        if f and r and d and action:
            payload=urllib.urlencode({'d':d[0],'f':f[0],'r':r[0]})
            data2,c= getUrlc(action[0],payload,header=header,useCookies=True)
            link=re.compile('\([\'"][^"\']+[\'"], [\'"][^"\']+[\'"], [\'"]([^"\']+)[\'"], 1\)').findall(data2)
            enc_data=json.loads(base64.b64decode(link[0]))
            ciphertext = 'Salted__' + enc_data['s'].decode('hex') + base64.b64decode(enc_data['ct'])
            src=aes.decrypt(item.get('key'),base64.b64encode(ciphertext))
            src=src.replace('"','').replace('\\','').encode('utf-8')
            a,c=getUrlc(srcs[-1],header=header,useCookies=True) if srcs else '',''
            a,c=getUrlc(src,header=header,useCookies=True)
            # print a
            if src.startswith('http'):
                href =src+'|Referer=%s&User-Agent=%s&X-Requested-With=ShockwaveFlash/22.0.0.209'%(urllib.quote(action[0]),UA)
                #href =src+'|Referer=%s&User-Agent=%s'%(urllib.quote(action[0]),UA)
                #href = src
                print href
                return href,srcs[-1],header
            else:
                href=aes.decode_hls(src)
                if href:
                    href +='|Referer=%s&User-Agent=%s&X-Requested-With=ShockwaveFlash/22.0.0.209'%(urllib.quote(r[0]),UA)
                    return href,srcs[-1],header
    return ''

# getUrlrh(src)

def getUrlrh(url,data=None,header={},useCookies=True):
    cj = cookielib.LWPCookieJar()
    if useCookies:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    if not header:
        header = {'User-Agent':UA}
    rh={}
    req = urllib2.Request(url,data,headers=header)
    try:
        response = urllib2.urlopen(req, timeout=15)
        for k in response.headers.keys(): rh[k]=response.headers[k]
        link = response.read()
        response.close()
    except:
        link=''
    c = ''.join(['%s=%s'%(c.name,c.value) for c in cj]) if cj else ''
    return link,rh



class JsUnwiser:
    def unwiseAll(self, data):
        try:
            in_data=data
            sPattern = 'eval\\(function\\(w,i,s,e\\).*?}\\((.*?)\\)'
            wise_data=re.compile(sPattern).findall(in_data)
            for wise_val in wise_data:
                unpack_val=self.unwise(wise_val)
                #print '\nunpack_val',unpack_val
                in_data=in_data.replace(wise_val,unpack_val)
            return re.sub(re.compile("eval\(function\(w,i,s,e\).*?join\(''\);}", re.DOTALL), "", in_data, count=1)
        except: 
            traceback.print_exc(file=sys.stdout)
            return data
        
    def containsWise(self, data):
        return 'w,i,s,e' in data
        
    def unwise(self, sJavascript):
        #print 'sJavascript',sJavascript
        page_value=""
        try:        
            ss="w,i,s,e=("+sJavascript+')' 
            exec (ss)
            page_value=self.__unpack(w,i,s,e)
        except: traceback.print_exc(file=sys.stdout)
        return page_value
        
    def __unpack( self,w, i, s, e):
        lIll = 0;
        ll1I = 0;
        Il1l = 0;
        ll1l = [];
        l1lI = [];
        while True:
            if (lIll < 5):
                l1lI.append(w[lIll])
            elif (lIll < len(w)):
                ll1l.append(w[lIll]);
            lIll+=1;
            if (ll1I < 5):
                l1lI.append(i[ll1I])
            elif (ll1I < len(i)):
                ll1l.append(i[ll1I])
            ll1I+=1;
            if (Il1l < 5):
                l1lI.append(s[Il1l])
            elif (Il1l < len(s)):
                ll1l.append(s[Il1l]);
            Il1l+=1;
            if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
                break;
            
        lI1l = ''.join(ll1l)#.join('');
        I1lI = ''.join(l1lI)#.join('');
        ll1I = 0;
        l1ll = [];
        for lIll in range(0,len(ll1l),2):
            #print 'array i',lIll,len(ll1l)
            ll11 = -1;
            if ( ord(I1lI[ll1I]) % 2):
                ll11 = 1;
            #print 'val is ', lI1l[lIll: lIll+2]
            l1ll.append(chr(    int(lI1l[lIll: lIll+2], 36) - ll11));
            ll1I+=1;
            if (ll1I >= len(l1lI)):
                ll1I = 0;
        ret=''.join(l1ll)
        if 'eval(function(w,i,s,e)' in ret:
            ret=re.compile('eval\(function\(w,i,s,e\).*}\((.*?)\)').findall(ret)[0] 
            return self.unwise(ret)
        else:
            return ret
