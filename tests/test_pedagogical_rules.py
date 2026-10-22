"""Kontrakt pedagogických pravidiel v1.1 bez volania platenej API."""
from pathlib import Path
from pedagogical_rules import add_pedagogical_rules, read_sections, rules_digest


def test_sections_present():
    sections = read_sections()
    assert set(sections) == {'COMMON','EXPLANATION','DIALOGUE'}
    assert 'sprístupnených pasážach' in sections['COMMON']


def test_explanation_vs_dialogue():
    explanation=add_pedagogical_rules('Špeciálne odborné pravidlá autora', 'explanation')
    dialogue=add_pedagogical_rules('Špeciálne odborné pravidlá autora', 'dialogue')
    assert 'Špeciálne odborné pravidlá autora' in explanation
    assert 'JEDNU hlavnú' in dialogue
    assert 'Nezakončuj ho otázkou' in explanation
    assert 'Po 20. študentskom' in dialogue
    assert 'výhradne' in explanation.lower() or 'jedinými prameňmi' in explanation.lower()


def test_rule_revision_changes_digest(tmp_path):
    src=Path(__file__).resolve().parents[1]/'tutor_rules.txt'
    copy=tmp_path/'rules.txt'
    copy.write_bytes(src.read_bytes())
    original=rules_digest(copy)
    copy.write_text(copy.read_text(encoding='utf-8')+'\n# test change\n', encoding='utf-8')
    assert rules_digest(copy) != original


def test_invalid_mode_raises():
    try:
        add_pedagogical_rules('X','freeform')
    except ValueError:
        pass
    else:
        raise AssertionError('Režim bez validácie')
