"""Actual Chromium rendering tests for the self-contained Streamlit v2 reader."""
from pathlib import Path
import ast
import json
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]


def assets():
    tree=ast.parse((ROOT/'book_reader.py').read_text(encoding='utf8'))
    output={}
    for node in tree.body:
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in {'READER_HTML','READER_CSS','READER_JS'}:
                    output[target.id]=ast.literal_eval(node.value)
    return output


def run_work(work_id,expected_heading=None,search_term='filozof',jump_to=None,check_table=False):
    corpus=json.loads((ROOT/'uvod_do_analytickej_filozofie_texty.json').read_text(encoding='utf8'))
    rows=[r for r in corpus['records'] if r['work_id']==work_id]
    source=assets()
    js=source['READER_JS'].replace('export default function(', 'function mountReader(',1)
    payload=json.dumps({'paragraphs':rows,'selected':None,
        'jumpToId':jump_to,'bookKey':work_id+'-test'},ensure_ascii=False).replace('</','<\\/')
    html=(f'<!doctype html><html lang="sk"><head><meta charset="utf-8"><style>{source["READER_CSS"]}</style></head>'
          f'<body style="width:1100px;margin:0">{source["READER_HTML"]}'
          f'<script>{js}\nwindow.selection=null;mountReader({{parentElement:document,data:{payload},'
          'setTriggerValue:(k,v)=>window.selection=v});</script></body></html>')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
        page=browser.new_page(viewport={'width':1150,'height':900})
        exceptions=[]
        page.on('pageerror',lambda e:exceptions.append(str(e)))
        page.set_content(html,wait_until='domcontentloaded')
        assert not exceptions,exceptions
        sc=page.locator('#af-scroll')
        maximum=sc.evaluate('(el)=>el.scrollHeight-el.clientHeight')
        assert maximum>400,(work_id,maximum)
        if jump_to:
            assert sc.evaluate('(el)=>el.scrollTop')>80,(work_id,'jump',jump_to)
            assert page.locator('.af-selected').count()>=1
        page.locator('#af-end-btn').click()
        assert abs(sc.evaluate('(el)=>el.scrollTop')-maximum)<3,(work_id,'end')
        assert page.locator('#af-bottom').is_visible()
        page.locator('#af-start').click()
        assert sc.evaluate('(el)=>el.scrollTop')<3,(work_id,'start')
        if expected_heading:
            headings=page.locator('#af-chapters option').all_text_contents()
            assert expected_heading in headings,(work_id,headings)
            page.locator('#af-chapters').select_option(label=expected_heading)
            assert sc.evaluate('(el)=>el.scrollTop')>0
        page.locator('#af-search').fill(search_term)
        assert page.locator('.af-hit').count()==1,(work_id,'search')
        assert 'Nález' in page.locator('#af-found').text_content()
        page.locator('#af-next').click()
        assert page.locator('.af-hit').count()==1,(work_id,'next')
        if check_table:
            assert page.locator('.af-real-table').count()==1
            assert page.locator('.af-real-table tr').count()>20
        # all primary blocks are separately clickable
        target=[r for r in rows if r['type'] in ('paragraph','quotation','thesis','list_item','table')][-1]
        page.locator('.af-paragraph').last.click()
        assert page.evaluate('window.selection')['id']==target['id']
        assert not exceptions,exceptions
        browser.close()
    return work_id,maximum,len(rows)


def test_all():
    for args in [
      ('AF01','Poznámky'),('AF02','Pojmová analýza'),('AF03','3. Štruktúra a obsah knihy'),
      ('AF04','Kam smeruje?'),('AF05','Quine'),('AF06','ZÁVER'),
      ('AF07','Klíčová díla analytické filosofie'),('AF08','XII'),('AF09',None)]:
        opts={'check_table':args[0]=='AF07'}
        if args[0]=='AF04':opts['jump_to']='AF04-0060'
        print('PASS',run_work(*args,**opts))

if __name__=='__main__':test_all()
