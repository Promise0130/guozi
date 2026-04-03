# -*- coding: utf-8 -*-
"""
Generate comprehensive guozi_entity_list CSV from crawled SASAC data.
Merges existing 32-row CSV with newly crawled enterprise data across all provinces.
"""
import csv
import os
from datetime import date

TODAY = "2026-04-04"
OUTPUT_PATH = os.path.join("delivery", "guozi_entity_list_v1_20260402.csv")
SITE_COPY = os.path.join("site", "data", "entity_list.csv")

# ─── Province metadata ────────────────────────────────────────────
PROVINCES = {
    "BJ": "北京", "TJ": "天津", "HE": "河北", "SX": "山西", "NM": "内蒙古",
    "LN": "辽宁", "JL": "吉林", "HL": "黑龙江", "SH": "上海", "JS": "江苏",
    "ZJ": "浙江", "AH": "安徽", "FJ": "福建", "JX": "江西", "SD": "山东",
    "HA": "河南", "HB": "湖北", "HN": "湖南", "GD": "广东", "GX": "广西",
    "HI": "海南", "CQ": "重庆", "SC": "四川", "GZ": "贵州", "YN": "云南",
    "XZ": "西藏", "SN": "陕西", "GS": "甘肃", "QH": "青海", "NX": "宁夏",
    "XJ": "新疆", "BT": "新疆兵团",
}

SASAC_URLS = {
    "BJ": "http://gzw.beijing.gov.cn", "TJ": "http://sasac.tj.gov.cn",
    "HE": "http://hbsa.hebei.gov.cn", "SX": "http://gzw.shanxi.gov.cn",
    "NM": "http://gzw.nmg.gov.cn", "LN": "http://gzw.ln.gov.cn",
    "JL": "http://gzw.jl.gov.cn", "HL": "http://gzw.hlj.gov.cn",
    "SH": "http://www.gzw.sh.gov.cn", "JS": "http://jsgzw.jiangsu.gov.cn",
    "ZJ": "https://gzw.zj.gov.cn", "AH": "http://gzw.ah.gov.cn",
    "FJ": "http://gzw.fujian.gov.cn", "JX": "http://gzw.jiangxi.gov.cn",
    "SD": "http://gzw.shandong.gov.cn", "HA": "http://gzw.henan.gov.cn",
    "HB": "http://gzw.hubei.gov.cn", "HN": "http://gzw.hunan.gov.cn",
    "GD": "https://gzw.gd.gov.cn", "GX": "http://gzw.gxzf.gov.cn",
    "HI": "https://gzw.hainan.gov.cn", "CQ": "http://gzw.cq.gov.cn",
    "SC": "http://gzw.sc.gov.cn", "GZ": "http://gzw.guizhou.gov.cn",
    "YN": "https://gzw.yn.gov.cn", "XZ": "http://gzw.xizang.gov.cn",
    "SN": "http://sxgz.shaanxi.gov.cn", "GS": "http://gzw.gansu.gov.cn",
    "QH": "http://gzw.qinghai.gov.cn", "NX": "http://gzw.nx.gov.cn",
    "XJ": "http://gzw.xinjiang.gov.cn", "BT": "http://gyzc.xjbt.gov.cn",
}


def make_row(code, full, short, caliber="supervised", caliber_label="省国资委监管企业",
             page_type="LIST-A", sector="综合", fin=False,
             completeness="full_list", confidence=0.90, uev=1, review=False, notes=""):
    return {
        "province_code": code,
        "province": PROVINCES[code],
        "entity_name_full": full,
        "entity_name_short": short,
        "list_caliber": caliber,
        "list_caliber_label": caliber_label,
        "source_page_type": page_type,
        "sector": sector,
        "includes_financial": fin,
        "completeness": completeness,
        "confidence": confidence,
        "uev_level": uev,
        "needs_manual_review": review,
        "notes": notes,
    }


# ─── Enterprise data per province ─────────────────────────────────
# Key: province_code → list of (full_name, short_name, sector, is_financial, notes)

def beijing_data():
    """42 enterprises from official paginated list at gzw.beijing.gov.cn/yggq/jgqy/"""
    items = [
        ("首钢集团有限公司", "首钢集团", "冶金", False),
        ("北京公共交通控股（集团）有限公司", "公交集团", "交通", False),
        ("北京市基础设施投资有限公司", "基础设施投资", "投资", False),
        ("北京市地铁运营有限公司", "地铁运营", "交通", False),
        ("北京控股集团有限公司", "北控集团", "综合", False),
        ("北京能源集团有限责任公司", "能源集团", "能源", False),
        ("北京首都创业集团有限公司", "首创集团", "环保", False),
        ("北京市国有资产经营有限责任公司", "国资经营", "投资", False),
        ("北京市自来水集团有限责任公司", "自来水集团", "公用事业", False),
        ("北京银行股份有限公司", "北京银行", "金融", True),
        ("华夏银行股份有限公司", "华夏银行", "金融", True),
        ("北京金融控股集团有限公司", "金控集团", "金融", True),
        ("北京农村商业银行股份有限公司", "农商银行", "金融", True),
        ("北京电子控股有限责任公司", "电子控股", "电子", False),
        ("北京汽车集团有限公司", "北汽集团", "汽车", False),
        ("北京建工集团有限责任公司", "建工集团", "建筑", False),
        ("北京城建集团有限责任公司", "城建集团", "建筑", False),
        ("北京首都旅游集团有限责任公司", "首旅集团", "旅游", False),
        ("首都实业投资有限公司", "首都实业", "投资", False),
        ("北京京城机电控股有限责任公司", "京城机电", "机械", False),
        ("北京一轻控股有限责任公司", "一轻控股", "轻工", False),
        ("北京时尚控股有限责任公司", "时尚控股", "轻工", False),
        ("北京化学工业集团有限责任公司", "化工集团", "化工", False),
        ("中国北京同仁堂（集团）有限责任公司", "同仁堂集团", "医药", False),
        ("北京金隅集团股份有限公司", "金隅集团", "建材", False),
        ("北京首都开发控股（集团）有限公司", "首开集团", "房地产", False),
        ("北京北辰实业集团有限责任公司", "北辰实业", "房地产", False),
        ("北京市首都公路发展集团有限公司", "首发集团", "交通", False),
        ("北京祥龙资产经营有限责任公司", "祥龙资产", "综合", False),
        ("北京城市排水集团有限责任公司", "排水集团", "公用事业", False),
        ("北京环境卫生工程集团有限公司", "环卫集团", "环保", False),
        ("北京城市副中心投资建设集团有限公司", "副中心投资", "投资", False),
        ("北京首农食品集团有限公司", "首农集团", "农业", False),
        ("北京市建筑设计研究院有限公司", "北京建院", "建筑", False),
        ("北京市供销合作总社", "供销合作社", "商贸", False),
        ("北京国有资本运营管理有限公司", "国资运营", "投资", False),
        ("北京保障房中心有限公司", "保障房中心", "房地产", False),
        ("北京水务投资集团有限公司", "水务投资", "公用事业", False),
        ("永定河流域投资有限公司", "永定河投资", "环保", False),
        ("北京航空有限责任公司", "北京航空", "交通", False),
        ("中关村发展集团股份有限公司", "中关村发展", "科技", False),
        ("首都文化科技集团有限公司", "首都文科", "文化", False),
    ]
    return [make_row("BJ", f, s, sector=sec,
                     fin=fin, notes="从官网监管企业名录三页提取",
                     confidence=0.92) for f, s, sec, fin in items]


def liaoning_data():
    """11 enterprises from official numbered list"""
    items = [
        ("辽宁省能源产业控股集团有限责任公司", "能源控股集团", "能源"),
        ("辽宁省交通建设投资集团有限责任公司", "交投集团", "交通"),
        ("辽宁省水资源管理和生态环保产业集团有限责任公司", "辽水集团", "环保"),
        ("辽渔集团有限公司", "辽渔集团", "农业"),
        ("辽宁省机场管理集团有限公司", "机场集团", "交通"),
        ("辽宁省粮食发展集团有限责任公司", "辽粮集团", "农业"),
        ("辽宁省地质矿产投资开发集团有限公司", "矿投集团", "矿业"),
        ("辽宁省咨询产业集团有限责任公司", "辽咨集团", "服务"),
        ("辽宁省文体旅产业发展集团有限责任公司", "文体旅集团", "文化"),
        ("辽宁控股（集团）有限责任公司", "辽控集团", "综合"),
        ("辽宁锦城石化有限公司", "锦城石化", "化工"),
    ]
    return [make_row("LN", f, s, sector=sec,
                     notes="从省企名录页官方编号列表提取") for f, s, sec in items]


def neimenggu_data():
    """19 enterprises from official enterprise info page"""
    items = [
        ("包头钢铁（集团）有限责任公司", "包钢集团", "冶金"),
        ("内蒙古森林工业集团有限责任公司", "森工集团", "林业"),
        ("内蒙古电力（集团）有限责任公司", "电力集团", "能源"),
        ("内蒙古民航机场集团有限责任公司", "机场集团", "交通"),
        ("内蒙古能源集团有限公司", "能源集团", "能源"),
        ("内蒙古地质矿产集团有限公司", "地矿集团", "矿业"),
        ("内蒙古交通投资（集团）有限责任公司", "交投集团", "交通"),
        ("内蒙古交通集团有限公司", "交通集团", "交通"),
        ("内蒙古蒙盐盐业集团有限公司", "蒙盐集团", "食品"),
        ("内蒙古新城宾馆旅游业集团有限责任公司", "新城宾馆集团", "旅游"),
        ("内蒙古国贸集团有限公司", "国贸集团", "商贸"),
        ("内蒙古水务发展集团有限公司", "水务集团", "公用事业"),
        ("内蒙古文化旅游投资集团有限公司", "文旅投资", "文化"),
        ("内蒙古国有资本运营有限公司", "国资运营", "投资"),
        ("内蒙古威信保安押运服务有限责任公司", "威信保安", "服务"),
        ("内蒙古联合交易控股集团有限公司", "联合交易集团", "服务"),
        ("内蒙古林草生态建设有限公司", "林草生态", "林业"),
        ("内蒙古自治区储备粮管理有限公司", "储备粮管理", "农业"),
        ("内蒙古自治区基本建设咨询投资有限公司", "基建咨询投资", "建筑"),
    ]
    return [make_row("NM", f, s, sector=sec,
                     notes="从企业信息公开页提取") for f, s, sec in items]


def hunan_data():
    """21 enterprises from official structured table"""
    direct = [
        ("湖南钢铁集团有限公司", "湖南钢铁", "冶金"),
        ("湖南省高速公路集团有限公司", "高速集团", "交通"),
        ("湖南建设投资集团有限责任公司", "建投集团", "投资"),
        ("湖南农业发展投资集团有限责任公司", "农发投资", "农业"),
        ("湖南省机场管理集团有限公司", "机场集团", "交通"),
        ("湖南轨道交通控股集团有限公司", "轨道交通", "交通"),
        ("湖南省港航水利集团有限公司", "港航水利", "交通"),
        ("湖南能源集团有限公司", "能源集团", "能源"),
        ("湘电集团有限公司", "湘电集团", "机械"),
        ("湖南省矿产资源集团有限责任公司", "矿产资源", "矿业"),
        ("湖南盐业集团有限公司", "盐业集团", "食品"),
        ("湖南海利高新技术产业集团有限公司", "海利集团", "化工"),
        ("湖南湘科控股集团有限公司", "湘科控股", "科技"),
        ("湖南医药发展投资集团有限公司", "医药投资", "医药"),
        ("湖南高新创业投资集团有限公司", "高新创投", "投资"),
        ("湖南兴湘投资控股集团有限公司", "兴湘投资", "投资"),
    ]
    entrusted = [
        ("湖南蓉园集团有限公司", "蓉园集团", "服务"),
        ("湖南湘勤集团有限公司", "湘勤集团", "服务"),
        ("湖南万安达集团有限责任公司", "万安达集团", "服务"),
    ]
    majority = [
        ("湖南鑫牛资产管理集团有限公司", "鑫牛资产", "投资"),
        ("中联重科股份有限公司", "中联重科", "机械"),
    ]
    rows = []
    for f, s, sec in direct:
        rows.append(make_row("HN", f, s, sector=sec, notes="直接监管企业"))
    for f, s, sec in entrusted:
        rows.append(make_row("HN", f, s, caliber="entrusted",
                             caliber_label="委托监管企业", sector=sec, notes="委托监管企业"))
    for f, s, sec in majority:
        rows.append(make_row("HN", f, s, caliber="majority_shareholder",
                             caliber_label="第一大股东企业", sector=sec, notes="第一大股东企业"))
    return rows


def xinjiang_data():
    """17 enterprises from official enterprise list page"""
    items = [
        ("新疆有色金属工业（集团）有限责任公司", "有色集团", "冶金"),
        ("新疆机场（集团）有限责任公司", "机场集团", "交通"),
        ("新疆能源（集团）有限责任公司", "能源集团", "能源"),
        ("新疆中泰（集团）有限责任公司", "中泰集团", "化工"),
        ("新疆投资发展（集团）有限责任公司", "投资发展集团", "投资"),
        ("新疆地矿投资（集团）有限责任公司", "地矿投资", "矿业"),
        ("新疆水利发展投资（集团）有限公司", "水利发展投资", "公用事业"),
        ("新疆交通投资（集团）有限责任公司", "交投集团", "交通"),
        ("新疆商贸物流（集团）有限公司", "商贸物流", "商贸"),
        ("数字新疆产业投资（集团）有限公司", "数字新疆", "科技"),
        ("新疆亚新煤层气投资开发（集团）有限责任公司", "亚新煤层气", "能源"),
        ("新疆人才发展集团有限责任公司", "人才发展集团", "服务"),
        ("新疆农牧业投资（集团）有限责任公司", "农牧业投资", "农业"),
        ("新疆新业国有资产经营（集团）有限责任公司", "新业集团", "综合"),
        ("新疆金融投资（集团）有限责任公司", "金融投资集团", "金融", ),
        ("新疆文化旅游投资集团有限公司", "文旅投资", "文化"),
        ("新疆教育出版社有限责任公司", "教育出版社", "文化"),
    ]
    rows = []
    for item in items:
        f, s, sec = item[0], item[1], item[2]
        fin = (sec == "金融")
        rows.append(make_row("XJ", f, s, sector=sec, fin=fin,
                             notes="从监管企业专栏提取"))
    return rows


def ningxia_data():
    """6 enterprises from official enterprise list page"""
    items = [
        ("宁夏交通建设投资集团有限公司", "交建投集团", "交通"),
        ("宁夏农垦集团公司", "农垦集团", "农业"),
        ("宁夏国有资本运营集团公司", "国资运营集团", "投资"),
        ("宁夏国有资产投资控股集团公司", "国投控股集团", "投资"),
        ("宁夏旅游投资集团公司", "旅投集团", "旅游"),
        ("数字宁夏建设运营有限责任公司", "数字宁夏", "科技"),
    ]
    return [make_row("NX", f, s, sector=sec,
                     notes="从企业名录/区属企业专栏提取") for f, s, sec in items]


def hainan_data():
    """9 enterprises from official 省属重点监管企业名录"""
    items = [
        ("海南省发展控股有限公司", "发展控股", "综合"),
        ("海南省农垦投资控股集团有限公司", "农垦集团", "农业"),
        ("海南省旅游投资集团有限公司", "旅投集团", "旅游"),
        ("海南国际商业航天发射有限公司", "商业航天", "科技"),
        ("海南省交通投资控股有限公司", "交投控股", "交通"),
        ("海南省水利水务发展集团有限公司", "水利水务集团", "公用事业"),
        ("海南海钢集团有限公司", "海钢集团", "冶金"),
        ("海南省工程咨询设计集团有限公司", "工程咨询设计", "建筑"),
        ("中国通用航空有限责任公司", "通用航空", "交通"),
    ]
    return [make_row("HI", f, s, sector=sec,
                     notes="从省属重点监管企业名录页提取") for f, s, sec in items]


def chongqing_data():
    """15+ enterprises from 国企简介 page (page 1)"""
    items = [
        ("重庆机场集团有限公司", "机场集团", "交通"),
        ("重庆联合产权交易所集团股份有限公司", "联交所集团", "服务"),
        ("重庆设计集团有限公司", "设计集团", "建筑"),
        ("民生实业（集团）有限公司", "民生实业", "综合"),
        ("重庆新华出版集团有限公司", "新华出版集团", "文化"),
        ("重庆文化旅游集团有限公司", "文旅集团", "文化"),
        ("庆铃汽车（集团）有限公司", "庆铃汽车", "汽车"),
        ("重庆交通开投集团有限公司", "交通开投", "交通"),
        ("重庆银行股份有限公司", "重庆银行", "金融"),
        ("重庆农村商业银行股份有限公司", "重庆农商行", "金融"),
        ("重庆市农业投资集团有限公司", "农投集团", "农业"),
        ("重庆高新开发建设投资集团有限公司", "高新投资", "投资"),
        ("西南证券股份有限公司", "西南证券", "金融"),
        ("重庆物流集团有限公司", "物流集团", "商贸"),
        ("重庆三峡银行股份有限公司", "三峡银行", "金融"),
    ]
    rows = []
    for f, s, sec in items:
        fin = (sec == "金融")
        rows.append(make_row("CQ", f, s, page_type="LIST-B", sector=sec, fin=fin,
                             completeness="partial_identified", confidence=0.80, uev=2,
                             review=True, notes="从国企简介专栏提取（第1页，可能不完整）"))
    return rows


def anhui_data():
    """29+ enterprises from 省企网群 sidebar links"""
    items = [
        ("安徽省交通控股集团有限公司", "省交通控股", "交通"),
        ("海螺集团有限责任公司", "海螺集团", "建材"),
        ("安徽省能源集团有限公司", "省能源集团", "能源"),
        ("淮北矿业控股股份有限公司", "淮北矿业", "矿业"),
        ("淮河能源控股集团有限责任公司", "淮河能源", "能源"),
        ("国元金融控股集团有限责任公司", "国元金控", "金融"),
        ("安徽省投资集团控股有限公司", "省投资集团", "投资"),
        ("铜陵有色金属集团控股有限公司", "铜陵有色", "冶金"),
        ("安徽江淮汽车集团控股有限公司", "江淮汽车集团", "汽车"),
        ("皖北煤电集团有限责任公司", "皖北煤电", "能源"),
        ("华安证券股份有限公司", "华安证券", "金融"),
        ("安徽省徽商银行股份有限公司", "徽商银行", "金融"),
        ("安徽引江济淮集团有限公司", "引江济淮集团", "公用事业"),
        ("安徽省港航集团有限公司", "省港航集团", "交通"),
        ("安徽叉车集团有限责任公司", "叉车集团", "机械"),
        ("安徽国控集团有限公司", "安徽国控", "综合"),
        ("安徽建工集团股份有限公司", "建工集团", "建筑"),
        ("安徽省机场集团有限公司", "机场集团", "交通"),
        ("安徽省农垦集团有限公司", "省农垦集团", "农业"),
        ("安徽皖维集团有限责任公司", "皖维集团", "化工"),
        ("安徽皖中集团有限责任公司", "皖中集团", "综合"),
        ("中煤矿建集团有限公司", "中煤矿建集团", "矿业"),
        ("安徽省徽商集团有限公司", "省徽商集团", "商贸"),
        ("安徽省生态环境集团有限公司", "省生态环境集团", "环保"),
        ("安徽省华强集团有限公司", "省华强集团", "科技"),
        ("安徽省淮海实业发展集团有限公司", "淮海集团", "综合"),
        ("安徽通航控股集团有限公司", "通航控股", "交通"),
        ("安徽省粮食产业集团有限公司", "省粮食产业集团", "农业"),
        ("数字安徽有限责任公司", "数字安徽", "科技"),
    ]
    rows = []
    for f, s, sec in items:
        fin = (sec == "金融")
        rows.append(make_row("AH", f, s, page_type="LIST-F", sector=sec, fin=fin,
                             completeness="full_list", confidence=0.80, uev=2,
                             notes="从省企网群侧边栏企业链接提取"))
    return rows


def shanxi_data():
    """5 enterprises visible from enterprise list page (likely truncated)"""
    items = [
        ("山西焦煤集团有限责任公司", "山西焦煤", "能源"),
        ("晋能控股集团有限公司", "晋能控股", "能源"),
        ("华阳新材料科技集团有限公司", "华阳新材料", "化工"),
        ("潞安化工集团有限公司", "潞安化工", "化工"),
        ("华新燃气集团有限公司", "华新燃气", "能源"),
    ]
    return [make_row("SX", f, s, sector=sec,
                     page_type="LIST-F", completeness="partial_identified",
                     confidence=0.70, uev=2, review=True,
                     notes="从监管企业名录页提取，页面可能截断，实际企业数更多")
            for f, s, sec in items]


def jilin_data():
    """9 enterprises identified from news/jobs"""
    items = [
        ("吉林省矿业集团有限责任公司", "矿业集团", "矿业"),
        ("吉林省安保集团有限责任公司", "安保集团", "服务"),
        ("吉林省农业发展集团有限公司", "农发集团", "农业"),
        ("吉林高速公路集团有限公司", "吉高集团", "交通"),
        ("一汽富维股份有限公司", "富维股份", "汽车"),
        ("吉林省资本运营集团有限公司", "吉林资本", "投资"),
        ("吉林省国资运营集团有限公司", "国资运营集团", "投资"),
        ("吉林省吉盛资产管理有限责任公司", "吉盛公司", "投资"),
        ("吉能集团有限公司", "吉能集团", "能源"),
    ]
    return [make_row("JL", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从新闻/招聘识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.55, uev=3, review=True,
                     notes="从招聘公告和新闻间接识别")
            for f, s, sec in items]


def heilongjiang_data():
    """3 enterprises from news mentions"""
    items = [
        ("黑龙江省农业投资集团有限公司", "农投集团", "农业"),
        ("龙江建投集团有限公司", "龙江建投", "建筑"),
        ("黑龙江产权交易集团有限公司", "交易集团", "服务"),
    ]
    return [make_row("HL", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从新闻识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.50, uev=3, review=True,
                     notes="从新闻间接识别，数量远不完整")
            for f, s, sec in items]


def fujian_data():
    """16 enterprises from official 所出资企业 list at gzw.fujian.gov.cn/gzgk/ssqy_1/"""
    items = [
        ("福建省高速公路集团有限公司", "福建高速集团", "交通"),
        ("福建省投资开发集团有限责任公司", "投资集团", "投资"),
        ("福建省工业控股集团有限公司", "工控集团", "制造"),
        ("福建省能源石化集团有限责任公司", "能源石化集团", "能源"),
        ("福建省港口集团有限责任公司", "港口集团", "交通"),
        ("福建省汽车工业集团有限公司", "福汽集团", "汽车"),
        ("福建省电子信息（集团）有限责任公司", "电子信息集团", "电子"),
        ("福建省船舶工业集团有限公司", "福船集团", "制造"),
        ("福建省建设投资集团有限责任公司", "建投集团", "建筑"),
        ("福建省旅游发展集团有限公司", "旅游发展集团", "旅游"),
        ("中国（福建）对外贸易中心集团有限责任公司", "外贸中心集团", "商贸"),
        ("福建省招标采购集团有限公司", "招标集团", "服务"),
        ("福建省水利投资开发集团有限公司", "水利投资集团", "水利"),
        ("福建省大数据集团有限公司", "大数据集团", "数据"),
        ("福建省国有资产管理有限公司", "国有资产管理", "投资"),
        ("福建省医药集团有限责任公司", "医药集团", "医药"),
    ]
    return [make_row("FJ", f, s, sector=sec,
                     caliber="supervised",
                     caliber_label="省国资委所出资企业",
                     page_type="LIST-A", completeness="full_list",
                     confidence=0.95, uev=1,
                     notes="官方所出资企业列表")
            for f, s, sec in items]


def henan_data():
    """5 enterprises from news mentions"""
    items = [
        ("河南省国控集团有限公司", "河南国控", "综合"),
        ("中国河南国际合作集团有限公司", "河南国际", "商贸"),
        ("河南省农业综合开发投资集团有限公司", "河南农投", "农业"),
        ("河南铁路建设投资集团有限公司", "河南铁建投", "交通"),
        ("河南省文化旅游投资集团有限公司", "河南文旅投", "文化"),
    ]
    return [make_row("HA", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从新闻识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.50, uev=3, review=True,
                     notes="从新闻间接识别，数量远不完整")
            for f, s, sec in items]


def guizhou_data():
    """8 enterprises from news/recruitment mentions"""
    items = [
        ("贵州能源集团有限公司", "贵州能源", "能源"),
        ("贵州高速公路集团有限公司", "贵州高速", "交通"),
        ("中国贵州茅台酒厂（集团）有限责任公司", "茅台集团", "食品"),
        ("贵州磷化（集团）有限责任公司", "贵州磷化", "化工"),
        ("贵州省水利投资（集团）有限责任公司", "贵州水投", "公用事业"),
        ("贵州大数据产业发展集团有限公司", "贵州大数据", "科技"),
        ("贵州省港航集团有限公司", "贵州港航", "交通"),
        ("贵州旅游投资控股（集团）有限责任公司", "贵旅集团", "旅游"),
    ]
    return [make_row("GZ", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从新闻/招聘识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.55, uev=3, review=True,
                     notes="从企业之窗和新闻间接识别")
            for f, s, sec in items]


def yunnan_data():
    """7 enterprises from news mentions"""
    items = [
        ("云南省机场集团有限责任公司", "云南机场集团", "交通"),
        ("云南省建设投资控股集团有限公司", "云南建投集团", "建筑"),
        ("云南康旅控股集团有限公司", "康旅集团", "旅游"),
        ("云南省能源投资集团有限公司", "能投集团", "能源"),
        ("云南省贵金属集团有限公司", "贵金属集团", "冶金"),
        ("云南锡业集团（控股）有限责任公司", "云锡集团", "冶金"),
        ("云南航空产业投资集团有限责任公司", "航空产业投资", "交通"),
    ]
    return [make_row("YN", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从新闻识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.55, uev=3, review=True,
                     notes="从省属企业新闻栏目间接识别")
            for f, s, sec in items]


def tianjin_data():
    """29 enterprises from official 市管国企名录 at sasac.tj.gov.cn"""
    items = [
        ("天津港（集团）有限公司", "天津港集团", "交通"),
        ("天津能源投资集团有限公司", "能源投资集团", "能源"),
        ("天津轨道交通集团有限公司", "轨道交通集团", "交通"),
        ("天津泰达投资控股有限公司", "泰达控股", "投资"),
        ("天津银行股份有限公司", "天津银行", "金融", True),
        ("渤海银行股份有限公司", "渤海银行", "金融", True),
        ("渤海证券股份有限公司", "渤海证券", "金融", True),
        ("北方国际集团有限公司", "北方国际集团", "商贸"),
        ("天津城建集团控股有限公司", "城建集团控股", "建筑"),
        ("天津水务集团有限公司", "水务集团", "公用事业"),
        ("天津食品集团有限公司", "食品集团", "食品"),
        ("天津百利机械装备集团有限公司", "百利装备集团", "制造"),
        ("天津渤海化工集团有限责任公司", "渤海化工集团", "化工"),
        ("天津渤海轻工投资集团有限公司", "渤海轻工集团", "轻工"),
        ("天津城市基础设施建设投资集团有限公司", "城投集团", "投资"),
        ("天津市交通（集团）有限公司", "交通集团", "交通"),
        ("天津市公共交通集团（控股）有限公司", "公交集团", "交通"),
        ("天津市政建设集团有限公司", "市政建设集团", "建筑"),
        ("天津市旅游（控股）集团有限公司", "旅游集团", "旅游"),
        ("天津房地产集团有限公司", "房地产集团", "房地产"),
        ("天津津融投资服务集团有限公司", "津融服务集团", "金融", True),
        ("天津纺织集团（控股）有限公司", "纺织集团", "轻工"),
        ("天津滨海农村商业银行股份有限公司", "滨海农商行", "金融", True),
        ("天津农村商业银行股份有限公司", "天津农商行", "金融", True),
        ("天津利和进出口集团有限公司", "利和进出口集团", "商贸"),
        ("天津劝业华联集团有限公司", "劝业华联集团", "商贸"),
        ("北方国际信托股份有限公司", "北方信托", "金融", True),
        ("天津国兴资本运营有限公司", "国兴资本", "投资"),
        ("天津国有资本投资运营有限公司", "国有资本投资运营", "投资"),
    ]
    rows = []
    for item in items:
        f, s, sec = item[0], item[1], item[2]
        fin = item[3] if len(item) > 3 else False
        rows.append(make_row("TJ", f, s, sector=sec, fin=fin,
                             caliber="supervised",
                             caliber_label="天津市国资委市管国企",
                             page_type="LIST-A", completeness="full_list",
                             confidence=0.95, uev=1,
                             notes="官方市管国企名录+委管企业名录"))
    return rows


def hebei_data():
    """4 enterprises from news at hbsa.hebei.gov.cn"""
    items = [
        ("开滦（集团）有限责任公司", "开滦集团", "矿业"),
        ("唐山三友集团有限公司", "三友集团", "化工"),
        ("河北建工集团有限责任公司", "河北建工集团", "建筑"),
        ("冀中能源集团有限责任公司", "冀中能源", "矿业"),
    ]
    return [make_row("HE", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从新闻识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.50, uev=3, review=True,
                     notes="企业名录页JS渲染 仅从新闻识别")
            for f, s, sec in items]


def shanghai_data():
    """42 enterprises from official info disclosure at www.gzw.sh.gov.cn/shgzw_xwzx_xxpl/"""
    items = [
        ("上海国际集团有限公司", "上海国际集团", "金融", True),
        ("上海国盛（集团）有限公司", "国盛集团", "投资"),
        ("上海国有资本投资有限公司", "上海国投", "投资"),
        ("上海交易集团有限公司", "交易集团", "金融", True),
        ("上海汽车集团股份有限公司", "上汽集团", "汽车"),
        ("上海电气集团股份有限公司", "上海电气", "制造"),
        ("上海华谊集团股份有限公司", "华谊集团", "化工"),
        ("上海实业（集团）有限公司", "上实集团", "综合"),
        ("申能（集团）有限公司", "申能集团", "能源"),
        ("上海仪电（集团）有限公司", "仪电集团", "电子"),
        ("上海华虹（集团）有限公司", "华虹集团", "电子"),
        ("上海数据集团有限公司", "数据集团", "数据"),
        ("上海联和投资有限公司", "联和投资", "投资"),
        ("上海国际港务（集团）股份有限公司", "上港集团", "交通"),
        ("上海建工集团股份有限公司", "上海建工", "建筑"),
        ("上海隧道工程股份有限公司", "隧道股份", "建筑"),
        ("华东建筑集团股份有限公司", "华东建筑", "建筑"),
        ("上海建科咨询集团股份有限公司", "建科咨询", "建筑"),
        ("绿地控股集团股份有限公司", "绿地控股", "房地产"),
        ("光明食品（集团）有限公司", "光明食品", "食品"),
        ("百联集团有限公司", "百联集团", "商贸"),
        ("锦江国际（集团）有限公司", "锦江国际", "旅游"),
        ("东浩兰生（集团）有限公司", "东浩兰生", "商贸"),
        ("上海国茂控股有限公司", "国茂控股", "综合"),
        ("东方国际（集团）有限公司", "东方国际", "商贸"),
        ("中国太平洋保险（集团）股份有限公司", "太平洋保险", "金融", True),
        ("上海浦东发展银行股份有限公司", "浦发银行", "金融", True),
        ("上海银行股份有限公司", "上海银行", "金融", True),
        ("上海农村商业银行股份有限公司", "上海农商行", "金融", True),
        ("国泰海通证券股份有限公司", "国泰海通证券", "金融", True),
        ("上海机场（集团）有限公司", "机场集团", "交通"),
        ("上海地产（集团）有限公司", "上海地产", "房地产"),
        ("上海城投（集团）有限公司", "上海城投", "投资"),
        ("上海久事（集团）有限公司", "久事集团", "综合"),
        ("上海申通地铁集团有限公司", "申通地铁", "交通"),
        ("上海临港经济发展（集团）有限公司", "临港集团", "投资"),
        ("上海申迪（集团）有限公司", "申迪集团", "旅游"),
        ("长三角投资（上海）有限公司", "长三角投资", "投资"),
        ("上海市现代农业投资发展集团有限公司", "现代农业投资", "农业"),
        ("上海东方枢纽投资建设发展集团有限公司", "东方枢纽集团", "交通"),
        ("长三角一体化示范区新发展建设有限公司", "长三角示范区新发展", "投资"),
        ("中保投资有限责任公司", "中保投资", "金融", True),
    ]
    rows = []
    for item in items:
        f, s, sec = item[0], item[1], item[2]
        fin = item[3] if len(item) > 3 else False
        rows.append(make_row("SH", f, s, sector=sec, fin=fin,
                             caliber="supervised",
                             caliber_label="上海市国资委监管企业",
                             page_type="LIST-A", completeness="full_list",
                             confidence=0.95, uev=1,
                             notes="官方信息披露企业目录"))
    return rows


def jiangsu_data():
    """21 enterprises from homepage column links at jsgzw.jiangsu.gov.cn"""
    items = [
        ("江苏国信集团有限公司", "国信集团", "综合"),
        ("江苏交通控股有限公司", "交通控股", "交通"),
        ("东部机场集团有限公司", "东部机场", "交通"),
        ("江苏苏豪控股集团有限公司", "苏豪控股", "商贸"),
        ("中国江苏国际经济技术合作集团有限公司", "中江集团", "商贸"),
        ("江苏省农垦集团有限公司", "江苏农垦", "农业"),
        ("江苏省徐矿集团有限公司", "徐矿集团", "矿业"),
        ("江苏省沿海开发集团有限公司", "沿海集团", "投资"),
        ("江苏省港口集团有限公司", "江苏港口", "交通"),
        ("江苏省铁路集团有限公司", "江苏铁路", "交通"),
        ("江苏省环保集团有限公司", "江苏环保", "环保"),
        ("江苏省盐业集团有限责任公司", "苏盐集团", "轻工"),
        ("江苏省粮食集团有限责任公司", "苏粮集团", "食品"),
        ("江苏省高科技投资集团有限公司", "江苏高投", "投资"),
        ("南京金陵饭店集团有限公司", "金陵饭店", "旅游"),
        ("南京钟山宾馆集团有限公司", "钟山宾馆", "旅游"),
        ("江苏水源有限责任公司", "江苏水源", "水利"),
        ("江苏省体育产业集团有限公司", "体产集团", "体育"),
        ("江苏省国有资本投资集团有限公司", "国投集团", "投资"),
        ("江苏省规划设计集团有限公司", "规划设计", "建筑"),
        ("江苏省数据集团有限公司", "数据集团", "数据"),
    ]
    return [make_row("JS", f, s, sector=sec,
                     caliber="supervised",
                     caliber_label="省国资委省属企业",
                     page_type="LIST-A", completeness="full_list",
                     confidence=0.95, uev=1,
                     notes="官方首页省属企业栏目")
            for f, s, sec in items]


def guangxi_data():
    """16 enterprises from official list at gzw.gxzf.gov.cn/gxgq/"""
    items = [
        ("广西交通投资集团有限公司", "广西交投", "交通"),
        ("广西农村投资集团有限公司", "广西农投", "农业"),
        ("广西北部湾国际港务集团有限公司", "北部湾港务", "交通"),
        ("广西北部湾投资集团有限公司", "北部湾投资", "投资"),
        ("广西国宏经济发展集团有限公司", "国宏集团", "综合"),
        ("广西国控资本运营集团有限责任公司", "国控资本", "投资"),
        ("广西宏桂资本运营集团有限公司", "宏桂资本", "投资"),
        ("广西投资集团有限公司", "广西投资集团", "投资"),
        ("广西旅游发展集团有限公司", "广西旅游集团", "旅游"),
        ("广西机场管理集团有限责任公司", "广西机场", "交通"),
        ("广西林业集团有限公司", "广西林业", "林业"),
        ("广西柳州钢铁集团有限公司", "柳钢集团", "冶金"),
        ("广西柳工集团有限公司", "柳工集团", "制造"),
        ("广西汽车集团有限公司", "广西汽车", "汽车"),
        ("广西玉柴机器集团有限公司", "玉柴集团", "制造"),
        ("广西现代物流集团有限公司", "广西物流", "物流"),
    ]
    return [make_row("GX", f, s, sector=sec,
                     caliber="supervised",
                     caliber_label="省国资委监管企业",
                     page_type="LIST-A", completeness="full_list",
                     confidence=0.95, uev=1,
                     notes="官方广西国企列表")
            for f, s, sec in items]


def jiangxi_data():
    """11 enterprises from list page at gzw.jiangxi.gov.cn"""
    items = [
        ("江西省交通投资集团有限公司", "江西交投集团", "交通"),
        ("江西省军工控股集团有限公司", "江西军工集团", "制造"),
        ("江西国泰集团有限责任公司", "江西国泰集团", "综合"),
        ("江西省建工集团有限责任公司", "江西建工集团", "建筑"),
        ("江西省建材集团有限公司", "江西建材集团", "建材"),
        ("江西省投资集团有限公司", "江西投资集团", "投资"),
        ("江西省港口集团有限公司", "江西港口集团", "交通"),
        ("江西省盐业集团股份有限公司", "江西盐业集团", "轻工"),
        ("江西铜业集团有限公司", "江西铜业集团", "冶金"),
        ("江西省长天旅游集团有限公司", "江西长旅集团", "旅游"),
        ("江钨控股集团有限公司", "江钨控股集团", "冶金"),
    ]
    return [make_row("JX", f, s, sector=sec,
                     caliber="supervised",
                     caliber_label="省国资委省属企业",
                     page_type="LIST-A", completeness="full_list",
                     confidence=0.85, uev=2, review=True,
                     notes="官方省属企业名录(短名推断全名)")
            for f, s, sec in items]


def shaanxi_data():
    """18 enterprises from 国企之窗 at sxgz.shaanxi.gov.cn"""
    items = [
        ("陕西煤业化工集团有限责任公司", "陕煤集团", "矿业"),
        ("延长石油（集团）有限责任公司", "延长石油", "能源"),
        ("陕西有色金属控股集团有限责任公司", "陕西有色金属集团", "冶金"),
        ("陕西建工控股集团有限公司", "陕建控股", "建筑"),
        ("陕西投资集团有限公司", "陕投集团", "投资"),
        ("法士特集团有限责任公司", "法士特集团", "汽车"),
        ("陕西汽车控股集团有限公司", "陕汽控股", "汽车"),
        ("西部机场集团有限公司", "西部机场", "交通"),
        ("秦川机床工具集团股份公司", "秦川集团", "制造"),
        ("陕西交通控股集团有限公司", "陕西交控", "交通"),
        ("陕西地矿集团有限公司", "陕西地矿", "矿业"),
        ("陕西旅游集团有限公司", "陕旅集团", "旅游"),
        ("中陕核工业集团有限公司", "中陕核", "能源"),
        ("陕西环保集团有限责任公司", "陕西环保集团", "环保"),
        ("陕西农业发展集团有限公司", "陕西农发集团", "农业"),
        ("陕西水务发展集团有限公司", "陕西水务发展集团", "水利"),
        ("陕西电子信息集团有限公司", "陕西电子", "电子"),
        ("陕西数字经济集团有限公司", "陕数集团", "数据"),
    ]
    return [make_row("SN", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别省属企业(从国企之窗识别)",
                     page_type="NEWS", completeness="full_list",
                     confidence=0.80, uev=2, review=True,
                     notes="从国企之窗企业动态栏目识别")
            for f, s, sec in items]


def xinjiang_bingtuan_data():
    """6 enterprises from news at gyzc.xjbt.gov.cn"""
    items = [
        ("中新建物流集团有限责任公司", "中新建物流集团", "物流"),
        ("中新建电力集团有限公司", "中新建电力集团", "能源"),
        ("新疆中新建数字发展有限责任公司", "中新建数字发展", "数据"),
        ("新疆兵投供应链管理有限责任公司", "兵投供应链", "物流"),
        ("新疆兵投检验检测有限责任公司", "兵投检验检测", "服务"),
        ("新疆昆仑纺织服装有限责任公司", "昆仑纺织", "轻工"),
    ]
    return [make_row("BT", f, s, sector=sec,
                     caliber="identifiable",
                     caliber_label="公开可识别兵团企业(从新闻识别)",
                     page_type="NEWS", completeness="partial_identified",
                     confidence=0.60, uev=3, review=True,
                     notes="从新疆兵团国资委新闻识别")
            for f, s, sec in items]


# ─── Existing province data (keep as-is from CSV) ─────────────────
def read_existing_csv():
    """Read existing CSV and return rows for provinces we won't replace."""
    rows = []
    with open(OUTPUT_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


# ─── Main generation ──────────────────────────────────────────────
def build_all_rows():
    """Combine existing data with new crawled data."""
    # Read existing data
    existing = read_existing_csv()

    # Provinces already in existing CSV that we'll KEEP as-is
    keep_codes = {"GD", "ZJ", "SD", "SC"}

    # Provinces already in existing CSV that we'll REPLACE with better data
    replace_codes = set()  # Not replacing any for now, all existing data is fine

    kept_rows = [r for r in existing if r["province_code"] in keep_codes]

    # New province data generators
    new_data_funcs = [
        beijing_data,
        tianjin_data,
        hebei_data,
        liaoning_data,
        neimenggu_data,
        shanghai_data,
        jiangsu_data,
        hunan_data,
        xinjiang_data,
        ningxia_data,
        hainan_data,
        chongqing_data,
        anhui_data,
        shanxi_data,
        jilin_data,
        heilongjiang_data,
        fujian_data,
        jiangxi_data,
        henan_data,
        guangxi_data,
        guizhou_data,
        yunnan_data,
        shaanxi_data,
        xinjiang_bingtuan_data,
    ]

    # Build new rows
    new_rows = []
    for func in new_data_funcs:
        new_rows.extend(func())

    # Convert new rows to full CSV dict format
    all_rows = []

    # First, kept rows (already in proper format)
    for r in kept_rows:
        all_rows.append(r)

    # Then new rows
    for r in new_rows:
        all_rows.append(r)

    # Sort by province_code alphabetically, then by entity_name_full
    province_order = list(PROVINCES.keys())
    all_rows.sort(key=lambda r: (
        province_order.index(r["province_code"]) if r["province_code"] in province_order else 99,
        r.get("admin_level", "L1"),
        r.get("entity_name_full", ""),
    ))

    # Assign entity_ids
    counters = {}
    final_rows = []
    for r in all_rows:
        code = r["province_code"]
        admin = r.get("admin_level", "L1")
        if admin == "L2":
            key = f"{code}-L2"
        else:
            key = code
        counters.setdefault(key, 0)
        counters[key] += 1
        if admin == "L2":
            eid = f"E-{code}-L2-{counters[key]:04d}"
        else:
            eid = f"E-{code}-{counters[key]:04d}"

        final_row = {
            "entity_id": eid,
            "province": r.get("province", PROVINCES.get(code, "")),
            "province_code": code,
            "admin_level": r.get("admin_level", "L1"),
            "city": r.get("city", ""),
            "entity_name_full": r.get("entity_name_full", ""),
            "entity_name_short": r.get("entity_name_short", ""),
            "list_caliber": r.get("list_caliber", ""),
            "list_caliber_label": r.get("list_caliber_label", ""),
            "source_institution": r.get("source_institution", f"{PROVINCES.get(code, '')}国资委"),
            "source_url": r.get("source_url", SASAC_URLS.get(code, "")),
            "source_page_type": r.get("source_page_type", ""),
            "extraction_date": r.get("extraction_date", TODAY),
            "list_publish_date": r.get("list_publish_date", ""),
            "sector": r.get("sector", ""),
            "includes_financial": r.get("includes_financial", "FALSE"),
            "completeness": r.get("completeness", ""),
            "confidence": r.get("confidence", ""),
            "uev_level": r.get("uev_level", ""),
            "needs_manual_review": r.get("needs_manual_review", "FALSE"),
            "notes": r.get("notes", ""),
        }
        # Normalize booleans
        for bk in ("includes_financial", "needs_manual_review"):
            v = final_row[bk]
            if isinstance(v, bool):
                final_row[bk] = "TRUE" if v else "FALSE"
            elif str(v).lower() in ("true", "1"):
                final_row[bk] = "TRUE"
            else:
                final_row[bk] = "FALSE"

        final_rows.append(final_row)

    return final_rows


FIELDNAMES = [
    "entity_id", "province", "province_code", "admin_level", "city",
    "entity_name_full", "entity_name_short", "list_caliber", "list_caliber_label",
    "source_institution", "source_url", "source_page_type", "extraction_date",
    "list_publish_date", "sector", "includes_financial", "completeness",
    "confidence", "uev_level", "needs_manual_review", "notes",
]


def write_csv(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Written {len(rows)} rows → {path}")


def main():
    print("=" * 60)
    print("地方国资企业名录 CSV 生成工具")
    print("=" * 60)

    rows = build_all_rows()

    # Stats
    provinces = set(r["province_code"] for r in rows)
    print(f"\n总计: {len(rows)} 条企业记录, 覆盖 {len(provinces)} 个省份")
    for code in sorted(provinces, key=lambda c: list(PROVINCES.keys()).index(c) if c in PROVINCES else 99):
        prows = [r for r in rows if r["province_code"] == code]
        print(f"  {PROVINCES.get(code, code):6s}: {len(prows):3d} 家企业")

    # Write delivery CSV
    write_csv(rows, OUTPUT_PATH)

    # Write site copy
    write_csv(rows, SITE_COPY)

    print("\n✓ 生成完成")


if __name__ == "__main__":
    main()
