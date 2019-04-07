from app import db
from datetime import datetime
from app.models import Bing
import requests
import urllib
import json


def restore_bing_wallpapers():
    cookies = "SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=13DD9DD96C29405A80C6CDC936783ED9&dmnchg=1; _EDGE_V=1; MUID=1AF657053B94627F322F5B393ABB63E9; MUIDB=1AF657053B94627F322F5B393ABB63E9; BFBN=gRBFUDVu9A4J7pPjXUeT-ezT31YMdh0GS7lTTE5suCZAZw; ANON=A=8AC4A7383D0B3CA8FF579218FFFFFFFF&E=15ac&W=1; NAP=V=1.9&E=1552&C=h6GnnSffsZ-Ql34Rx5NZx-mRP3JCnBKR1YaJ0yCAX9sqf4mxI9KyTQ&W=1; ENSEARCH=BENVER=1; SRCHUSR=DOB=20180730&T=1538107234000; _EDGE_S=SID=2FF3F9A75F98669E0B50F5DF5EB667A6; _UR=MC=1; ipv6=hit=1538116466060&t=4; undefined=undefined=undefined; ULC=P=16A92|139:@39&H=16A92|139:39&T=16A92|139:39:7; _SS=SID=2FF3F9A75F98669E0B50F5DF5EB667A6&bIm=311413&HV=1538112880; SRCHHPGUSR=CW=150&CH=931&DPR=1.25&UTC=480&WTS=63673709657"
    headers = {
        "Host": "cn.bing.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Contebt-Type": "application/json",
        'Cookie': cookies
    }

    params = urllib.parse.urlencode({
        'format': 'js',
        'idx': -1,
        'n': 8,
        'pid': 'hp',
        'mkt': 'en-US'
    })
    req = requests.get(
        'https://cn.bing.com/HPImageArchive.aspx', headers=headers, params=params)
    data = ''
    if req.status_code == 200:
        data = req.text
    all = json.loads(data)
    if all:
        bings = all['images']
        for item in bings:
            try:
                startdate = datetime.strptime(
                    item['fullstartdate'], '%Y%m%d%H%M%S')
                url = 'https://cn.bing.com' + item['url']
                urlbase = 'https://cn.bing.com' + item['urlbase']
                copyright = item['copyright']
                title = item['title']
                caption = item['caption']
                desc = item['desc']
                hsh = item['hsh']

                model = Bing(hsh=hsh, datetime=startdate, url=url,
                             urlbase=urlbase, copyright=copyright,
                             title=title, caption=caption, description=desc)
                has = Bing.query.filter_by(hsh=model.hsh).first()
                if has is None:
                    print(model.hsh)
                    db.session.add(model)
            except Exception as e:
                print(e)
                continue
        db.session.commit()
