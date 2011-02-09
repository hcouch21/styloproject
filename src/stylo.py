#!/usr/bin/python

from PluginManager import *

class StyloCLI(object):
    pass

if __name__ == "__main__":
    p = PluginManager()
    p.load_plugin("FeatureExtractor")
    p.load_plugin("OrangeAdaptor")
    print p