from PlugInInterface import *

class OrangeAdaptor(PlugIn, ClassifyStart, TrainStart):
    def register(self, hooks):
        hooks[Hooks.CLASSIFYSTART].append(self)
        hooks[Hooks.TRAINSTART].append(self)

    def unregister(self, hooks):
        hooks[Hooks.CLASSIFYSTART].remove(self)
        hooks[Hooks.TRAINSTART].append(self)

    def run_classify_start_action(self, state, manager):
        print "Classification started..."

    def run_train_start_action(self, state, manager):
        print "Training started..."