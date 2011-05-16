from PlugInInterface import *
from progressbar import *

class ConsoleNotifier(PlugIn, ExtractStart,  ExtractStop, FeatureStart, TrainStart,  TrainStop):
    """ Notifier plugin that prints status messages to STDOUT"""
    dependencies = None
    conflicts = None
    needs_vanilla_data = False
    modifies_data = False
    category = Categories.OUTPUT
    
    _progress_bar = None
    
    def register(self, events):
        """Set up callbacks for events we want to know about"""
        
        events[Events.EXTRACTSTART].append(self)
        events[Events.EXTRACTSTOP].append(self)
        events[Events.FEATURESTART].append(self)
        events[Events.TRAINSTART].append(self)
        events[Events.TRAINSTOP].append(self)

    def unregister(self, events):
        """Remove us from the list of callbacks"""
        
        events[Events.EXTRACTSTART].remove(self)
        events[Events.EXTRACTSTOP].remove(self)
        events[Events.FEATURESTART].remove(self)
        events[Events.TRAINSTART].remove(self)
        events[Events.TRAINSTOP].remove(self)
    
    def run_extract_start_action(self, state, manager):
        """Called when feature extraction begins"""
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
        """Called when feature extraction finishes"""
        if not state.training:
            self._progress_bar.finish()
            sys.stdout.write("\n")
    
    def run_feature_start_action(self, state, manager):
        """Called when an individual feature begins extraction"""
        if not state.training:
            #if self._progress_bar.maxval == 999:
            #    self._progress_bar.maxval = len(state.features_to_extract)
            
            if not self._progress_bar:
                self._progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=len(state.features_to_extract)).start()
            
            nextval = self._progress_bar.currval + 1
            self._progress_bar.update(nextval)
    
    def run_train_start_action(self, state, manager):
        """Called when training begins"""
        print "Training..."
        self._progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=state.corpus.author_count()).start()
    
    def run_train_stop_action(self, state, manager):
        """Called when training ends"""
        self._progress_bar.finish()
        sys.stdout.write("\n")
