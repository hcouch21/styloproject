#!/usr/bin/python

from PluginManager import *
from FeatureFactory import *

class StyloCLI(object):
    pass

if __name__ == "__main__":
    p = PluginManager()
    p.load_plugin("FeatureExtractor")
    p.load_plugin("OrangeAdaptor")
    print p

    print "Installed features:"
    for feature in FeatureFactory.get_installed_features():
			print FeatureFactory.get_feature(feature).get_long_name()
