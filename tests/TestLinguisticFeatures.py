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

from src.Domain import Sample

class  LinguisticFeaturesTestCase(unittest.TestCase):
    def setUp(self):
        sys.path.append("./src")

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None

    def get_linguistic_feature(self, name):
        mod = imp.load_source(name, "src/features/%s.py" % name)
        return getattr(mod, name)()

    def test_char_count(self):
        correct = [3182, 2906, 2870, 3001, 3052]
        
        lin_feat = self.get_linguistic_feature("CharCount")

        count = 0
        files = os.listdir("./tests/data")
        files.sort()

        for file in files:
            sample = Sample("tests/data/%s" % file)
            val = lin_feat.extract(sample)

            if val[0].value != correct[count]:
                self.fail("CharCount for %s calculated value %d is not equal to given value %d." % (file, val[0].value, correct[count]))

            count += 1

    def test_punct_count(self):
        pass

    def test_word_count(self):
        pass

if __name__ == '__main__':
    unittest.main()

