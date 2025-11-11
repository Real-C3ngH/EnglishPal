''' 
   Estimate a user's vocabulary level given his vocabulary data
   Estimate an English article's difficulty level given its content
   Preliminary design
   
   Hui, 2024-09-23
   Last upated: 2024-09-25, 2024-09-30
'''

import pickle


def load_record(pickle_fname):
    with open(pickle_fname, 'rb') as f:
        d = pickle.load(f)
    return d


class VocabularyLevelEstimator:
    _test = load_record('words_and_tests.p') # map a word to the sources where it appears

    @property
    def level(self):
        total = 0.0 # TODO: need to compute this number
        num = 1
        for word in self.word_lst:
            num += 1
            if word in self._test:
                print(f'{word} : {self._test[word]}')
            else:
                print(f'{word}')
        return total/num


class UserVocabularyLevel(VocabularyLevelEstimator):
    def __init__(self, d):
        self.d = d
        self.word_lst = list(d.keys())
        # just look at the most recently-added words


class ArticleVocabularyLevel(VocabularyLevelEstimator):
    def __init__(self, content):
        self.content = content
        self.word_lst = content.lower().split()
        # select the 10 most difficult words
        

if __name__ == '__main__':
    d = load_record('frequency_mrlan85.pickle')
    print(d)
    user = UserVocabularyLevel(d)
    print(user.level) # level is a property
    article = ArticleVocabularyLevel('This is an interesting article')
    print(article.level)
    
    
    
