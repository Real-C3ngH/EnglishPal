# Run this test script on the command line:
#   pytest test_vocabulary.py
#
# Last modified by Mr Lan Hui on 2025-03-05

from vocabulary import UserVocabularyLevel, ArticleVocabularyLevel


def test_article_level_empty_content():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('')
    assert article.level == 0

def test_article_level_punctuation_only():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel(',')
    assert article.level == 0

def test_article_level_digit_only():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('1')
    assert article.level == 0
    
def test_article_level_single_word():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('source')
    assert 2 <= article.level <= 4

def test_article_level_subset_vs_superset():
    ''' Boundary case test '''
    article1 = ArticleVocabularyLevel('source')
    article2 = ArticleVocabularyLevel('open source')
    assert article1.level < article2.level
    
def test_article_level_multiple_words():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('Producing Open Source Software - How to Run a Successful Free Software Project')
    assert 3 <= article.level <= 5

def test_article_level_short_paragraph():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('At parties, people no longer give me a blank stare when I tell them I work in open source software. "Oh, yes — like Linux?" they say. I nod eagerly in agreement. "Yes, exactly! That\'s what I do." It\'s nice not to be completely fringe anymore. In the past, the next question was usually fairly predictable: "How do you make money doing that?" To answer, I\'d summarize the economics of free software: that there are organizations in whose interest it is to have certain software exist, but that they don\'t need to sell copies, they just want to make sure the software is available and maintained, as a tool instead of as a rentable monopoly.')
    assert 4 <= article.level <= 6

def test_article_level_medium_paragraph():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('In considering the Origin of Species, it is quite conceivable that a naturalist, reflecting on the mutual affinities of organic beings, on their embryological relations, their geographical distribution, geological succession, and other such facts, might come to the conclusion that each species had not been independently created, but had descended, like varieties, from other species. Nevertheless, such a conclusion, even if well founded, would be unsatisfactory, until it could be shown how the innumerable species inhabiting this world have been modified, so as to acquire that perfection of structure and coadaptation which most justly excites our admiration. Naturalists continually refer to external conditions, such as climate, food, etc., as the only possible cause of variation. In one very limited sense, as we shall hereafter see, this may be true; but it is preposterous to attribute to mere external conditions, the structure, for instance, of the woodpecker, with its feet, tail, beak, and tongue, so admirably adapted to catch insects under the bark of trees. In the case of the misseltoe, which draws its nourishment from certain trees, which has seeds that must be transported by certain birds, and which has flowers with separate sexes absolutely requiring the agency of certain insects to bring pollen from one flower to the other, it is equally preposterous to account for the structure of this parasite, with its relations to several distinct organic beings, by the effects of external conditions, or of habit, or of the volition of the plant itself.')
    assert 5 <= article.level <= 7
    
def test_article_level_long_paragraph():
    ''' Boundary case test '''
    article = ArticleVocabularyLevel('These several facts accord well with my theory. I believe in no fixed law of development, causing all the inhabitants of a country to change abruptly, or simultaneously, or to an equal degree. The process of modification must be extremely slow. The variability of each species is quite independent of that of all others. Whether such variability be taken advantage of by natural selection, and whether the variations be accumulated to a greater or lesser amount, thus causing a greater or lesser amount of modification in the varying species, depends on many complex contingencies,—on the variability being of a beneficial nature, on the power of intercrossing, on the rate of breeding, on the slowly changing physical conditions of the country, and more especially on the nature of the other inhabitants with which the varying species comes into competition. Hence it is by no means surprising that one species should retain the same identical form much longer than others; or, if changing, that it should change less. We see the same fact in geographical distribution; for instance, in the land-shells and coleopterous insects of Madeira having come to differ considerably from their nearest allies on the continent of Europe, whereas the marine shells and birds have remained unaltered. We can perhaps understand the apparently quicker rate of change in terrestrial and in more highly organised productions compared with marine and lower productions, by the more complex relations of the higher beings to their organic and inorganic conditions of life, as explained in a former chapter. When many of the inhabitants of a country have become modified and improved, we can understand, on the principle of competition, and on that of the many all-important relations of organism to organism, that any form which does not become in some degree modified and improved, will be liable to be exterminated. Hence we can see why all the species in the same region do at last, if we look to wide enough intervals of time, become modified; for those which do not change will become extinct.')
    assert 6 <= article.level <= 8
    
def test_user_level_empty_dictionary():
    ''' Boundary case test '''
    user = UserVocabularyLevel({})
    assert user.level == 0

def test_user_level_one_simple_word():
    ''' Boundary case test '''
    user = UserVocabularyLevel({'simple':['202408050930']})
    assert 0 < user.level <= 4
    
def test_user_level_invalid_word():
    ''' Boundary case test '''
    user = UserVocabularyLevel({'xyz':['202408050930']})
    assert user.level == 0
 
def test_user_level_one_hard_word():
    ''' Boundary case test '''
    user = UserVocabularyLevel({'pasture':['202408050930']})
    assert 5 <= user.level <= 8
 
def test_user_level_multiple_words():
    ''' Boundary case test '''
    user = UserVocabularyLevel(
        {'sessile': ['202408050930'], 'putrid': ['202408050930'], 'prodigal': ['202408050930'], 'presumptuous': ['202408050930'], 'prehension': ['202408050930'], 'pied': ['202408050930'], 'pedunculated': ['202408050930'], 'pasture': ['202408050930'], 'parturition': ['202408050930'], 'ovigerous': ['202408050930'], 'ova': ['202408050930'], 'orifice': ['202408050930'], 'obliterate': ['202408050930'], 'niggard': ['202408050930'], 'neuter': ['202408050930'], 'locomotion': ['202408050930'], 'lineal': ['202408050930'], 'glottis': ['202408050930'], 'frivolous': ['202408050930'], 'frena': ['202408050930'], 'flotation': ['202408050930'], 'ductus': ['202408050930'], 'dorsal': ['202408050930'], 'dearth': ['202408050930'], 'crustacean': ['202408050930'], 'cornea': ['202408050930'], 'contrivance': ['202408050930'], 'collateral': ['202408050930'], 'cirriped': ['202408050930'], 'canon': ['202408050930'], 'branchiae': ['202408050930'], 'auditory': ['202408050930'], 'articulata': ['202408050930'], 'alimentary': ['202408050930'], 'adduce': ['202408050930'], 'aberration': ['202408050930']}        
    )
    assert 6 <= user.level <= 8
 
def test_user_level_consider_only_most_recent_words_difficult_words_most_recent():
    ''' Consider only the most recent three words '''
    user = UserVocabularyLevel(
        {'pasture':['202408050930'], 'putrid': ['202408040000'], 'frivolous':['202408030000'], 'simple':['202408020000'], 'apple':['202408010000']}
    )
    assert 5 <= user.level <= 8
 
def test_user_level_consider_only_most_recent_words_easy_words_most_recent():
    ''' Consider only the most recent three words '''
    user = UserVocabularyLevel(
        {'simple':['202408050930'], 'apple': ['202408040000'], 'happy':['202408030000'], 'pasture':['202408020000'], 'putrid':['202408010000'], 'dearth':['202407310000']}
    )
    assert 4 <= user.level <= 5
