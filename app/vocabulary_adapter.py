###########################################################################
# Copyright 2025 (C) C3ngH <c3ngh@qq.com>
# Written permission must be obtained from the author for commercial uses.
###########################################################################

import os
import sys
import pickle
from datetime import datetime

_current_dir = os.path.dirname(__file__)
_possible_paths = [
    os.path.join(os.path.dirname(_current_dir), 'vocabulary'),
    os.path.join(_current_dir, '..', 'vocabulary'),
]

_vocabulary_path = None
for path in _possible_paths:
    if os.path.exists(path):
        _vocabulary_path = path
        break

if _vocabulary_path and _vocabulary_path not in sys.path:
    sys.path.insert(0, _vocabulary_path)

try:
    from vocabulary import UserVocabularyLevel, ArticleVocabularyLevel
except ImportError as e:
    import importlib.util
    
    if _vocabulary_path is None:
        raise ImportError(f"Cannot find vocabulary module. Tried: {_possible_paths}")
    
    vocab_file = os.path.join(_vocabulary_path, "vocabulary.py")
    if not os.path.exists(vocab_file):
        raise ImportError(f"Cannot find vocabulary.py at {vocab_file}")
    
    spec = importlib.util.spec_from_file_location("vocabulary", vocab_file)
    if spec and spec.loader:
        vocabulary_module = importlib.util.module_from_spec(spec)
        sys.modules['vocabulary'] = vocabulary_module
        spec.loader.exec_module(vocabulary_module)
        UserVocabularyLevel = vocabulary_module.UserVocabularyLevel
        ArticleVocabularyLevel = vocabulary_module.ArticleVocabularyLevel
    else:
        raise ImportError(f"Cannot import vocabulary module from {vocab_file}")


def load_record(pickle_fname):
    try:
        with open(pickle_fname, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def save_frequency_to_pickle(d, pickle_fname):
    exclusion_lst = ['one', 'no', 'has', 'had', 'do', 'that', 'have', 'by', 'not', 'but', 
                     'we', 'this', 'my', 'him', 'so', 'or', 'as', 'are', 'it', 'from', 
                     'with', 'be', 'can', 'for', 'an', 'if', 'who', 'whom', 'whose', 'which', 
                     'the', 'to', 'a', 'of', 'and', 'you', 'i', 'he', 'she', 'they', 'me', 
                     'was', 'were', 'is', 'in', 'at', 'on', 'their', 'his', 'her', 's', 
                     'said', 'all', 'did', 'been', 'w']
    
    d2 = {}
    for k in d:
        if k not in exclusion_lst and not k.isnumeric() and len(k) >= 2:
            if isinstance(d[k], list):
                d2[k] = list(sorted(d[k]))
            else:
                d2[k] = d[k]
    
    with open(pickle_fname, 'wb') as f:
        pickle.dump(d2, f)


def dict2lst(d):
    if len(d) == 0:
        return []
    
    keys = list(d.keys())
    if isinstance(d[keys[0]], int):
        lst = []
        for k in d:
            lst.append((k, [datetime.now().strftime('%Y%m%d%H%M')]))
        return lst
    elif isinstance(d[keys[0]], list):
        return list(d.items())
    
    return []


def lst2dict(lst, d):
    for x in lst:
        word = x[0]
        dates = x[1]
        if word not in d:
            d[word] = dates
        else:
            if isinstance(dates, list):
                d[word] += dates
            else:
                d[word] = dates


def merge_frequency(lst1, lst2):
    d = {}
    lst2dict(lst1, d)
    lst2dict(lst2, d)
    return d


def unfamiliar(path, word):
    if not os.path.exists(path):
        d = {word: [datetime.now().strftime('%Y%m%d%H%M')]}
    else:
        with open(path, "rb") as f:
            d = pickle.load(f)
        if word in d:
            if isinstance(d[word], list):
                d[word].append(datetime.now().strftime('%Y%m%d%H%M'))
            else:
                d[word] = [datetime.now().strftime('%Y%m%d%H%M')]
        else:
            d[word] = [datetime.now().strftime('%Y%m%d%H%M')]
    
    with open(path, "wb") as fp:
        pickle.dump(d, fp)


def familiar(path, word):
    if not os.path.exists(path):
        return
    
    with open(path, "rb") as f:
        d = pickle.load(f)
    
    if word in d:
        if isinstance(d[word], list):
            if len(d[word]) > 1:
                d[word].pop(0)
            else:
                d.pop(word)
        else:
            d.pop(word)
    
    with open(path, "wb") as fp:
        pickle.dump(d, fp)


def deleteRecord(path, word):
    if not os.path.exists(path):
        return
    
    with open(path, 'rb') as f:
        db = pickle.load(f)
    
    try:
        db.pop(word)
    except KeyError:
        pass
    
    with open(path, 'wb') as ff:
        pickle.dump(db, ff)


exclusion_lst = ['one', 'no', 'has', 'had', 'do', 'that', 'have', 'by', 'not', 'but', 
                 'we', 'this', 'my', 'him', 'so', 'or', 'as', 'are', 'it', 'from', 
                 'with', 'be', 'can', 'for', 'an', 'if', 'who', 'whom', 'whose', 'which', 
                 'the', 'to', 'a', 'of', 'and', 'you', 'i', 'he', 'she', 'they', 'me', 
                 'was', 'were', 'is', 'in', 'at', 'on', 'their', 'his', 'her', 's', 
                 'said', 'all', 'did', 'been', 'w']


ENGLISH_WORD_DIFFICULTY_DICT = {}


def convert_test_type_to_difficulty_level(d):
    result = {}
    L = list(d.keys())
    
    for k in L:
        if 'CET4' in d[k]:
            result[k] = 4
        elif 'OXFORD3000' in d[k]:
            result[k] = 5
        elif 'CET6' in d[k] or 'GRADUATE' in d[k]:
            result[k] = 6
        elif 'OXFORD5000' in d[k] or 'IELTS' in d[k]:
            result[k] = 7
        elif 'BBC' in d[k]:
            result[k] = 8
    
    global ENGLISH_WORD_DIFFICULTY_DICT
    ENGLISH_WORD_DIFFICULTY_DICT = result
    
    return result


def get_difficulty_level_for_user(d1, d2):
    global ENGLISH_WORD_DIFFICULTY_DICT
    
    if not ENGLISH_WORD_DIFFICULTY_DICT:
        d2 = convert_test_type_to_difficulty_level(d2)
    else:
        d2 = ENGLISH_WORD_DIFFICULTY_DICT
    
    for k in d1:
        if k not in d2:
            d2[k] = 3
    
    return d2


def user_difficulty_level(d_user, d, calc_func=0):
    if not d_user:
        return 1.0
    
    user_vocab = UserVocabularyLevel(d_user)
    level = user_vocab.level_score
    
    return max(level, 1.0)


def text_difficulty_level(s, d):
    if not s or not s.strip():
        return 1.0
    
    article_vocab = ArticleVocabularyLevel(s)
    level = article_vocab.level_score
    
    return max(level, 1.0)


def revert_dict(d):
    d2 = {}
    for k in d:
        if isinstance(d[k], list):
            lst = d[k]
        elif isinstance(d[k], int):
            freq = d[k]
            lst = freq * ['2021082019']
        else:
            continue
        
        for time_info in lst:
            date = time_info[:10]
            if date not in d2:
                d2[date] = [k]
            else:
                d2[date].append(k)
    
    return d2
