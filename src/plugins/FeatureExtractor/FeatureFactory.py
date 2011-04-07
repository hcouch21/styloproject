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

import imp
import os

from LinguisticFeature import *

def init_features(clazz):
    installed_features = os.listdir("features");

    for feature in installed_features:
        if feature.endswith(".py"):
            clazz.load_feature(feature[:-3])

    return clazz

@init_features
class FeatureFactory:
    _registered_features = {}

    @classmethod
    def get_feature(self, name):
        if name not in self._registered_features:
            self.load_feature(name)

        return self._registered_features[name]

    @classmethod
    def load_feature(self, name):
        try:
            mod = imp.load_source(name, "features/%s.py" % name);

            instance = getattr(mod, name)()

            if isinstance(instance, LinguisticFeature):
                self._registered_features[name] = getattr(mod, name)()
            else:
                print "Feature %s is not a Linguistic Feature!" % name
        except Exception as e:
            print "Failed to load feature %s: %s" % (name, e)
        
    @classmethod
    def get_installed_features(self):
        return self._registered_features.keys()
