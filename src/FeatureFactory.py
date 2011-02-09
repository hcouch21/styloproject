import imp
import os

from LinguisticFeature import *

def init_features(clazz):
    installed_features = os.listdir("features");

    for feature in installed_features:
        if feature.endswith(".py"):
            clazz.load_feature(feature.rstrip(".py"))

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
            print "Failed to load feature %s." % name
        
    @classmethod
    def get_installed_features(self):
        return self._registered_features.keys()
