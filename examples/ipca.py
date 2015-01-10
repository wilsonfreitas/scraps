
# /html/body/div[1]/div[3]/table/tbody/tr/td/div/center/table/tbody/tr[1]

import scraps
import textparser
import itertools

class NumberParser(textparser.TextParser):
    def parse_int(self, text, match):
        r'^\d+$'
        return eval(text)
    
    def parse_number_ptBR_with_percent(self, text, match):
        r'^-?\s*((\d+[\.])+)?\d+[,]\d+%$'
        text = text.replace('%', '')
        text = text.replace('.', '')
        text = text.replace(',', '.')
        return eval(text)*100
    
    def parse_number_ptBR_with_thousands(self, text, match):
        r'^-?\s*((\d+[\.])+)?\d+[,]\d+?$'
        text = text.replace('.', '')
        text = text.replace(',', '.')
        return eval(text)
    
    def parseText(self, text):
        return 'NA'


def month_pt2en(mes):
    mes = mes.lower()
    return {'fev':'feb', 'abr':'apr', 'mai':'may', 'ago':'aug', 'set':'sep', 'out':'oct'}.get(mes, mes)


def month_pt2number(mes):
    mes = mes.lower()
    return {
        'jan':1, 'fev':2, 'mar':3, 'abr':4, 'mai':5, 'jun':6, 'jul':7, 'ago':8, 'set':9, 'out':10, 'nov':11,'dez':12
    }.get(mes)


number_parser = NumberParser()


class IPCAScrap(scraps.Scrap):
    colnames = scraps.Attribute(xpath='//table[3]/tr[1]/td', apply=[month_pt2en])
    rownames = scraps.Attribute(xpath='//table[3]/tr[position()>1]/td[1]')
    data = scraps.Attribute(xpath='//table[3]/tr[position()>1]/td[position()>1]', apply=[number_parser.parse])


# ----------------


class IPCAScrap(scraps.Scrap):
    colnames = scraps.Attribute(xpath='//table[1]/*/tr[1]/td[position()>1]', apply=[month_pt2number])
    rownames = scraps.Attribute(xpath='//table[1]/*/tr[position()>1]/td[1]', apply=[number_parser.parse])
    data = scraps.Attribute(xpath='//table[1]/*/tr[position()>1]/td[position()>1]')#, apply=[number_parser.parse])


class IPCAFetcher(scraps.Fetcher):
    scrapclass = IPCAScrap
    url = 'http://www.portalbrasil.net/ipca.htm'


fetcher = IPCAFetcher()
res = fetcher.fetch()


print(res.colnames)
# print(res.rownames)
# print(res.data)


# for month, rate in zip(list(itertools.product(res.rownames, res.colnames)), res.data):
#     print(month + (rate,))