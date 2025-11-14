import re
import pickle
from statistics import mean

TAG_ORDER = [
    "CET4",
    "CET6",
    "OXFORD3000",
    "OXFORD5000",
    "IELTS",
    "GRADUATE",
    "BBC"
]

TAG_DIFFICULTY = {tag: i + 1 for i, tag in enumerate(TAG_ORDER)}  # CET4=1, BBC=7


def load_record(fname):
    with open(fname, "rb") as f:
        return pickle.load(f)


class VocabularyLevelEstimator:
    """Base class for vocabulary difficulty computation."""

    def __init__(self):
        self._test = load_record("words_and_tests.p")

    def word_difficulty(self, word):
        """Return difficulty score of a word based on its TAGs."""
        tags = self._test.get(word.lower())
        if not tags:
            return 0  # unknown word difficulty = 0

        # A word may appear in multiple systems → use the hardest one
        return max(TAG_DIFFICULTY.get(tag, 0) for tag in tags)

    def map_score_to_tag(self, score):
        """Convert numeric score back to a representative TAG level."""
        if score <= 0:
            return "UNKNOWN"

        closest = min(TAG_DIFFICULTY.items(), key=lambda x: abs(x[1] - score))
        return closest[0]


class UserVocabularyLevel(VocabularyLevelEstimator):
    """
    User level = weighted average difficulty of unknown words.
    weight = number of times user added this word.
    """

    def __init__(self, freq_dict):
        super().__init__()
        self.freq_dict = freq_dict

    def _word_weight(self, value):
        """Convert value to weight (compat old format)."""
        if isinstance(value, list):
            return len(value)
        return int(value)

    @property
    def level(self):
        scores = []
        weights = []

        for word, value in self.freq_dict.items():
            diff = self.word_difficulty(word)
            w = self._word_weight(value)

            scores.append(diff)
            weights.append(w)

        if not scores:
            return {"score": 0, "level": "UNKNOWN", "details": {}}

        weighted_score = sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        level_tag = self.map_score_to_tag(weighted_score)

        return {
            "score": round(weighted_score, 3),
            "level": level_tag,
            "details": {
                "word_count": len(scores),
                "weighted_total": sum(weights),
            }
        }


class ArticleVocabularyLevel(VocabularyLevelEstimator):
    """Article difficulty = average of top 10% hardest words."""

    def __init__(self, content):
        super().__init__()
        self.content = content

    def tokenize(self):
        tokens = re.findall(r"[a-zA-Z]+", self.content.lower())
        return [w for w in tokens if len(w) > 2]  # ignore very short words

    @property
    def level(self):
        words = self.tokenize()
        if not words:
            return {"score": 0, "level": "UNKNOWN", "details": {}}

        diffs = [(w, self.word_difficulty(w)) for w in words]
        diffs.sort(key=lambda x: x[1], reverse=True)

        top_n = max(1, len(diffs) // 10)  # top 10%
        hardest = diffs[:top_n]

        score = mean(d for _, d in hardest)
        level_tag = self.map_score_to_tag(score)

        return {
            "score": round(score, 3),
            "level": level_tag,
            "details": {
                "word_count": len(words),
                "hardest_words": hardest,
                "top_percent": "10%",
            }
        }

