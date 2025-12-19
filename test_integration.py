#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###########################################################################
# Copyright 2025 (C) C3ngH <c3ngh@qq.com>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

import os
import sys
import pickle
from datetime import datetime

app_path = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_path)

import vocabulary_adapter as adapter

print("=" * 80)
print("Testing vocabulary_adapter integration")
print("=" * 80)

print("\n[Test 1] Pickle load/save operations")
test_dict = {
    'apple': ['20231201', '20231202'],
    'banana': ['20231203'],
    'orange': ['20231204', '20231205', '20231206']
}

test_file = '/tmp/test_vocab.p'
try:
    adapter.save_frequency_to_pickle(test_dict, test_file)
    loaded_dict = adapter.load_record(test_file)
    assert loaded_dict == test_dict, "Dict mismatch after save/load"
    print("✓ Pickle save/load works correctly")
except Exception as e:
    print(f"✗ Pickle save/load failed: {e}")
finally:
    if os.path.exists(test_file):
        os.remove(test_file)

print("\n[Test 2] Dictionary to list conversion")
try:
    lst = adapter.dict2lst(test_dict)
    assert len(lst) == 3, f"Expected 3 items, got {len(lst)}"
    assert ('apple', ['20231201', '20231202']) in lst, "apple not in list"
    print(f"✓ dict2lst conversion works: {lst}")
except Exception as e:
    print(f"✗ dict2lst failed: {e}")

print("\n[Test 3] List to dictionary merge")
try:
    new_dict = {}
    new_lst = [('pear', ['20231207']), ('apple', ['20231208'])]
    adapter.lst2dict(new_lst, new_dict)
    assert 'pear' in new_dict, "pear not added"
    assert 'apple' in new_dict, "apple not added"
    print(f"✓ lst2dict works: {new_dict}")
except Exception as e:
    print(f"✗ lst2dict failed: {e}")

print("\n[Test 4] Frequency merge")
try:
    lst1 = [('word1', ['20231201']), ('word2', ['20231202'])]
    lst2 = [('word2', ['20231203']), ('word3', ['20231204'])]
    merged = adapter.merge_frequency(lst1, lst2)
    assert len(merged) == 3, f"Expected 3 words, got {len(merged)}"
    assert len(merged['word2']) == 2, f"word2 should have 2 dates, got {len(merged['word2'])}"
    print(f"✓ merge_frequency works: {merged}")
except Exception as e:
    print(f"✗ merge_frequency failed: {e}")

print("\n[Test 5] Unfamiliar/familiar word tracking")
test_file2 = '/tmp/test_user_vocab.p'
try:
    adapter.unfamiliar(test_file2, 'test')
    loaded = adapter.load_record(test_file2)
    assert 'test' in loaded, "test word not added"
    assert len(loaded['test']) == 1, "Should have 1 timestamp"
    
    adapter.unfamiliar(test_file2, 'test')
    loaded = adapter.load_record(test_file2)
    assert len(loaded['test']) == 2, "Should have 2 timestamps"
    
    adapter.familiar(test_file2, 'test')
    loaded = adapter.load_record(test_file2)
    assert len(loaded['test']) == 1, "Should have 1 timestamp after familiar"
    
    adapter.familiar(test_file2, 'test')
    loaded = adapter.load_record(test_file2)
    assert 'test' not in loaded, "Word should be removed"
    
    print("✓ unfamiliar/familiar tracking works")
except Exception as e:
    print(f"✗ unfamiliar/familiar failed: {e}")
finally:
    if os.path.exists(test_file2):
        os.remove(test_file2)

print("\n[Test 6] Delete record")
test_file3 = '/tmp/test_delete.p'
try:
    test_dict_del = {'word1': ['20231201'], 'word2': ['20231202']}
    adapter.save_frequency_to_pickle(test_dict_del, test_file3)
    
    adapter.deleteRecord(test_file3, 'word1')
    loaded = adapter.load_record(test_file3)
    assert 'word1' not in loaded, "word1 should be deleted"
    assert 'word2' in loaded, "word2 should remain"
    
    print("✓ deleteRecord works")
except Exception as e:
    print(f"✗ deleteRecord failed: {e}")
finally:
    if os.path.exists(test_file3):
        os.remove(test_file3)

print("\n[Test 7] User difficulty level calculation")
try:
    user_dict = {
        'abandon': ['20231201', '20231202'],
        'ability': ['20231203']
    }
    level = adapter.user_difficulty_level(user_dict, {})
    assert isinstance(level, (int, float)), f"Level should be numeric, got {type(level)}"
    assert level >= 0, f"Level should be non-negative, got {level}"
    print(f"✓ user_difficulty_level works: {level}")
except Exception as e:
    print(f"✗ user_difficulty_level failed: {e}")

print("\n[Test 8] Text difficulty level calculation")
try:
    sample_text = """
    This is a simple test article with some words.
    It contains basic vocabulary and some more advanced words.
    We want to test if the difficulty calculation works correctly.
    """
    level = adapter.text_difficulty_level(sample_text, {})
    assert isinstance(level, (int, float)), f"Level should be numeric, got {type(level)}"
    assert level >= 0, f"Level should be non-negative, got {level}"
    print(f"✓ text_difficulty_level works: {level}")
except Exception as e:
    print(f"✗ text_difficulty_level failed: {e}")

print("\n[Test 9] Exclusion list filtering")
try:
    test_dict_excl = {
        'apple': ['20231201'],
        'the': ['20231202'],
        'a': ['20231203'],
        'banana': ['20231204']
    }
    test_file4 = '/tmp/test_excl.p'
    adapter.save_frequency_to_pickle(test_dict_excl, test_file4)
    loaded = adapter.load_record(test_file4)
    
    assert 'apple' in loaded, "apple should be kept"
    assert 'banana' in loaded, "banana should be kept"
    assert 'the' not in loaded, "the should be excluded"
    assert 'a' not in loaded, "a should be excluded"
    
    print("✓ Exclusion list works")
    if os.path.exists(test_file4):
        os.remove(test_file4)
except Exception as e:
    print(f"✗ Exclusion list failed: {e}")

print("\n" + "=" * 80)
print("Integration test completed!")
print("=" * 80)
