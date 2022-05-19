# THIS PROGRAM WORKS FINE AS LONG AS I IMPORT THE LIST OF URL KEYWORDS
# FROM AN EXTERNAL FILE data_file.py
import os
import requests
import codecs
from bs4 import BeautifulSoup
from data_file import NCT_LIST
OUTFILE = input('Output-File name (scrapperout.txt): ') or 'scrapperout.txt'
OUT = ''


def prep_output(nctnmbr, callback_fnct):
    return callback_fnct(nctnmbr)


def get_clinical_trial_data(nctid):
    out = ''
    print(nctid)
    data = BeautifulSoup(requests.get(
        "https://clinicaltrials.gov/ct2/show/" + nctid + "?displayxml=true").text, "xml")
    subset = ['condition', 'sponsors', 'phase']
    tag_dict = {f'ct{subset_detail.capitalize()}': [current_tag.text
                                                    for current_tag
                                                    in data.find_all(subset_detail)
                                                    if current_tag.text.strip()]
                for subset_detail in subset}
    result_data = {k: ", ".join(v) for (k, v) in tag_dict.items() if v}
    result_data['ctID'] = nctid
    for res in result_data:
        out += '\t' + \
            result_data[res].strip().replace('\n', ' ').replace('\t', ' ')
    return out.strip()


for nct in NCT_LIST:
    OUT += prep_output(nct, get_clinical_trial_data) + '\n'
    print(OUT)
with codecs.open(OUTFILE, "w", "utf-8") as f:
    f.write(OUT)
os.system(OUTFILE)
