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
        'За възрастни': '18+',
        'Възрастни': '18+',
        'Политематични': 'Други',
        'Лайфстайл': 'Други',
        'Руски': 'Други',
        'Кино': 'Филмови',
        'Филми': 'Филмови',
        'Документални': 'Научни',
        'Спорт': 'Спортни',
        'Музика': 'Музикални',
        'Детски': 'Детски',
        'За ниска скорост': 'Lq',
        'Информационни': 'Други',
        'Култура': 'Други',
        'Свободни': 'Други',
        'Български': 'Други',
        'Новини': 'Други',
        'Френски': 'Други',
        'Италиански': 'Други',
        'Немски': 'Други',
        'Турски': 'Други',
        'Тематични': 'Други',
    }

local_map_ch = {
        'БНТ 4': {'id':'БНТ 4','group':'Български','logo': None},
        'БНТ 4 HD': {'id':'БНТ 4','group':'Български','logo': None},
        'БНТ 3 HD': {'id':'БНТ 3','group':'Български','logo': None},
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
        'TLC LQ': {'id':'TLC', 'group':'Филми','logo':'http://logos.kodibg.org/tlc.png'},
        'Тест 1': {'id':'Тест 1','group':'Тематични','logo': None},
        'TV1000 Русское кино': {'id':'TV1000 Русское кино','group':'Филми','logo': None},
        'ARD / Das Erste HD': {'id':'ARD / Das Erste', 'group':'Немски','logo':'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Das_Erste_HD_Logo.svg/725px-Das_Erste_HD_Logo.svg.png'},
        'Disney DE HD': {'id':'Disney DE', 'group':'Детски','logo':'http://logos.kodibg.org/disney.png'},
        'ERT World': {'id':'ERT', 'group':'Тематични','logo':'http://img.pathfinder.gr/Pathfinder/Tv/channels/ert1.jpg?v=3'},
        'Nova News': {'id':'Nova News', 'group':'Информационни','logo':'http://box.tivi.bg/logo/153x153/novanews.png'},
        'Star Life': {'id':'Star Life', 'group':'Други','logo': None},
        'Star Crime': {'id':'Star Life', 'group':'Други','logo': None},
        'Star Channel': {'id':'Star Life', 'group':'Други','logo': None},
        'Bulgaria on Air HD': {'id':'Bulgaria on Air', 'group':'Информационни','logo':'http://box.tivi.bg/logo/153x153/bulgariaonair.png'},
        'Euronews BG': {'id':'EuroNews', 'group':'Информационни','logo':'http://box.tivi.bg/logo/153x153/euronews.png'},
        'Нова HD': {'id':'Nova', 'group':'ЕФИРНИ','logo':'http://logos.kodibg.org/novatv.png'},
        'Star Life HD': {'id':'Star Life', 'group':'Други','logo': None},
        'Star Crime HD': {'id':'Star Life', 'group':'Други','logo': None},
        'Star Channel HD':  {'id':'Star Life', 'group':'Други','logo': None},
        'This Is Bulgaria HD': {'id':'thisisbg', 'group':'Научни','logo':'http://logos.epg.cloudns.org/thisisbg.png'},
        '7/8 TV': {'id':'78TV', 'group':'Други','logo':'http://logos.epg.cloudns.org/78tv.png'},
        'Code Health': {'id':'CodeHealth', 'group':'Други','logo': None},
        'Code Health HD': {'id':'CodeHealth', 'group':'Други','logo': None},
        'TV 999': {'id':'TV999', 'group':'Други','logo': None},
        'bTV Lady HD': {'id':'bTVLady', 'group':'Филмови','logo':'http://logos.epg.cloudns.org/btvlady.png'},
        'ТНТ 25': {'id':'tnt.ru', 'group':'Други','logo': None},
        'Любимое кино': {'id':'Любимоекино', 'group':'Други','logo': None},
        'EDGE Sport': {'id':'EDGE Sport', 'group':'Спорт','logo': None},
        'Super Tennis HD': {'id':'Supper Tennis', 'group':'Спорт','logo': None},
        'Deutsche Welle HD': {'id':'DeutscheWelle', 'group':'Политематични','logo':'http://logos.epg.cloudns.org/deutschewelle.png'},
        'France 24 HD': {'id':'france24fr.fr', 'group':'Политематични','logo': None},
        'TV5 Monde HD': {'id':'trtworld.com', 'group':'Други','logo': None},
        'DTX HD': {'id':'dtx.tv', 'group':'Други','logo': None},
        'TLC HD': {'id':'TLC', 'group':'Филмови','logo':'http://logos.epg.cloudns.org/tlc.png'},
        'Fishing and Hunting HD': {'id':'FishingandHunting', 'group':'Други','logo': None},
        'Nova News HD': {'id':'NovaNews', 'group':'Информационни','logo':'http://logos.epg.cloudns.org/novanews.png'},
        'Euronews BG HD': {'id':'EuroNews', 'group':'Информационни','logo':'http://logos.epg.cloudns.org/euronews.png'},
        'БГ+': {'id':'БГ+', 'group':'Други','logo': None},
        'Bulgaria 24 HD': {'id':'Bulgaria24', 'group':'Информационни','logo':'http://logos.epg.cloudns.org/bulgaria24.png'},
        '7/8 HD': {'id':'78TV', 'group':'Други','logo':'http://logos.epg.cloudns.org/78tv.png'},
        'TV Tourism HD': {'id':'tvt.bg', 'group':'Научни','logo': None},
        'RM TV': {'id':'RMTV', 'group':'Други','logo': None},
        'Agro TV HD': {'id':'agroTV', 'group':'Други','logo':'http://logos.epg.cloudns.org/agrotv.png'},
        'Евроком HD': {'id':'Eurocom', 'group':'Други','logo':'http://logos.epg.cloudns.org/eurocom.png'},
        'Travel XP HD': {'id':'TravelXP', 'group':'Научни','logo':'http://logos.epg.cloudns.org/travelxp.png'},
        'БГ+ HD': {'id':'БГ+', 'group':'Други','logo': None},
        'TV 999 HD':  {'id':'TV999', 'group':'Други','logo': 'http://logos.epg.cloudns.org/tv999.png'},
        'Романи Як': {'id':'РоманиЯк', 'group':'Други','logo': None},
        'Тянков Orient Folk': {'id':'TiankovFolk', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/tiankovfolk.png'},
        'Фен Фолк': {'id':'FENTV', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/fentv.png'},
        'MTV 90’s': {'id':'MTV90s', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/mtv90s.png'},
        'MTV 00s': {'id':'MTV00s', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/mtv00s.png'},
        'MTV 80’s': {'id':'MTV80s', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/mtv80s.png'},
        'Code Fashion TV HD': {'id':'FashionTV', 'group':'Други','logo':'http://logos.epg.cloudns.org/fashiontv.png'},
        'City HD': {'id':'City', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/city.png'},
        'Родина ТВ HD': {'id':'РодинаТВ', 'group':'Музикални','logo':''},
        'Тянков Folk HD': {'id':'TiankovFolk', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/tiankovfolk.png'},
        'Тянков Orient Folk HD': {'id':'TiankovFolk', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/tiankovfolk.png'},
        'Тянков Folk': {'id':'TiankovFolk', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/tiankovfolk.png'},
        'Шансон ТВ': {'id':'ШансонТВ', 'group':'Музикални','logo': None},
        'The Voice HD': {'id':'TheVoice', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/thevoice.png'},
        'ECTV Kids': {'id':'ECTVKids', 'group':'Детски','logo': None},
        'Cartoonito': {'id':'Cartoonito', 'group':'Детски','logo':'http://logos.epg.cloudns.org/cartoonito.png'},
        'Nicktoons': {'id':'Nicktoons', 'group':'Детски','logo':'http://logos.epg.cloudns.org/nicktoons.png'},
        'Централное ТВ': {'id':'ЦентралноеТВ', 'group':'Други','logo': None},
        'France 24 FR HD':{'id':'france24fr.fr', 'group':'Политематични','logo': None},
        'Първа програма': {'id':'PerviyKanal', 'group':'Други','logo': 'http://logos.epg.cloudns.org/perviykanal.png'},
        'TV 1000 org': {'id':'TV1000', 'group':'Други','logo':'http://logos.epg.cloudns.org/tv1000.png'},
        'KinoNova HD': {'id':'KinoNova', 'group':'Филмови','logo':'http://box.tivi.bg/logo/153x153/kinonova.png'},
        'Diema HD': {'id':'Diema', 'group':'Филмови','logo':'http://logos.kodibg.org/diema.png'},
        'Diema Family HD': {'id':'Diema Family', 'group':'Филмови','logo':'http://logos.kodibg.org/diemafamily.png'},
        'TVE HD': {'id':'TVE', 'group':'Други','logo': None},
        'Nova News LQ': {'id':'NovaNews', 'group':'Информационни','logo':'http://logos.epg.cloudns.org/novanews.png'},
        'Star Life LQ': {'id':'Star Life', 'group':'Други','logo': None},
        'Star Crime LQ': {'id':'Star Crime', 'group':'Други','logo': None},
        'Star Channel LQ': {'id':'Star Channel', 'group':'Други','logo': None},
        'БНТ 2 LQ': {'id':'bnt2.bg', 'group':'ЕФИРНИ','logo':'http://box.tivi.bg/logo/153x153/bnt2.png'},
        'БНТ 3 LQ': {'id':'bnt3.bg', 'group':'ЕФИРНИ','logo': None},
        'BTV HD h265 test': {'id':'bTV', 'group':'ЕФИРНИ','logo': 'http://box.tivi.bg/logo/153x153/btv.png'},
        'Nova HD 50p test': {'id':'Nova', 'group':'ЕФИРНИ','logo': 'http://logos.kodibg.org/novatv.png'},
        'Канал 8 Int': {'id':'Канал8Int', 'group':'Други','logo': None},
        'Mosaic 1': {'id':'Mosaic1', 'group':'Други','logo': None},
        'Мозайка 1': {'id':'Mosaic1', 'group':'Други','logo': None},
        'Euronews BG M': {'id':'EuroNews', 'group':'Информационни','logo':'http://logos.epg.cloudns.org/euronews.png'},
        '7/8 LQ': {'id':'78TV', 'group':'Други','logo':'http://logos.epg.cloudns.org/78tv.png'},
        'Nova Sport LQ': {'id':'Nova Sport', 'group':'Спортни','logo':'http://logos.kodibg.org/novasport.png'},
        'Planeta LQ': {'id':'Planeta', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/planeta.png'},
        'Planeta Folk LQ': {'id':'PlanetaFolk', 'group':'Музикални','logo':'http://logos.epg.cloudns.org/planetafolk.png'},
        'Б1Б Спорт': {'id':'b1b.tv', 'group':'Спорт','logo':'http://logos.epg.cloudns.org/planetafolk.png'},
        'Passion XXX 2': {'id':'PassionXXX2', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'SCT': {'id':'SCT', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Penthouse Quickies HD': {'id':'PenthouseQuickies', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Penthouse Gold HD': {'id':'PenthouseGold', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Penthouse Passion HD': {'id':'PenthousePassion', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Dorcel XXX HD': {'id':'dorcelxxx.com', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Dorcel TV HD': {'id':'dorceltv.com', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Prive TV': {'id':'private.tv', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Cento X Cento': {'id':'CentoXCento', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'Cento X Cento +2': {'id':'CentoXCento2', 'group':'18+','logo': 'http://box.tivi.bg/logo/153x153/18plus.png'},
        'KCN 1': {'id':'KCN1', 'group':'Други','logo': None},
        'KCN 2': {'id':'KCN2', 'group':'Други','logo': None},
        'KCN 3': {'id':'KCN3', 'group':'Други','logo': None},
        'Planeta 4K': {'id':'Planeta4K', 'group':'Музикални','logo': 'http://logos.epg.cloudns.org/planeta4k.png'},
        'Kiss UK': {'id':'Kiss TV', 'group':'Други','logo': None},
        'Inplus HD': {'id':'Inplus', 'group':'Други','logo': None},
    }
_map_ch.update(local_map_ch)

bg_map_ch = {
        'БНТ 1': {'id': 'BNT1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'БНТ 2': {'id': 'BNT2', 'group': 'Български', 'logo': 'http://logos.kodibg.org/bnt2.png'},
        'БНТ 2 HD': {'id': 'BNT2', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt2.png'},
        'BNT1 HD': {'id': 'BNT1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'БНТ 1 HD': {'id': 'BNT1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'BNT World': {'id': 'BNT World', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bntworld.png'},
        'BNT World HD': {'id': 'BNT World', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bntworld.png'},
        'БНТ HD': {'id': 'БНТ HD', 'group': 'Спортни', 'logo': 'http://logos.kodibg.org/bnthd.png'},
        'БНТ HD в SD': {'id': 'БНТ HD', 'group': 'Спортни', 'logo': 'http://logos.kodibg.org/bnthd.png'},
        'bTV': {'id': 'bTV', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'bTV HD': {'id': 'bTV', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'BNT1 +1': {'id': 'BNT1 +1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'BTV +1': {'id': 'BTV +1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'Nova +1': {'id': 'Nova +1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'БНТ HD +1': {'id': 'БНТ HD +1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnthd.png'},
        'BNT1 +2': {'id': 'BNT1 +2', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'BTV +2': {'id': 'BTV +2', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'Nova +2': {'id': 'Nova +2', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'BNT1 +7': {'id': 'BNT1 +7', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'BTV +7': {'id': 'BTV +7', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'Nova +7': {'id': 'Nova +7', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'БНТ HD +12': {'id': 'БНТ HD +12', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnthd.png'},
        'BNT1 +24': {'id': 'BNT1 +24', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'BTV +24': {'id': 'BTV +24', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'Nova +24': {'id': 'Nova +24', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'BNT1 +48': {'id': 'BNT1 +48', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'BTV +48': {'id': 'BTV +48', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'Nova +48': {'id': 'Nova +48', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'БНТ1 LQ': {'id': 'БНТ 1', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bnt1.png'},
        'bTV LQ': {'id': 'bTV', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/btv.png'},
        'Nova LQ': {'id': 'Nova', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'БНТ 2 LQ': {'id': 'BNT2', 'group': 'Ефирни', 'logo': 'http://box.tivi.bg/logo/153x153/bnt2.png'},
        'БНТ 3 LQ': {'id': 'BNT3', 'group': 'Ефирни', 'logo': 'https://box.tivi.bg/logo/153x153/bnt3.png'},
        'БНТ 3 HD': {'id': 'BNT3', 'group': 'Ефирни', 'logo': 'https://box.tivi.bg/logo/153x153/bnt3.png'},
        'БНТ 3': {'id': 'BNT3', 'group': 'Ефирни', 'logo': 'https://box.tivi.bg/logo/153x153/bnt3.png'},
        'BTV HD h265 test': {'id': 'bTV', 'group': 'Ефирни', 'logo': 'http://box.tivi.bg/logo/153x153/btv.png'},
        'Nova HD 50p test': {'id': 'Nova', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'Нова HD': {'id': 'Nova', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'Nova LQ': {'id': 'Nova', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/novatv.png'},
        'Bulgaria on Air HD': {'id': 'BulgariaOnAir', 'group': 'Ефирни', 'logo': 'http://box.tivi.bg/logo/153x153/bulgariaonair.png'},
        'Bulgaria on Air': {'id': 'BulgariaOnAir', 'group': 'Ефирни', 'logo': 'http://logos.kodibg.org/bgonair.png'},
    }
_map_ch.update(bg_map_ch)

my_map_ch = {
        'Viasat History HD': {'id':'', 'group':'Научни','logo':'http://logos.kodibg.org/viasathistory.png'},
        'Viasat Explore HD': {'id':'ViasatExplorer', 'group':'Научни','logo':'http://box.tivi.bg/logo/153x153/viasatexplorer.png'},
        'Viasat Nature HD': {'id':'ViasatNature', 'group':'Научни','logo':'http://logos.epg.cloudns.org/viasatnature.png'},
        'Viasat History': {'id':'', 'group':'Научни','logo':'http://logos.kodibg.org/viasathistory.png'},
        'Viasat Explore': {'id':'ViasatExplorer', 'group':'Научни','logo':'http://box.tivi.bg/logo/153x153/viasatexplorer.png'},
        'Viasat Nature': {'id':'ViasatNature', 'group':'Научни','logo':'http://logos.epg.cloudns.org/viasatnature.png'},
        'History HD': {'id':'History', 'group':'Научни','logo':'http://logos.kodibg.org/history.png'},
        'History Channel': {'id':'History', 'group':'Научни','logo':'http://logos.kodibg.org/history.png'},
        'NatGeo HD': {'id':'NatGeo', 'group':'Научни','logo':'http://logos.kodibg.org/natgeo.png'},
        'National Geographic' : {'id':'NatGeo', 'group':'Научни','logo':'http://logos.kodibg.org/natgeo.png'},
        'NatGeo LQ' : {'id':'NatGeo', 'group':'Научни','logo':'http://logos.kodibg.org/natgeo.png'},
        'Discovery Channel': {'id':'Discovery', 'group':'Научни','logo':'http://logos.kodibg.org/discovery.png'},
        'Discovery LQ': {'id':'Discovery', 'group':'Научни','logo':'http://logos.kodibg.org/discovery.png'},
        'Discovery HD': {'id':'Discovery', 'group':'Научни','logo':'http://logos.kodibg.org/discovery.png'},
        'Discovery Science': {'id':'DiscoveryScience', 'group':'Научни','logo':'http://logos.kodibg.org/discoveryscience.png'},
        'Discovery Science HD': {'id':'DiscoveryScience', 'group':'Научни','logo':'http://logos.kodibg.org/discoveryscience.png'},
        'Travel Channel HD': {'id':'TravelChannel', 'group':'Научни','logo':'http://logos.kodibg.org/travelchannel.png'},
        'Travel Channel': {'id':'TravelChannel', 'group':'Научни','logo':'http://logos.kodibg.org/travelchannel.png'},
    }
_map_ch.update(my_map_ch)

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
    _filt = re.compile(r'^#EXTINF.*group-title="(?P<group>.*?)".*ch-number="(?P<num>.*?)".*,(?P<name>.*).*\n(?P<url>.*)$', re.I|re.M)
    r = self.__s.get('http://cdn.tivi.bg/m/%s/hevc' % self.__mac)
    if r.status_code == requests.codes.ok and '#EXTM3U' == r.text[:7]:
        for m in _filt.finditer(r.text):
            yield m.group('name'), m.group('group'), m.group('num'), m.group('url')
    else:
        sys.exit('wrong responce')

  def __fill_storage(self):
      self.__store = {}
      for n, g, ch, url in self.__fetch():
          if n in list(_map_ch.keys()):
              if g not in list (_map_group.keys()):
                  print ('Group not found: %s name: %s' % (g, n))
              group = _map_ch[n].get('group', g)
              group = _map_group.get(group, group)
              self.__store[ch] = {'name': n, 'group': group, 'url': url, 'id': _map_ch[n]['id'], 'logo': _map_ch[n]['logo']}
          else:
              print('Not found %s' % n)

  def get_ch(self, ch):
      #self.__fill_storage()
      _ch = self.__store.get(ch, None)
      if not _ch:
          return None
      return _ch.get('url', None)

  def get_pls(self):
    self.__fill_storage()
    _line = '#EXTM3U\n'
    for k, v in list(self.__store.items()):
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

      _line = _line + '#EXTINF:-1 %s\n' % (extinf,)
      _line = _line + 'pipe:///usr/bin/curl -s -L -N --output - http://%s:%s/id/%s\n' % (self.__host, self.__port, k)
      # _line = _line + 'pipe:///usr/bin/ffmpeg -loglevel fatal -ignore_unknown -i http://%s:%s/id/%s -map 0 -c copy -metadata service_provider=tivi -metadata service_name=%s -tune zerolatency -f mpegts pipe:1\n' % (self.__host, self.__port, k, k)
    return _line.encode('utf-8')
