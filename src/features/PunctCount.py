short_name = "PunctCount"
long_name = "Punctuation Count"
description = "Number of each type of punctuation in the sample."

plain_text = False

__punctuation__ = {
    "PunctPeriod" : ".",
    "PunctComma" : ",",
    "PunctExclamation" : "!",
    "PunctQuestion" : "?",
}

def extract(sample):
    rVal = {}

    sample_length = len(sample)

    for key, value in __punctuation__.items():
        rVal[key] = round((float(sample.count(value)) / sample_length) * 100, 2)

    return rVal