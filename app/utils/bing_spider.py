from app import db, log
from datetime import datetime
from app.models import Bing
import requests
import urllib
import json

USER_AGENG = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
COOKIES = "SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=550985DA3A594E778D50B0672C8B7B3C&dmnchg=1; _EDGE_V=1; MUID=1229F3F5A56B69751C77FE63A41468D4; MUIDB=1229F3F5A56B69751C77FE63A41468D4; ENSEARCH=BENVER=1; SerpPWA=reg=1; MSCC=1; MSTC=ST=1; _tarLang=default=zh-Hans; _EDGE_S=mkt=zh-cn&SID=2FDB4EA865B263983FA74332649C62ED; _FP=hta=on; ULC=P=1175F|7:3&H=1175F|7:3&T=1175F|7:3; ipv6=hit=1563175374895&t=4; SRCHHPGUSR=CW=1920&CH=947&DPR=1&UTC=480&WTS=63698768573; SRCHUSR=DOB=20190711&T=1563171781000; _SS=SID=2FDB4EA865B263983FA74332649C62ED&HV=1563171782&bIm=208"


def spider():
    headers = {
        "Host": "cn.bing.com",
        "User-Agent": USER_AGENG,
        'Cookie': COOKIES
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
    if req.status_code == 200:
        data = json.loads(req.text)
        bings = data.get('images', None)
        for item in bings:
            try:
                startdate = datetime.strptime(
                    item.get('fullstartdate', datetime.utcnow()), '%Y%m%d%H%M%S')
                url = 'https://cn.bing.com' + item.get('url', None)
                urlbase = 'https://cn.bing.com' + item.get('urlbase', None)
                copyright = item.get('copyright', None)
                title = item.get('title', None)
                caption = item.get('caption', None)
                desc = item.get('desc', None)
                hsh = item.get('hsh', None)

                model = Bing(hsh=hsh, pub_date=startdate, url=url,
                             urlbase=urlbase, copyright=copyright,
                             title=title, caption=caption, description=desc)
                has = Bing.query.filter_by(pub_date=model.pub_date).first()
                if has is None:
                    log.logger.debug(model.pub_date)
                    db.session.add(model)
            except Exception as e:
                log.logger.critical(e)
                db.session.rollback()
                continue
        db.session.commit()
