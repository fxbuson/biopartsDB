# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 07:42:41 2020

@author: Felipe
"""

from bs4 import BeautifulSoup
import os

where = '../database/templates'

for what in os.listdir(where):
    if what.endswith('.html'):
        print(what)
        
        file = open(where + '/' + what, 'r', encoding='utf-8')
        text = file.read()
        
#        text = text.replace("example-table", "parts-table")
        
        soup = BeautifulSoup(text, 'html.parser')
        file.close()
#        file = open('../database/templates/nav_template.html')
#        text = file.read()
#        new = BeautifulSoup(text, 'html.parser')
        
        if soup.head:
            new = soup.new_tag("link")
            new["href"] = "../images/logo_square.png"
            new["rel"] = "icon"
#            soup.nav.replace_with(new)
            soup.head.append(new)
        
        html = soup.prettify(soup.original_encoding)
        with open(where + '/' + what, "w", encoding='utf-8') as dest:
            dest.write(html)