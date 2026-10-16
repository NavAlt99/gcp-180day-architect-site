import re
import urllib.parse
from bs4 import BeautifulSoup

spec_path = "scratch/day_data_010.py"
spec_text = open(spec_path).read()

# Let's inspect DATA['contract_version']
if "'contract_version': 1" in spec_text:
    spec_text = spec_text.replace("'contract_version': 1", "'contract_version': 2", 1)
    print("Updated contract_version to 2")
elif "'contract_version': 2" in spec_text:
    print("contract_version is already 2")

with open(spec_path, "w") as f:
    f.write(spec_text)
