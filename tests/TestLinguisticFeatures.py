#    This file is part of Stylo.
#
#    Stylo is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
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
        correct = [2870, 3001, 3052, 3182, 2906]
        
        lin_feat = self.get_linguistic_feature("CharCount")

        count = 0
        for file in os.listdir("./tests/data/"):
            with open("tests/data/%s" % file, "r") as f:
                val = lin_feat.extract(f.read())
                
                if val != correct[count]:
                    self.fail("CharCount for %s calculated value %d is not equal to given value %d." % (file, val, correct[count]))

            count += 1

    def test_punct_count(self):
        pass

    def test_word_count(self):
        pass

if __name__ == '__main__':
    unittest.main()

