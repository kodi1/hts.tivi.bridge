#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import simplejson as json
import requests
import re
from mapping import streams_map as _map_ch

headers = {
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0 Iceweasel/22.0'
            }

proxies = None
#proxies = {'http': "http://127.0.0.1:8182"}

_map_group = {
        'Възрастни': '18+',
        'Български': 'ЕФИРНИ',
        'Руски': 'ДРУГИ',
        'Немски': 'ДРУГИ',
        'Турски': 'ДРУГИ',
        'Френски': 'ДРУГИ',
        'Италиански': 'ДРУГИ',
        'Филми': 'Филмови',
        'Документални': 'Научни',
        'Спортни': 'Спортни',
        'Тематични': 'ДРУГИ',
        'Новини': 'ДРУГИ',
        'Други': 'ДРУГИ',
        'Музикални': 'Музикални',
        'Детски': 'Детски',
    }

local_map_ch = {
        'БНТ 4': {'id':'БНТ 4','group':'Български','logo': None},
        'БНТ 4 HD': {'id':'БНТ 4','group':'Български','logo': None},
        'БНТ 3 HD': {'id':'БНТ 3','group':'Български','logo': None},
        'Discovery HD': {'id':'Discovery Showcase HD', 'group':'Документални','logo':'http://logos.kodibg.org/discoveryhdshowcase.png'},
        'Fishing & Hunting HD': {'id':'Fishing &amp; Hunting', 'group':'Документални','logo':'http://logos.kodibg.org/thefishinghuntingchannel.png'},
        'ТВ Центр Международный': {'id':'ТВ Центр Международный','group':'Тематични','logo': None},
        'БНТ 3': {'id':'БНТ 3','group':'Български','logo': None},
        'B1B Action': {'id':'B1B Action','group':'Тематични','logo': None},
        'B1B Action HD': {'id':'B1B Action','group':'Тематични','logo': None},
        'Fishing & Hunting': {'id':'Fishing &amp; Hunting', 'group':'Документални','logo':'http://logos.kodibg.org/thefishinghuntingchannel.png'},
        'MM TV HD': {'id':'MM TV','group':'Музикални','logo': None},
        'Mooz Dance HD': {'id':'Mooz Dance','group':'Музикални','logo': None},
        'F.O. SD': {'id':'F.O.','group':'Тематични','logo': None},
        'Magic TV HD': {'id':'Magic TV','group':'Тематични','logo': None},
        'KiKa HD': {'id':'KiKa','group':'Тематични','logo': None},
        'RT Arabic': {'id':'RT Arabic','group':'Тематични','logo': None},
        'Sat.1': {'id':'Sat.1','group':'Тематични','logo': None},
        'ProSieben Maxx': {'id':'ProSieben Maxx','group':'Тематични','logo': None},
        'Kabel 1 Doku': {'id':'Kabel 1 Doku.','group':'Тематични','logo': None},
        'Deutsches Musik': {'id':'Deutsches Musik','group':'Музикални','logo': None},
        'Домашний Intl': {'id':'Домашний Intl','group':'Тематични','logo': None},
        'RT France HD': {'id':'RT France','group':'Тематични','logo': None},
        'UA TV (Укр)': {'id':'UA TV (Укр)','group':'Тематични','logo': None},
        'PPV 1 (demo)': {'id':'PPV 1 (demo)','group':'Филми','logo': None},
        'PPV 2 (demo)': {'id':'PPV 2 (demo)','group':'Филми','logo': None},
        'PPV 3 (demo)': {'id':'PPV 3 (demo)','group':'Филми','logo': None},
        'PPV 4 (demo)': {'id':'PPV 4 (demo)','group':'Филми','logo': None},
        'PPV 5 (demo)': {'id':'PPV 5 (demo)','group':'Филми','logo': None},
        'PPV 6 (demo)': {'id':'PPV 6 (demo)','group':'Филми','logo': None},
        'Sundance': {'id':'Sundance','group':'Музикални','logo': None},
        'TeleSur': {'id':'TeleSur','group':'Тематични','logo': None},
        'TeleSur HD': {'id':'TeleSur','group':'Тематични','logo': None},
        'RT Espagnol': {'id':'RT Espagnol','group':'Тематични','logo': None},
        'БНТ1 LQ': {'id':'БНТ 1','group':'Български','logo':'http://logos.kodibg.org/bnt1.png'},
        'bTV LQ': {'id': 'bTV','group':'Български','logo': 'http://logos.kodibg.org/btv.png'},
        'Nova LQ':{'id': 'Nova','group':'Български','logo': 'http://logos.kodibg.org/novatv.png'},
        'bTV Comedy LQ': {'id':'bTV Comedy', 'group':'Филми','logo':'http://logos.kodibg.org/btvcomedy.png'},
        'bTV Comedy HD': {'id':'bTV Comedy', 'group':'Филми','logo':'http://logos.kodibg.org/btvcomedy.png'},
        'bTV Cinema LQ': {'id':'bTV Cinema', 'group':'Филми','logo':'http://logos.kodibg.org/btvcinema.png'},
        'bTV Cinema HD': {'id':'bTV Cinema', 'group':'Филми','logo':'http://logos.kodibg.org/btvcinema.png'},
        'bTV Action LQ': {'id':'bTV Action', 'group':'Филми','logo':'http://logos.kodibg.org/btvaction.png'},
        'KinoNova LQ': {'id':'KinoNova', 'group':'Филми','logo':'http://logos.kodibg.org/kinonova.png'},
        'Diema LQ': {'id':'Diema', 'group':'Филми','logo':'http://logos.kodibg.org/diema.png'},
        'FOX Life LQ': {'id':'FOX Life', 'group':'Филми','logo':'http://logos.kodibg.org/foxlife.png'},
        'FOX Crime LQ': {'id':'FOX Crime', 'group':'Филми','logo':'http://logos.kodibg.org/foxcrime.png'},
        'FOX LQ': {'id':'FOX', 'group':'Филми','logo':'http://logos.kodibg.org/fox.png'},
        'БНТ2 LQ': {'id':'БНТ 2', 'group':'Български','logo':'http://logos.kodibg.org/bnt2.png'},
        'ТВ Европа LQ': {'id':'ТВ Европа', 'group':'Български','logo':'http://logos.kodibg.org/tveuropa.png'},
        'БНТ HD LQ': {'id':'БНТ HD', 'group':'Спортни','logo':'http://logos.kodibg.org/bnthd.png'},
        'NOVAsport LQ': {'id':'Nova Sport', 'group':'Спортни','logo':'http://logos.kodibg.org/novasport.png'},
        'RING LQ': {'id':'RING BG HD', 'group':'Спортни','logo':'http://logos.kodibg.org/ring.png'},
        'Eurosport LQ': {'id':'Eurosport HD', 'group':'Спортни','logo':'http://www.vivacom.bg/web/files/richeditor/tv/tv-channels-logos/eurosport1-logo.png'},
        'Eurosport 2 LQ': {'id':'Eurosport 2 HD', 'group':'Спортни','logo':'http://www.vivacom.bg/web/files/richeditor/tv/tv-channels-logos/eurosport2-logo.png'},
        'Discovery LQ': {'id':'Discovery Channel', 'group':'Документални','logo':'http://logos.kodibg.org/discovery.png'},
        'Animal Planet LQ': {'id':'Animal Planet', 'group':'Документални','logo':'http://logos.kodibg.org/animalplanet.png'},
        'Diema Family LQ': {'id':'Diema Family', 'group':'Филми','logo':'http://logos.kodibg.org/diemafamily.png'},
        'BTV Lady LQ': {'id':'bTV Lady', 'group':'Филми','logo':'http://logos.kodibg.org/btvlady.png'},
        '24 Kitchen LQ': {'id':'24 Kitchen', 'group':'Тематични','logo':'http://logos.kodibg.org/24kitchen.png'},
        'Nickelodeon LQ': {'id':'Nickelodeon', 'group':'Детски','logo':'http://logos.kodibg.org/nickelodeon.png'},
        'Cartoon Net LQ': {'id':'Cartoon Network', 'group':'Детски','logo':'http://logos.kodibg.org/cartoonnetwork.png'},
        'Disney LQ': {'id':'Disney Channel', 'group':'Детски','logo':'http://logos.kodibg.org/disney.png'},
        'NatGeo LQ': {'id':'National Geographic', 'group':'Документални','logo':'http://logos.kodibg.org/natgeo.png'},
        'TLC LQ': {'id':'TLC', 'group':'Филми','logo':'http://logos.kodibg.org/tlc.png'},
        'Тест 1': {'id':'Тест 1','group':'Тематични','logo': None},
        'TV1000 Русское кино': {'id':'TV1000 Русское кино','group':'Филми','logo': None},
        'ARD / Das Erste HD': {'id':'ARD / Das Erste', 'group':'Немски','logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Das_Erste_HD_Logo.svg/725px-Das_Erste_HD_Logo.svg.png'},
        'Disney DE HD': {'id':'Disney DE', 'group':'Детски','logo':'http://logos.kodibg.org/disney.png'},
        'ERT World': {'id':'ERT', 'group':'Тематични','logo':'http://img.pathfinder.gr/Pathfinder/Tv/channels/ert1.jpg?v=3'},
    }

class data():
  def __init__(self, m, host, port):
    self.__store = None
    self.__mac = m
    self.__host = host
    self.__port = port

    retry = requests.packages.urllib3.util.Retry(
                                                  total=5,
                                                  read=5,
                                                  connect=5,
                                                  backoff_factor=1,
                                                  status_forcelist=[ 502, 503, 504 ],
                                                  )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)

    self.__s = requests.Session()
    self.__s.mount('http://', adapter)
    self.__s.mount('https://', adapter)

    self.__fill_storage()

  def __fetch(self):
    _filt = re.compile(r'^#EXTINF.*group-title="(?P<group>.*?)".*ch-number="(?P<num>.*?)".*,(?P<name>.*)\n#.*\n(?P<url>.*)$', re.I|re.M)
    r = self.__s.get('http://cdn.tivi.bg/m/%s' % self.__mac)
    if r.status_code == requests.codes.ok and '#EXTM3U' == r.text[:7]:
        for m in _filt.finditer(r.text):
            yield m.group('name').encode('utf-8'), m.group('group'), m.group('num'), m.group('url').encode('utf-8')
    else:
        sys.exit('wrong responce')

  def __fill_storage(self):
      self.__store = {}
      _map_ch.update(local_map_ch)
      for n, g, ch, url in self.__fetch():
          if n in _map_ch.keys():
              group = _map_group.get(_map_ch[n]['group'], _map_ch[n]['group'])
              self.__store[ch] = {'name': n, 'group': group, 'url': url, 'id': _map_ch[n]['id'], 'logo': _map_ch[n]['logo']}
          else:
              print 'Not found %s' % n

  def get_ch(self, ch):
      #self.__fill_storage()
      _ch = self.__store.get(ch, None)
      if not _ch:
          return None
      return _ch.get('url', None)

  def get_pls(self):
    self.__fill_storage()
    _line = u'#EXTM3U\n'
    for k, v in self.__store.items():
      extinf = 'tvh-epg="off"'

      logo = v.get('logo')
      if logo:
        extinf = '%s tvg-logo="%s"' % (extinf, logo)

      tvid = v.get('id')
      if tvid:
        extinf = '%s tvg-id="%s"' % (extinf, tvid)

      tag = v.get('group')
      if tag:
        extinf = '%s tvh-tags="%s"' % (extinf, tag)

      name = v.get('name')
      if name:
        extinf = '%s,%s' % (extinf, name)
      else:
        extinf = '%s,%s' % (extinf, k)

      _line = _line + '#EXTINF:-1 %s\n' % (extinf.decode('utf-8'),)
      #_line = _line + 'http://%s:%s/id/%s\n' % (self.__host, self.__port, k)
      _line = _line + 'pipe:///usr/bin/ffmpeg -loglevel fatal -ignore_unknown -i http://%s:%s/id/%s -map 0 -c copy -metadata service_provider=tivi -metadata service_name=%s -tune zerolatency -f mpegts pipe:1\n' % (self.__host, self.__port, k, k)
    return _line.encode('utf-8')
