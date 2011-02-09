short_name = "CharCount"
long_name = "Character Count"
description = "Number of characters in the sample."

plain_text = True

def extract(sample):
    return len(sample)