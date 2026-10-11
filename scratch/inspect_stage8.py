with open('scratch/day_data_010.py') as f:
    text = f.read()

import re
pos = text.find("DATA['topics'][0]['lab']['steps'][7]")
print(text[pos:pos+1500])
