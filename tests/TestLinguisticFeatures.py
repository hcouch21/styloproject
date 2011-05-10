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

import unittest

import imp
import os
import sys

sys.path.append(os.getcwd())

from Domain import Sample

class  LinguisticFeaturesTestCase(unittest.TestCase):
    #def setUp(self):

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def get_linguistic_feature(self, name):
        mod = imp.load_source(name, "features/%s.py" % name)
        return getattr(mod, name)()

    def run_and_check_test(self, feature_name, correct) :
        lin_feat = self.get_linguistic_feature(feature_name)

        count = 0

        files = os.listdir("../tests/data")
        files.sort()

        for file in files :
            sample = Sample("../tests/data/%s" % file)
            val = lin_feat.extract(sample)

            for result in val :
                # Account for floating point inaccuracy
                if abs(result.value - correct[count]) > 0.0001 :
                    self.fail(("%s for %s calculated value %f is not " +
                                "equal to given value %f") % (feature_name,
                                file, result.value, correct[count]))
                count += 1

    def test_char_count(self):
        correct = [3182, 2906, 2870, 3001, 3052]

        self.run_and_check_test("CharCount", correct)

    def test_punct_pct(self):
        correct = [0.00, 0.85, 0.00, 0.97, 0.00,
                   0.00, 1.20, 0.07, 1.27, 0.00,
                   0.00, 1.05, 0.03, 1.08, 0.00,
                   0.00, 0.83, 0.00, 0.93, 0.00,
                   0.00, 0.85, 0.00, 0.95, 0.00]

        self.run_and_check_test("PctPunctuation", correct)

    def test_word_count(self):
        correct = [502, 505, 506, 498, 505]

        self.run_and_check_test("WordCount", correct)

    def test_ngram_freq(self):
        # @todo Is there any good way of testing this..?
        pass

    def test_avg_chars_per_paragraph(self):
        correct = [397.75, 363.25, 717.50, 500.17, 508.67]

        self.run_and_check_test("AvgCharactersPerParagraph", correct)

    def test_avg_words_per_paragraph(self):
        correct = [62.75, 63.13, 126.50, 83, 84.17]

        self.run_and_check_test("AvgWordsPerParagraph", correct)

    def test_avg_sent_per_paragraph(self):
        correct = [3.38, 4.38, 7.5, 4.17, 4.33]

        self.run_and_check_test("AvgSentencesPerParagraph", correct)

    def test_avg_sent_length(self):
        correct = [18.6296, 14.3429, 16.8667, 19.88, 19.4615]

        self.run_and_check_test("AvgSentenceLength", correct)

    def test_avg_syllables(self):
        correct = [1.6693, 1.394, 1.3636, 1.5582, 1.5603]

        self.run_and_check_test("AvgSyllables", correct)

if __name__ == '__main__':
    unittest.main()

