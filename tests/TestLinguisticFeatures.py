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

    def test_char_count(self):
        correct = [3182, 2906, 2870, 3001, 3052]
        
        lin_feat = self.get_linguistic_feature("CharCount")

        count = 0
        files = os.listdir("../tests/data")
        files.sort()

        for file in files:
            sample = Sample("../tests/data/%s" % file)
            val = lin_feat.extract(sample)

            if val[0].value != correct[count]:
                self.fail("CharCount for %s calculated value %d is not " +
                          "equal to given value %d." % (file, val[0].value, 
                          correct[count]))

            count += 1

    def test_punct_pct(self):
        lin_feat = self.get_linguistic_feature("PctPunctuation")

        correct = [[0.00, 0.91, 0.00, 0.97, 0.00],
                   [0.00, 1.20, 0.07, 1.27, 0.00],
                   [0.00, 1.08, 0.03, 1.08, 0.00],
                   [0.00, 0.83, 0.00, 0.93, 0.00],
                   [0.00, 0.85, 0.00, 0.95, 0.00]]

        files = os.listdir("../tests/data")
        files.sort()

        row = 0;
        col = 0;

        for file in files:
            sample = Sample("../tests/data/%s" % file)
            val = lin_feat.extract(sample)

            col = 0;

            for result in val :
                if result.value != correct[row][col]:
                    self.fail("PctPunctuation for %s calculated value %.2f " +
                              "is not equal to given value %.2f. at (%d,%d)" %
                              (file, result.value, correct[row][col],row,col))
                col += 1

            row += 1

    def test_word_count(self):
        pass

    def test_ngram_freq(self):
        lin_feat = self.get_linguistic_feature("NGramFreq")

        files = os.listdir("../tests/data")
        files.sort()

        for file in files :
            sample = Sample("../tests/data/%s" % file)
            val = lin_feat.extract(sample)

#            print "Results for " + file + ":\n"
#            for result in val :
#                print result.name + ": " + str(result.value) + "\n"

if __name__ == '__main__':
    unittest.main()

