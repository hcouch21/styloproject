from PlugInInterface import *

class FeatureExtractor(PlugIn, ExtractStart):
    def register(self, hooks):
        hooks[Hooks.EXTRACTSTART].append(self)

    def unregister(self, hooks):
        hooks[Hooks.EXTRACTSTART].remove(self)
    
    def run_extract_start_action(self, sample, corpus, manager):
        print "Feature extraction started..."