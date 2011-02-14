class PlugIn(object):
    def register(self, hooks):
        raise NotImplementedError()

    def unregister(self, hooks):
        raise NotImplementedError()

class StyloStart(object):
    def run_stylo_start_action(self, state, manager):
        raise NotImplementedError()

class StyloStop(object):
    def run_stylo_stop_action(self, state, manager):
        raise NotImplementedError()

class ExtractStart(object):
    def run_extract_start_action(self, state, manager):
        raise NotImplementedError()

class ExtractStop(object):
    def run_extract_stop_action(self, state, manager):
        raise NotImplementedError()

class FeatureStart(object):
    def run_feature_start_action(self, state, feature):
        raise NotImplementedError()

class FeatureStop(object):
    def run_feature_stop_action(self, state, manager):
        raise NotImplementedError()

class ClassifyStart(object):
    def run_classify_start_action(self, state, manager):
        raise NotImplementedError()

class ClassifyStop(object):
    def run_classify_stop_action(self, state, manager):
        raise NotImplementedError()

class TrainStart(object):
    def run_train_start_action(self, state, manager):
        raise NotImplementedError()

class TrainStop(object):
    def run_train_stop_action(self, state, manager):
        raise NotImplementedError()

class RunState(object):
    training = None

    corpus = None
    sample = None

    current_feature = None

class Hooks(object):
    STYLOSTART = "StyloStart"
    STYLOSTOP = "StyloStop"
    EXTRACTSTART = "ExtractStart"
    EXTRACTSTOP = "ExtractStop"
    FEATURESTART = "FeatureStart"
    FEATURESTOP = "FeatureStop"
    CLASSIFYSTART = "ClassifyStart"
    CLASSIFYSTOP = "ClassifyStop"
    TRAINSTART = "TrainStart"
    TRAINSTOP = "TrainStop"