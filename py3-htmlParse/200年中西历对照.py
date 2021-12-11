#! /usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import osLib
import pprint
import requests
import html2text
import tranJulianDay
from lxml import etree
import csv

empReigns = [{'dyna': '西漢', 'king': '平帝', 'reign': '元始'},
             {'dyna': '西漢', 'king': '孺子嬰', 'reign': '居攝'},
             {'dyna': '西漢', 'king': '孺子嬰', 'reign': '初始'},
             {'dyna': '新', 'king': '王莽', 'reign': '始建國'},
             {'dyna': '新', 'king': '王莽', 'reign': '天鳳'},
             {'dyna': '新', 'king': '王莽', 'reign': '地皇'},
             {'dyna': '更始朝', 'king': '淮陽王', 'reign': '更始'},
             {'dyna': '東漢', 'king': '光武帝', 'reign': '建武'},
             {'dyna': '東漢', 'king': '光武帝', 'reign': '建武中元'},
             {'dyna': '東漢', 'king': '明帝', 'reign': '永平'},
             {'dyna': '東漢', 'king': '章帝', 'reign': '建初'},
             {'dyna': '東漢', 'king': '章帝', 'reign': '元和'},
             {'dyna': '東漢', 'king': '章帝', 'reign': '章和'},
             {'dyna': '東漢', 'king': '和帝', 'reign': '永元'},
             {'dyna': '東漢', 'king': '和帝', 'reign': '元興'},
             {'dyna': '東漢', 'king': '殤帝', 'reign': '延平'},
             {'dyna': '東漢', 'king': '安帝', 'reign': '永初'},
             {'dyna': '東漢', 'king': '安帝', 'reign': '元初'},
             {'dyna': '東漢', 'king': '安帝', 'reign': '永寧'},
             {'dyna': '東漢', 'king': '安帝', 'reign': '建光'},
             {'dyna': '東漢', 'king': '安帝', 'reign': '延光'},
             {'dyna': '東漢', 'king': '北鄉侯', 'reign': '延光'},
             {'dyna': '東漢', 'king': '順帝', 'reign': '永建'},
             {'dyna': '東漢', 'king': '順帝', 'reign': '陽嘉'},
             {'dyna': '東漢', 'king': '順帝', 'reign': '永和'},
             {'dyna': '東漢', 'king': '順帝', 'reign': '漢安'},
             {'dyna': '東漢', 'king': '順帝', 'reign': '建康'},
             {'dyna': '東漢', 'king': '沖帝', 'reign': '永嘉'},
             {'dyna': '東漢', 'king': '質帝', 'reign': '本初'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '建和'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '和平'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '元嘉'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '永興'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '永壽'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '延熹'},
             {'dyna': '東漢', 'king': '桓帝', 'reign': '永康'},
             {'dyna': '東漢', 'king': '靈帝', 'reign': '建寧'},
             {'dyna': '東漢', 'king': '靈帝', 'reign': '熹平'},
             {'dyna': '東漢', 'king': '靈帝', 'reign': '光和'},
             {'dyna': '東漢', 'king': '靈帝', 'reign': '中平'},
             {'dyna': '東漢', 'king': '少帝', 'reign': '光熹'},
             {'dyna': '東漢', 'king': '少帝', 'reign': '昭寧'},
             {'dyna': '東漢', 'king': '獻帝', 'reign': '永漢'},
             {'dyna': '東漢', 'king': '獻帝', 'reign': '中平'},
             {'dyna': '東漢', 'king': '獻帝', 'reign': '初平'},
             {'dyna': '東漢', 'king': '獻帝', 'reign': '興平'},
             {'dyna': '東漢', 'king': '獻帝', 'reign': '建安'},
             {'dyna': '東漢', 'king': '獻帝', 'reign': '延康'},
             {'dyna': '魏', 'king': '文帝', 'reign': '黃初'},
             {'dyna': '魏', 'king': '明帝', 'reign': '太和'},
             {'dyna': '魏', 'king': '明帝', 'reign': '青龍'},
             {'dyna': '魏', 'king': '明帝', 'reign': '景初'},
             {'dyna': '魏', 'king': '少帝', 'reign': '正始'},
             {'dyna': '魏', 'king': '少帝', 'reign': '嘉平'},
             {'dyna': '魏', 'king': '高貴鄉公', 'reign': '正元'},
             {'dyna': '魏', 'king': '高貴鄉公', 'reign': '甘露'},
             {'dyna': '魏', 'king': '元帝', 'reign': '景元'},
             {'dyna': '魏', 'king': '元帝', 'reign': '咸熙'},
             {'dyna': '蜀', 'king': '昭烈帝', 'reign': '章武'},
             {'dyna': '蜀', 'king': '後主', 'reign': '建興'},
             {'dyna': '蜀', 'king': '後主', 'reign': '延熙'},
             {'dyna': '蜀', 'king': '後主', 'reign': '景耀'},
             {'dyna': '蜀', 'king': '後主', 'reign': '炎興'},
             {'dyna': '吳', 'king': '大帝', 'reign': '黃武'},
             {'dyna': '吳', 'king': '大帝', 'reign': '黃龍'},
             {'dyna': '吳', 'king': '大帝', 'reign': '嘉禾'},
             {'dyna': '吳', 'king': '大帝', 'reign': '赤烏'},
             {'dyna': '吳', 'king': '大帝', 'reign': '太元'},
             {'dyna': '吳', 'king': '大帝', 'reign': '神鳳'},
             {'dyna': '吳', 'king': '會稽王', 'reign': '建興'},
             {'dyna': '吳', 'king': '會稽王', 'reign': '五鳳'},
             {'dyna': '吳', 'king': '會稽王', 'reign': '太平'},
             {'dyna': '吳', 'king': '景帝', 'reign': '永安'},
             {'dyna': '吳', 'king': '末帝', 'reign': '元興'},
             {'dyna': '吳', 'king': '末帝', 'reign': '甘露'},
             {'dyna': '吳', 'king': '末帝', 'reign': '寶鼎'},
             {'dyna': '吳', 'king': '末帝', 'reign': '建衡'},
             {'dyna': '吳', 'king': '末帝', 'reign': '鳳凰'},
             {'dyna': '吳', 'king': '末帝', 'reign': '天冊'},
             {'dyna': '吳', 'king': '末帝', 'reign': '天璽'},
             {'dyna': '吳', 'king': '末帝', 'reign': '天紀'},
             {'dyna': '西晉', 'king': '武帝', 'reign': '泰始'},
             {'dyna': '西晉', 'king': '武帝', 'reign': '咸寧'},
             {'dyna': '西晉', 'king': '武帝', 'reign': '太康'},
             {'dyna': '西晉', 'king': '武帝', 'reign': '太熙'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永熙'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永平'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '元康'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永康'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永寧'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '太安'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永安'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '建武'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永安(復稱)'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '永興'},
             {'dyna': '西晉', 'king': '惠帝', 'reign': '光熙'},
             {'dyna': '西晉', 'king': '懷帝', 'reign': '永嘉'},
             {'dyna': '西晉', 'king': '愍帝', 'reign': '建興'},
             {'dyna': '東晉', 'king': '元帝', 'reign': '建武'},
             {'dyna': '東晉', 'king': '元帝', 'reign': '太興'},
             {'dyna': '東晉', 'king': '元帝', 'reign': '永昌'},
             {'dyna': '東晉', 'king': '明帝', 'reign': '太寧'},
             {'dyna': '東晉', 'king': '成帝', 'reign': '咸和'},
             {'dyna': '東晉', 'king': '成帝', 'reign': '咸康'},
             {'dyna': '東晉', 'king': '康帝', 'reign': '建元'},
             {'dyna': '東晉', 'king': '穆帝', 'reign': '永和'},
             {'dyna': '東晉', 'king': '穆帝', 'reign': '升平'},
             {'dyna': '東晉', 'king': '哀帝', 'reign': '隆和'},
             {'dyna': '東晉', 'king': '哀帝', 'reign': '興寧'},
             {'dyna': '東晉', 'king': '海西公', 'reign': '太和'},
             {'dyna': '東晉', 'king': '簡文帝', 'reign': '咸安'},
             {'dyna': '東晉', 'king': '孝武帝', 'reign': '寧康'},
             {'dyna': '東晉', 'king': '孝武帝', 'reign': '太元'},
             {'dyna': '東晉', 'king': '安帝', 'reign': '隆安'},
             {'dyna': '東晉', 'king': '安帝', 'reign': '元興'},
             {'dyna': '東晉', 'king': '安帝', 'reign': '義熙'},
             {'dyna': '東晉', 'king': '恭帝', 'reign': '元熙'},
             {'dyna': '前宋', 'king': '武帝', 'reign': '永初'},
             {'dyna': '前宋', 'king': '營陽王', 'reign': '景平'},
             {'dyna': '前宋', 'king': '文帝', 'reign': '元嘉'},
             {'dyna': '前宋', 'king': '孝武帝', 'reign': '孝建'},
             {'dyna': '前宋', 'king': '孝武帝', 'reign': '大明'},
             {'dyna': '前宋', 'king': '前廢帝', 'reign': '永光'},
             {'dyna': '前宋', 'king': '前廢帝', 'reign': '景和'},
             {'dyna': '前宋', 'king': '明帝', 'reign': '泰始'},
             {'dyna': '前宋', 'king': '明帝', 'reign': '泰豫'},
             {'dyna': '前宋', 'king': '蒼梧王', 'reign': '元徽'},
             {'dyna': '前宋', 'king': '順帝', 'reign': '昇明'},
             {'dyna': '南齊', 'king': '高帝', 'reign': '建元'},
             {'dyna': '南齊', 'king': '武帝', 'reign': '永明'},
             {'dyna': '南齊', 'king': '鬱林王', 'reign': '隆昌'},
             {'dyna': '南齊', 'king': '海陵王', 'reign': '延興'},
             {'dyna': '南齊', 'king': '明帝', 'reign': '建武'},
             {'dyna': '南齊', 'king': '明帝', 'reign': '永泰'},
             {'dyna': '南齊', 'king': '東昏侯', 'reign': '永元'},
             {'dyna': '南齊', 'king': '和帝', 'reign': '中興'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '天監'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '普通'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '大通'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '中大通'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '大同'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '中大同'},
             {'dyna': '南梁', 'king': '武帝', 'reign': '太清'},
             {'dyna': '南梁', 'king': '簡文帝', 'reign': '大寶'},
             {'dyna': '南梁', 'king': '豫章王', 'reign': '天正'},
             {'dyna': '南梁', 'king': '元帝', 'reign': '承聖'},
             {'dyna': '南梁', 'king': '貞陽侯', 'reign': '天成'},
             {'dyna': '南梁', 'king': '敬帝', 'reign': '紹泰'},
             {'dyna': '南梁', 'king': '敬帝', 'reign': '太平'},
             {'dyna': '陳', 'king': '武帝', 'reign': '永定'},
             {'dyna': '陳', 'king': '文帝', 'reign': '天嘉'},
             {'dyna': '陳', 'king': '文帝', 'reign': '天康'},
             {'dyna': '陳', 'king': '臨海王', 'reign': '光大'},
             {'dyna': '陳', 'king': '宣帝', 'reign': '太建'},
             {'dyna': '陳', 'king': '後主', 'reign': '至德'},
             {'dyna': '陳', 'king': '後主', 'reign': '禎明'},
             {'dyna': '北魏', 'king': '道武帝', 'reign': '登國'},
             {'dyna': '北魏', 'king': '道武帝', 'reign': '皇始'},
             {'dyna': '北魏', 'king': '道武帝', 'reign': '天興'},
             {'dyna': '北魏', 'king': '道武帝', 'reign': '天賜'},
             {'dyna': '北魏', 'king': '明元帝', 'reign': '永興'},
             {'dyna': '北魏', 'king': '明元帝', 'reign': '神瑞'},
             {'dyna': '北魏', 'king': '明元帝', 'reign': '泰常'},
             {'dyna': '北魏', 'king': '太武帝', 'reign': '始光'},
             {'dyna': '北魏', 'king': '太武帝', 'reign': '神䴥'},
             {'dyna': '北魏', 'king': '太武帝', 'reign': '延和'},
             {'dyna': '北魏', 'king': '太武帝', 'reign': '太延'},
             {'dyna': '北魏', 'king': '太武帝', 'reign': '太平真君'},
             {'dyna': '北魏', 'king': '太武帝', 'reign': '正平'},
             {'dyna': '北魏', 'king': '南安王', 'reign': '承平'},
             {'dyna': '北魏', 'king': '文成帝', 'reign': '興安'},
             {'dyna': '北魏', 'king': '文成帝', 'reign': '興光'},
             {'dyna': '北魏', 'king': '文成帝', 'reign': '太安'},
             {'dyna': '北魏', 'king': '文成帝', 'reign': '和平'},
             {'dyna': '北魏', 'king': '獻文帝', 'reign': '天安'},
             {'dyna': '北魏', 'king': '獻文帝', 'reign': '皇興'},
             {'dyna': '北魏', 'king': '孝文帝', 'reign': '延興'},
             {'dyna': '北魏', 'king': '孝文帝', 'reign': '承明'},
             {'dyna': '北魏', 'king': '孝文帝', 'reign': '太和'},
             {'dyna': '北魏', 'king': '宣武帝', 'reign': '景明'},
             {'dyna': '北魏', 'king': '宣武帝', 'reign': '正始'},
             {'dyna': '北魏', 'king': '宣武帝', 'reign': '永平'},
             {'dyna': '北魏', 'king': '宣武帝', 'reign': '延昌'},
             {'dyna': '北魏', 'king': '孝明帝', 'reign': '熙平'},
             {'dyna': '北魏', 'king': '孝明帝', 'reign': '神龜'},
             {'dyna': '北魏', 'king': '孝明帝', 'reign': '正光'},
             {'dyna': '北魏', 'king': '孝明帝', 'reign': '孝昌'},
             {'dyna': '北魏', 'king': '孝明帝', 'reign': '武泰'},
             {'dyna': '北魏', 'king': '孝莊帝', 'reign': '建義'},
             {'dyna': '北魏', 'king': '孝莊帝', 'reign': '永安'},
             {'dyna': '北魏', 'king': '長廣王', 'reign': '建明'},
             {'dyna': '北魏', 'king': '節閔帝', 'reign': '普泰'},
             {'dyna': '北魏', 'king': '安定王', 'reign': '中興'},
             {'dyna': '北魏', 'king': '孝武帝', 'reign': '太昌'},
             {'dyna': '北魏', 'king': '孝武帝', 'reign': '永興'},
             {'dyna': '北魏', 'king': '孝武帝', 'reign': '永熙'},
             {'dyna': '西魏', 'king': '文帝', 'reign': '大統'},
             {'dyna': '東魏', 'king': '孝靜帝', 'reign': '天平'},
             {'dyna': '東魏', 'king': '孝靜帝', 'reign': '元象'},
             {'dyna': '東魏', 'king': '孝靜帝', 'reign': '興和'},
             {'dyna': '東魏', 'king': '孝靜帝', 'reign': '武定'},
             {'dyna': '北齊', 'king': '文宣帝', 'reign': '天保'},
             {'dyna': '北齊', 'king': '廢帝', 'reign': '乾明'},
             {'dyna': '北齊', 'king': '孝昭帝', 'reign': '皇建'},
             {'dyna': '北齊', 'king': '武成帝', 'reign': '大寧'},
             {'dyna': '北齊', 'king': '武成帝', 'reign': '河清'},
             {'dyna': '北齊', 'king': '後主', 'reign': '天統'},
             {'dyna': '北齊', 'king': '後主', 'reign': '武平'},
             {'dyna': '北齊', 'king': '後主', 'reign': '隆化'},
             {'dyna': '北齊', 'king': '幼主', 'reign': '承光'},
             {'dyna': '北周', 'king': '明帝', 'reign': '*'},
             {'dyna': '北周', 'king': '明帝', 'reign': '武成'},
             {'dyna': '北周', 'king': '武帝', 'reign': '保定'},
             {'dyna': '北周', 'king': '武帝', 'reign': '天和'},
             {'dyna': '北周', 'king': '武帝', 'reign': '建德'},
             {'dyna': '北周', 'king': '武帝', 'reign': '宣政'},
             {'dyna': '北周', 'king': '宣帝', 'reign': '大成'},
             {'dyna': '北周', 'king': '靜帝', 'reign': '大象'},
             {'dyna': '北周', 'king': '靜帝', 'reign': '大定'},
             {'dyna': '隋', 'king': '文帝', 'reign': '開皇'},
             {'dyna': '隋', 'king': '文帝', 'reign': '仁壽'},
             {'dyna': '隋', 'king': '煬帝', 'reign': '大業'},
             {'dyna': '隋', 'king': '恭帝', 'reign': '義寧'},
             {'dyna': '唐', 'king': '高祖', 'reign': '武德'},
             {'dyna': '唐', 'king': '太宗', 'reign': '貞觀'},
             {'dyna': '唐', 'king': '高宗', 'reign': '永徽'},
             {'dyna': '唐', 'king': '高宗', 'reign': '顯慶'},
             {'dyna': '唐', 'king': '高宗', 'reign': '龍朔'},
             {'dyna': '唐', 'king': '高宗', 'reign': '麟德'},
             {'dyna': '唐', 'king': '高宗', 'reign': '乾封'},
             {'dyna': '唐', 'king': '高宗', 'reign': '總章'},
             {'dyna': '唐', 'king': '高宗', 'reign': '咸亨'},
             {'dyna': '唐', 'king': '高宗', 'reign': '上元'},
             {'dyna': '唐', 'king': '高宗', 'reign': '儀鳳'},
             {'dyna': '唐', 'king': '高宗', 'reign': '調露'},
             {'dyna': '唐', 'king': '高宗', 'reign': '永隆'},
             {'dyna': '唐', 'king': '高宗', 'reign': '開耀'},
             {'dyna': '唐', 'king': '高宗', 'reign': '永淳'},
             {'dyna': '唐', 'king': '高宗', 'reign': '弘道'},
             {'dyna': '唐', 'king': '中宗', 'reign': '嗣聖'},
             {'dyna': '唐', 'king': '睿宗', 'reign': '文明'},
             {'dyna': '唐', 'king': '武后', 'reign': '光宅'},
             {'dyna': '唐', 'king': '武后', 'reign': '垂拱'},
             {'dyna': '唐', 'king': '武后', 'reign': '永昌'},
             {'dyna': '唐', 'king': '武后', 'reign': '載初'},
             {'dyna': '唐', 'king': '武后', 'reign': '天授'},
             {'dyna': '唐', 'king': '武后', 'reign': '如意'},
             {'dyna': '唐', 'king': '武后', 'reign': '長壽'},
             {'dyna': '唐', 'king': '武后', 'reign': '延載'},
             {'dyna': '唐', 'king': '武后', 'reign': '證聖'},
             {'dyna': '唐', 'king': '武后', 'reign': '天冊萬歲'},
             {'dyna': '唐', 'king': '武后', 'reign': '萬歲登封'},
             {'dyna': '唐', 'king': '武后', 'reign': '萬歲通天'},
             {'dyna': '唐', 'king': '武后', 'reign': '神功'},
             {'dyna': '唐', 'king': '武后', 'reign': '聖曆'},
             {'dyna': '唐', 'king': '武后', 'reign': '久視'},
             {'dyna': '唐', 'king': '武后', 'reign': '大足'},
             {'dyna': '唐', 'king': '武后', 'reign': '長安'},
             {'dyna': '唐', 'king': '武后', 'reign': '神龍'},
             {'dyna': '唐', 'king': '中宗', 'reign': '神龍'},
             {'dyna': '唐', 'king': '中宗', 'reign': '景龍'},
             {'dyna': '唐', 'king': '殤帝', 'reign': '唐隆'},
             {'dyna': '唐', 'king': '睿宗', 'reign': '景雲'},
             {'dyna': '唐', 'king': '睿宗', 'reign': '太極'},
             {'dyna': '唐', 'king': '睿宗', 'reign': '延和'},
             {'dyna': '唐', 'king': '玄宗', 'reign': '先天'},
             {'dyna': '唐', 'king': '玄宗', 'reign': '開元'},
             {'dyna': '唐', 'king': '玄宗', 'reign': '天寶'},
             {'dyna': '唐', 'king': '肅宗', 'reign': '至德'},
             {'dyna': '唐', 'king': '肅宗', 'reign': '乾元'},
             {'dyna': '唐', 'king': '肅宗', 'reign': '上元'},
             {'dyna': '唐', 'king': '肅宗', 'reign': '*'},
             {'dyna': '唐', 'king': '肅宗', 'reign': '寶應'},
             {'dyna': '唐', 'king': '代宗', 'reign': '廣德'},
             {'dyna': '唐', 'king': '代宗', 'reign': '永泰'},
             {'dyna': '唐', 'king': '代宗', 'reign': '大曆'},
             {'dyna': '唐', 'king': '德宗', 'reign': '建中'},
             {'dyna': '唐', 'king': '德宗', 'reign': '興元'},
             {'dyna': '唐', 'king': '德宗', 'reign': '貞元'},
             {'dyna': '唐', 'king': '順宗', 'reign': '永貞'},
             {'dyna': '唐', 'king': '憲宗', 'reign': '元和'},
             {'dyna': '唐', 'king': '穆宗', 'reign': '長慶'},
             {'dyna': '唐', 'king': '敬宗', 'reign': '寶曆'},
             {'dyna': '唐', 'king': '文宗', 'reign': '太和'},
             {'dyna': '唐', 'king': '文宗', 'reign': '開成'},
             {'dyna': '唐', 'king': '武宗', 'reign': '會昌'},
             {'dyna': '唐', 'king': '宣宗', 'reign': '大中'},
             {'dyna': '唐', 'king': '懿宗', 'reign': '咸通'},
             {'dyna': '唐', 'king': '僖宗', 'reign': '乾符'},
             {'dyna': '唐', 'king': '僖宗', 'reign': '廣明'},
             {'dyna': '唐', 'king': '僖宗', 'reign': '中和'},
             {'dyna': '唐', 'king': '僖宗', 'reign': '光啟'},
             {'dyna': '唐', 'king': '僖宗', 'reign': '文德'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '龍紀'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '大順'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '景福'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '乾寧'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '光化'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '天復'},
             {'dyna': '唐', 'king': '昭宗', 'reign': '天祐'},
             {'dyna': '唐', 'king': '哀帝', 'reign': '天祐'},
             {'dyna': '後梁', 'king': '太祖', 'reign': '開平'},
             {'dyna': '後梁', 'king': '太祖', 'reign': '乾化'},
             {'dyna': '後梁', 'king': '郢王', 'reign': '鳳曆'},
             {'dyna': '後梁', 'king': '末帝', 'reign': '乾化'},
             {'dyna': '後梁', 'king': '末帝', 'reign': '貞明'},
             {'dyna': '後梁', 'king': '末帝', 'reign': '龍德'},
             {'dyna': '後唐', 'king': '莊宗', 'reign': '同光'},
             {'dyna': '後唐', 'king': '明宗', 'reign': '天成'},
             {'dyna': '後唐', 'king': '明宗', 'reign': '長興'},
             {'dyna': '後唐', 'king': '閔帝', 'reign': '應順'},
             {'dyna': '後唐', 'king': '廢帝', 'reign': '清泰'},
             {'dyna': '後晉', 'king': '高祖', 'reign': '天福'},
             {'dyna': '後晉', 'king': '出帝', 'reign': '天福'},
             {'dyna': '後晉', 'king': '出帝', 'reign': '開運'},
             {'dyna': '後漢', 'king': '高祖', 'reign': '天福'},
             {'dyna': '後漢', 'king': '高祖', 'reign': '乾祐'},
             {'dyna': '後漢', 'king': '隱帝', 'reign': '乾祐'},
             {'dyna': '後周', 'king': '太祖', 'reign': '廣順'},
             {'dyna': '後周', 'king': '太祖', 'reign': '顯德'},
             {'dyna': '後周', 'king': '世宗', 'reign': '顯德'},
             {'dyna': '後周', 'king': '恭帝', 'reign': '顯德'},
             {'dyna': '宋', 'king': '太祖', 'reign': '建隆'},
             {'dyna': '宋', 'king': '太祖', 'reign': '乾德'},
             {'dyna': '宋', 'king': '太祖', 'reign': '開寶'},
             {'dyna': '宋', 'king': '太宗', 'reign': '太平興國'},
             {'dyna': '宋', 'king': '太宗', 'reign': '雍熙'},
             {'dyna': '宋', 'king': '太宗', 'reign': '端拱'},
             {'dyna': '宋', 'king': '太宗', 'reign': '淳化'},
             {'dyna': '宋', 'king': '太宗', 'reign': '至道'},
             {'dyna': '宋', 'king': '真宗', 'reign': '咸平'},
             {'dyna': '宋', 'king': '真宗', 'reign': '景德'},
             {'dyna': '宋', 'king': '真宗', 'reign': '大中祥符'},
             {'dyna': '宋', 'king': '真宗', 'reign': '天禧'},
             {'dyna': '宋', 'king': '真宗', 'reign': '乾興'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '天聖'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '明道'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '景祐'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '寶元'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '康定'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '慶曆'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '皇祐'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '至和'},
             {'dyna': '宋', 'king': '仁宗', 'reign': '嘉祐'},
             {'dyna': '宋', 'king': '英宗', 'reign': '治平'},
             {'dyna': '宋', 'king': '神宗', 'reign': '熙寧'},
             {'dyna': '宋', 'king': '神宗', 'reign': '元豐'},
             {'dyna': '宋', 'king': '哲宗', 'reign': '元祐'},
             {'dyna': '宋', 'king': '哲宗', 'reign': '紹聖'},
             {'dyna': '宋', 'king': '哲宗', 'reign': '元符'},
             {'dyna': '宋', 'king': '徽宗', 'reign': '建中靖國'},
             {'dyna': '宋', 'king': '徽宗', 'reign': '崇寧'},
             {'dyna': '宋', 'king': '徽宗', 'reign': '大觀'},
             {'dyna': '宋', 'king': '徽宗', 'reign': '政和'},
             {'dyna': '宋', 'king': '徽宗', 'reign': '重和'},
             {'dyna': '宋', 'king': '徽宗', 'reign': '宣和'},
             {'dyna': '宋', 'king': '欽宗', 'reign': '靖康'},
             {'dyna': '宋', 'king': '高宗', 'reign': '建炎'},
             {'dyna': '宋', 'king': '高宗', 'reign': '紹興'},
             {'dyna': '宋', 'king': '孝宗', 'reign': '隆興'},
             {'dyna': '宋', 'king': '孝宗', 'reign': '乾道'},
             {'dyna': '宋', 'king': '孝宗', 'reign': '淳熙'},
             {'dyna': '宋', 'king': '光宗', 'reign': '紹熙'},
             {'dyna': '宋', 'king': '寧宗', 'reign': '慶元'},
             {'dyna': '宋', 'king': '寧宗', 'reign': '嘉泰'},
             {'dyna': '宋', 'king': '寧宗', 'reign': '開禧'},
             {'dyna': '宋', 'king': '寧宗', 'reign': '嘉定'},
             {'dyna': '宋', 'king': '理宗', 'reign': '寶慶'},
             {'dyna': '宋', 'king': '理宗', 'reign': '紹定'},
             {'dyna': '宋', 'king': '理宗', 'reign': '端平'},
             {'dyna': '宋', 'king': '理宗', 'reign': '嘉熙'},
             {'dyna': '宋', 'king': '理宗', 'reign': '淳祐'},
             {'dyna': '宋', 'king': '理宗', 'reign': '寶祐'},
             {'dyna': '宋', 'king': '理宗', 'reign': '開慶'},
             {'dyna': '宋', 'king': '理宗', 'reign': '景定'},
             {'dyna': '宋', 'king': '度宗', 'reign': '咸淳'},
             {'dyna': '宋', 'king': '恭宗', 'reign': '德祐'},
             {'dyna': '宋', 'king': '端宗', 'reign': '景炎'},
             {'dyna': '宋', 'king': '昺帝', 'reign': '祥興'},
             {'dyna': '遼', 'king': '太祖', 'reign': '*'},
             {'dyna': '遼', 'king': '太祖', 'reign': '神冊'},
             {'dyna': '遼', 'king': '太祖', 'reign': '天贊'},
             {'dyna': '遼', 'king': '太祖', 'reign': '天顯'},
             {'dyna': '遼', 'king': '太宗', 'reign': '天顯'},
             {'dyna': '遼', 'king': '太宗', 'reign': '會同'},
             {'dyna': '遼', 'king': '太宗', 'reign': '大同'},
             {'dyna': '遼', 'king': '世宗', 'reign': '天祿'},
             {'dyna': '遼', 'king': '穆宗', 'reign': '應曆'},
             {'dyna': '遼', 'king': '景宗', 'reign': '保寧'},
             {'dyna': '遼', 'king': '景宗', 'reign': '乾亨'},
             {'dyna': '遼', 'king': '聖宗', 'reign': '統和'},
             {'dyna': '遼', 'king': '聖宗', 'reign': '開泰'},
             {'dyna': '遼', 'king': '聖宗', 'reign': '太平'},
             {'dyna': '遼', 'king': '興宗', 'reign': '景福'},
             {'dyna': '遼', 'king': '興宗', 'reign': '重熙'},
             {'dyna': '遼', 'king': '道宗', 'reign': '清寧'},
             {'dyna': '遼', 'king': '道宗', 'reign': '咸雍'},
             {'dyna': '遼', 'king': '道宗', 'reign': '大康'},
             {'dyna': '遼', 'king': '道宗', 'reign': '大安'},
             {'dyna': '遼', 'king': '道宗', 'reign': '壽昌'},
             {'dyna': '遼', 'king': '天祚帝', 'reign': '乾統'},
             {'dyna': '遼', 'king': '天祚帝', 'reign': '天慶'},
             {'dyna': '遼', 'king': '天祚帝', 'reign': '保大'},
             {'dyna': '金', 'king': '太祖', 'reign': '收國'},
             {'dyna': '金', 'king': '太祖', 'reign': '天輔'},
             {'dyna': '金', 'king': '太宗', 'reign': '天會'},
             {'dyna': '金', 'king': '熙宗', 'reign': '天會'},
             {'dyna': '金', 'king': '熙宗', 'reign': '天眷'},
             {'dyna': '金', 'king': '熙宗', 'reign': '皇統'},
             {'dyna': '金', 'king': '海陵王', 'reign': '天德'},
             {'dyna': '金', 'king': '海陵王', 'reign': '貞元'},
             {'dyna': '金', 'king': '海陵王', 'reign': '正隆'},
             {'dyna': '金', 'king': '世宗', 'reign': '大定'},
             {'dyna': '金', 'king': '章宗', 'reign': '明昌'},
             {'dyna': '金', 'king': '章宗', 'reign': '承安'},
             {'dyna': '金', 'king': '章宗', 'reign': '泰和'},
             {'dyna': '金', 'king': '衛紹王', 'reign': '大安'},
             {'dyna': '金', 'king': '衛紹王', 'reign': '至寧'},
             {'dyna': '金', 'king': '宣宗', 'reign': '貞祐'},
             {'dyna': '金', 'king': '宣宗', 'reign': '興定'},
             {'dyna': '金', 'king': '宣宗', 'reign': '元光'},
             {'dyna': '金', 'king': '哀宗', 'reign': '正大'},
             {'dyna': '元', 'king': '世祖', 'reign': '中統'},
             {'dyna': '元', 'king': '世祖', 'reign': '至元'},
             {'dyna': '元', 'king': '成宗', 'reign': '元貞'},
             {'dyna': '元', 'king': '成宗', 'reign': '大德'},
             {'dyna': '元', 'king': '武宗', 'reign': '至大'},
             {'dyna': '元', 'king': '仁宗', 'reign': '皇慶'},
             {'dyna': '元', 'king': '仁宗', 'reign': '延祐'},
             {'dyna': '元', 'king': '英宗', 'reign': '至治'},
             {'dyna': '元', 'king': '泰定帝', 'reign': '泰定'},
             {'dyna': '元', 'king': '泰定帝', 'reign': '致和'},
             {'dyna': '元', 'king': '天順帝', 'reign': '天順'},
             {'dyna': '元', 'king': '文宗', 'reign': '天曆'},
             {'dyna': '元', 'king': '明宗', 'reign': '天曆'},
             {'dyna': '元', 'king': '文宗', 'reign': '天曆'},
             {'dyna': '元', 'king': '文宗', 'reign': '至順'},
             {'dyna': '元', 'king': '寧宗', 'reign': '至順'},
             {'dyna': '元', 'king': '順帝', 'reign': '元統'},
             {'dyna': '元', 'king': '順帝', 'reign': '至元'},
             {'dyna': '元', 'king': '順帝', 'reign': '至正'},
             {'dyna': '元', 'king': '昭宗', 'reign': '宣光'},
             {'dyna': '元', 'king': '孛兒只斤脫古思帖木兒', 'reign': '天元'},
             {'dyna': '明', 'king': '太祖', 'reign': '洪武'},
             {'dyna': '明', 'king': '惠帝', 'reign': '建文'},
             {'dyna': '明', 'king': '成祖', 'reign': '永樂'},
             {'dyna': '明', 'king': '仁宗', 'reign': '洪熙'},
             {'dyna': '明', 'king': '宣宗', 'reign': '宣德'},
             {'dyna': '明', 'king': '英宗', 'reign': '正統'},
             {'dyna': '明', 'king': '景帝', 'reign': '景泰'},
             {'dyna': '明', 'king': '英宗', 'reign': '天順'},
             {'dyna': '明', 'king': '憲宗', 'reign': '成化'},
             {'dyna': '明', 'king': '孝宗', 'reign': '弘治'},
             {'dyna': '明', 'king': '武宗', 'reign': '正德'},
             {'dyna': '明', 'king': '世宗', 'reign': '嘉靖'},
             {'dyna': '明', 'king': '穆宗', 'reign': '隆慶'},
             {'dyna': '明', 'king': '神宗', 'reign': '萬曆'},
             {'dyna': '明', 'king': '光宗', 'reign': '泰昌'},
             {'dyna': '明', 'king': '熹宗', 'reign': '天啟'},
             {'dyna': '明', 'king': '思宗', 'reign': '崇禎'},
             {'dyna': '明', 'king': '安宗（福王）', 'reign': '弘光'},
             {'dyna': '明', 'king': '紹宗（唐王）', 'reign': '隆武'},
             {'dyna': '明', 'king': '昭宗（桂王）', 'reign': '永曆'},
             {'dyna': '清', 'king': '太祖', 'reign': '天命'},
             {'dyna': '清', 'king': '太宗', 'reign': '天聰'},
             {'dyna': '清', 'king': '太宗', 'reign': '崇德'},
             {'dyna': '清', 'king': '世祖', 'reign': '順治'},
             {'dyna': '清', 'king': '聖祖', 'reign': '康熙'},
             {'dyna': '清', 'king': '世宗', 'reign': '雍正'},
             {'dyna': '清', 'king': '高宗', 'reign': '乾隆'},
             {'dyna': '清', 'king': '仁宗', 'reign': '嘉慶'},
             {'dyna': '清', 'king': '宣宗', 'reign': '道光'},
             {'dyna': '清', 'king': '文宗', 'reign': '咸豐'},
             {'dyna': '清', 'king': '穆宗', 'reign': '同治'},
             {'dyna': '清', 'king': '德宗', 'reign': '光緒'},
             {'dyna': '清', 'king': '遜帝', 'reign': '宣統'}]
#甲乙丙丁戊己庚辛壬癸
#子丑寅卯辰巳午未申酉戌亥
Ganzhi=['甲子','乙丑','丙寅','丁卯','戊辰','己巳','庚午','辛未','壬申','癸酉',
        '甲戌','乙亥','丙子','丁丑','戊寅','己卯','庚辰','辛巳','壬午','癸未',
        '甲申','乙酉','丙戌','丁亥','戊子','己丑','庚寅','辛卯','壬辰','癸巳',
        '甲午','乙未','丙申','丁酉','戊戌','己亥','庚子','辛丑','壬寅','癸卯',
        '甲辰','乙巳','丙午','丁未','戊申','己酉','庚戌','辛亥','壬子','癸丑',
        '甲寅','乙卯','丙辰','丁巳','戊午','己未','庚申','辛酉','壬戌','癸亥']

def getIndex(str):
    index=0
    for day in Ganzhi:
        if day==str:
            return index
        index+=1

def start():
    path='D:\\CalendarDate'
    for file in os.listdir(path):
        print(file)
        if not file.endswith('.html'):continue
        with open(os.path.join(path,file),'r',encoding='utf-8') as f:
            text=f.read()
        html_tree=etree.HTML(text)

        trs=html_tree.xpath('//tr')
        #print(etree.tostring(trs[0], pretty_print=True))
        index=0
        text=""
        yearIndex=0
        file=file.split('.')[0]
        dyna=file.split('_')[0]
        king=file.split('_')[1]
        reign=file.split('_')[2]
        JulianDay=0
        for i,tr in enumerate(trs):
            if i<2:continue
            index+=1
            td=tr.xpath('./td')
            #print(i,len(td))
            if len(td)==1:
                yearIndex+=1
                pattern1 = re.compile(r'[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]')   # 查找数字
                yearGanzhi = pattern1.findall(td[0].xpath('./text()')[0])[0]
                pattern2 = re.compile(r'\d+')   # 查找数字
                result2 = pattern2.findall(td[0].xpath('./text()')[0],15)
                JulianDay=tranJulianDay.Calendar2JD(int(result2[0]),int(result2[1]),int(result2[2]))

            if len(td)==33:
                month=tr.xpath('./th/text()')[0]
                monthDays=29 if (td[32].xpath('./text()')[0]=='-') else 30
                monthStart=getIndex(td[0].xpath('./text()')[0])
                for i in range(monthDays):
                    out=[dyna,king,reign,yearIndex,yearGanzhi,month,Ganzhi[(monthStart+i)%60],i+1,JulianDay]

                    write2csv(os.path.join(path,'out.csv'),out)
                    JulianDay+=1


            #text=text+parseChapterPage(link_href)
            # file_dir='D:\\OneNoteTempFile\\新书'
            # if not os.path.exists(file_dir):
            #     os.mkdir(file_dir)
            # file_name=str(index)+link_text+'.txt'
            # file_path=file_dir+'\\'+file_name
            # with open(file_path,'a',encoding='utf-8') as f:
            #     f.write(text)


# def parseChapterPage(chapterUrl):
#     html_tree=etree.HTML(text)
#     div=html_tree.xpath('//*[@id="content"]')[0]
#     h=html2text.HTML2Text()
#     h.ignore_links=True
#     text=h.handle(etree.tostring(div, pretty_print=True).decode())
#     return text

def step1():
    # 已完成。对原网站的政权数据提取为empReigns
    items=[];

    for empReign in empReigns:

        #print(empReign[0]);
        if empReign[0]==1:
            dyna=empReign[1];
            #print(empReign[1]);

        if empReign[0]==2:
            king=empReign[1];
            #print(empReign[1]);

        if empReign[0]==3:
            item = {'dyna': dyna, 'king': king, 'reign': empReign[1]};
            # print(item);
            items.append(item)

    pprint.pprint(items)
    # print(items)


def write2csv(filedir, stu):
    # write file
    # 打开文件，追加a
    with open(filedir, 'a',newline='',encoding='utf-8') as out:
    # 设定写入模式
        csv_write = csv.writer(out, dialect='excel')
        csv_write.writerow(stu)


def getCalendar():
    stu=[id, ]
    write2csv('D:\\CalendarDate\\calendar.csv', stu)

start()