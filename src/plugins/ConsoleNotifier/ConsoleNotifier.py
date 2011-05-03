from PlugInInterface import *
from progressbar import *

class ConsoleNotifier(PlugIn, ExtractStart,  ExtractStop, FeatureStart, TrainStart,  TrainStop):
    _progress_bar = None
    
    def register(self, hooks):
        """Set up callbacks for events we want to know about"""
        
        hooks[Hooks.EXTRACTSTART].append(self)
        hooks[Hooks.EXTRACTSTOP].append(self)
        hooks[Hooks.FEATURESTART].append(self)
        hooks[Hooks.TRAINSTART].append(self)
        hooks[Hooks.TRAINSTOP].append(self)

    def unregister(self, hooks):
        """Remove us from the list of callbacks"""
        
        hooks[Hooks.EXTRACTSTART].remove(self)
        hooks[Hooks.EXTRACTSTOP].remove(self)
        hooks[Hooks.FEATURESTART].remove(self)
        hooks[Hooks.TRAINSTART].remove(self)
        hooks[Hooks.TRAINSTOP].remove(self)
    
    def run_extract_start_action(self, state, manager):
        if state.training:
            nextval = self._progress_bar.currval + 1
            self._progress_bar.update(nextval)
        else:
            print "Classifying %s..." % state.to_extract[0].name
        #else:
        #    if state.features_to_extract:
        #        self._progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(state.features_to_extract)).start()
        #    else:
        #        self._progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=999).start()
    
    def run_extract_stop_action(self,  state,  manager):
        if not state.training:
            self._progress_bar.finish()
            sys.stdout.write("\n")
    
    def run_feature_start_action(self, state, manager):
        if not state.training:
            #if self._progress_bar.maxval == 999:
            #    self._progress_bar.maxval = len(state.features_to_extract)
            
            if not self._progress_bar:
                self._progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(state.features_to_extract)).start()
            
            nextval = self._progress_bar.currval + 1
            self._progress_bar.update(nextval)
    
    def run_train_start_action(self, state, manager):
        print "Training..."
        self._progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=state.corpus.author_count()).start()
    
    def run_train_stop_action(self, state, manager):
        self._progress_bar.finish()
        sys.stdout.write("\n")
