from PlugInInterface import *

class FeatureExtractor(PlugIn, ExtractStart):
    def register(self, hooks):
        hooks[Hooks.EXTRACTSTART].append(self)

    def unregister(self, hooks):
        hooks[Hooks.EXTRACTSTART].remove(self)
    
    def run_extract_start_action(self, state, manager):
        print "Feature extraction started..."

        for feature in FeatureFactory.get_installed_features():
            print FeatureFactory.get_feature(feature).get_long_name()