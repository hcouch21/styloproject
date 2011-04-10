#    This file is part of Stylo.
#
#    Stylo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Stylo is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Stylo.  If not, see <http://www.gnu.org/licenses/>.

from Domain import FeatureResult
from LinguisticFeature import *

import nltk
from nltk_contrib.readability import syllables_en

class Readability(LinguisticFeature):
    _short_name = "Readability"
    _long_name = "Readability"
    _description = "Various readability computations."
    
    word_count = 0
    char_count = 0
    syllable_count = 0
    sentence_count = 0
    avg_words_per_sentence = 0

    def extract(self, sample):
        self.__analyze_text(sample)
        
        results = []
        
        # FleschReadingEase
        result = FeatureResult("FleschReadingEase")
        result.value = 4.71 * (self.char_count / self.word_count) + 0.5 * (self.word_count / self.sentence_count) - 21.43
        results.append(result)
        
        return results
    
    def __analyze_text(self,  sample):
        words = self._get_words(sample)

        self.word_count = len(words)
        self.char_count = len(sample.plain_text)
        
        for word in words:
            self.syllable_count += syllables_en.count(word)
        
        self.sentence_count = len(nltk.sent_tokenize(sample.plain_text))
        
        self.avg_words_per_sentence = float(self.word_count) / \
                                      float(self.sentence_count)
