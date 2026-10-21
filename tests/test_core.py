"""Offline tests: source integrity, retrieval scope, dialogue budgeting."""
from pathlib import Path
import json
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tutor_core import (load_corpus,CorpusError,PassageIndex,CONTENT_TYPES,
                       MAX_TURNS,source_label,evidence,transcript,normalize,api_error)

@pytest.fixture(scope='module')
def corpus():return load_corpus(ROOT/'uvod_do_analytickej_filozofie_texty.json')

@pytest.fixture(scope='module')
def index(corpus):return PassageIndex(corpus)

def test_nine_unique_works(corpus):
    assert len(corpus['works'])==9
    assert len({w['author'] for w in corpus['works']})==9
    assert [w['id'] for w in corpus['works']]==[f'AF{x:02d}' for x in range(1,10)]

def test_records(corpus):
    assert len(corpus['records'])==754
    assert len({r['id'] for r in corpus['records']})==754
    assert all(r['work_id'] in {w['id'] for w in corpus['works']} for r in corpus['records'])

def test_language_and_scope(corpus):
    assert [w['language'] for w in corpus['works']].count('cs')==1
    assert next(w for w in corpus['works'] if w['id']=='AF07')['author']=='Jaroslav Peregrin'
    for w in corpus['works']:
        assert any(r['type']=='paragraph' for r in corpus['records'] if r['work_id']==w['id'])

def test_hylton_opening_is_clickable(corpus):
    first=next(r for r in corpus['records'] if r['id']=='AF05-0003')
    assert first['type']=='paragraph' and 'filozofická analýza' in first['text']

def test_glock_stroll_only_chapters(corpus):
    assert 'kapitola' in next(w for w in corpus['works'] if w['id']=='AF03')['kind']
    assert 'kapitola' in next(w for w in corpus['works'] if w['id']=='AF09')['kind']

def test_peregrin_table(corpus):
    tables=[r for r in corpus['records'] if r['type']=='table']
    assert len(tables)==1 and tables[0]['work_id']=='AF07'
    assert tables[0]['rows'][0]==['Rok','Autor','Dílo']
    assert len(tables[0]['rows'])>20

def test_sources_no_fake_page(corpus):
    r=next(r for r in corpus['records'] if r['type']=='paragraph')
    label=source_label(r)
    assert 'pracovný odsek' in label and 'strana' not in label

def test_index_has_only_primary_content(index):
    assert len(index.rows)==sum(r['type'] in CONTENT_TYPES for r in load_corpus(ROOT/'uvod_do_analytickej_filozofie_texty.json')['records'])
    assert not any(r['type']=='note' for r in index.rows)

def test_focus_first(index):
    matches=index.find('filozofické problémy',work_ids={'AF05'},focus_id='AF05-0003')
    assert matches[0]['id']=='AF05-0003'
    assert all(r['work_id']=='AF05' for r in matches)

def test_scope_restriction(index):
    for chosen in [{'AF01'},{'AF03','AF04'},{'AF07'}]:
        matches=index.find('analytická filozofia',work_ids=chosen,limit=12)
        assert matches and all(r['work_id'] in chosen for r in matches)
    assert len(index.find('analytická filozofia',limit=9))==9

def test_diacritic_normalization():
    assert normalize('Analýza analytickej filozofie')=='analyza analytickej filozofie'

def test_evidence_limit(index):
    result=evidence(index,'analýza a logika',limit=20,char_budget=3000)
    assert len(result)<4200 and 'PRIMÁRNY PODKLAD:' in result
    assert 'nie pôvodná' in result.lower() or 'nie pôvodná' in result

def test_transcript():
    assert MAX_TURNS==20
    messages=[{'role':'user','content':'Čo je analýza?'},{'role':'assistant','content':'Pozrime sa na definície.'}]
    t=transcript(messages,'Test','celý korpus','test-model','abc')
    assert '1/20' in t and 'Čo je analýza?' in t and 'abc' in t

def test_api_error():
    assert '429' in api_error(Exception('429 RESOURCE_EXHAUSTED'),'model')
    assert '503' in api_error(Exception('503'),'model')
    assert '404' in api_error(Exception('404'),'model')
    assert 'časov' in api_error(Exception('ReadTimeout'),'model')

def test_reject_malformed(tmp_path,corpus):
    data=json.loads(json.dumps(corpus,ensure_ascii=False))
    data['records'].pop()
    path=tmp_path/'broken.json';path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf8')
    with pytest.raises(CorpusError):load_corpus(path)
