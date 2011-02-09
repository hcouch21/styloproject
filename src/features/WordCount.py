short_name = "WordCount"
long_name = "Word Count"
description = "Number of words in the sample."

plain_text = False

def extract(sample):
    return len(sample)