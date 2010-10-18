# This Python file uses the following encoding: utf-8
import os, sys
import datetime
from models import Position

p = Position(title = u'网站开发工程师',
             department = u'R&D',
             responsibility = u'开发基于Python/Javascript的网站应用；负责相应模块的设计，开发，单元测试和文档编写；参与相关领域的创新和探索性研究。',
             requirement = u'计算机专业或相关领域本科学历（及以上）；三年以上网站开发工作经验；精通Python/Cheerypy开发，熟悉相关平台；精通Javascript/JQuery开发，熟悉Json/Ajax/XML/REST等技术；熟悉各种浏览器特性和开发；为人开朗，有良好的团队合作精神。',
             preference = u'熟悉Flash/ActionScript开发，并有相关工作背景视为额外优势；熟悉网络构架，网络协议，有网络监控或者协议分析相关工作背景视为额外优势。',
             pub_date=datetime.datetime.now());
p.save();
