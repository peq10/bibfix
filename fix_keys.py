'''
A script to change all keys in a .bib file to the format: 
    <firstauthorlastname><year><first meaningful word of title>
    
requires bibtexparser https://bibtexparser.readthedocs.io/en/master/

'''

import bibtexparser as btp
import copy
import re
import argparse
from pathlib import Path
import ast

def fix_bibkeys(path_to_bib, skip_words = ['a','the','an']):
    '''
    Changes all keys in a .bib file to the format: 
    <firstauthorlastname><year><first meaningful word of title>

    This helps with e.g. citing same thing twice with different keys if your 
    .bib file has been cobbled together from multiple sources.


    Parameters
    ----------
    path_to_bib : string
        Path to the bib file containing the entries .
    
    skip-words : list of strings.
        List of words which will be skipped over in the title of bib entries 
        i.e. defines what is not 'meaningful'

    Returns
    -------
    None.
    
    Places the file <name of old bibfile>_clean.bib in the same directory with the cleaned entries.
    

    '''
    path_to_bib = Path(path_to_bib)
    clean_bib_path = Path(f'{path_to_bib.parent}/{path_to_bib.stem}_clean.bib')
    
    with open(path_to_bib) as bibtex_file:
        bibtex_str = bibtex_file.read()
    
    
    parser = btp.bparser.BibTexParser(common_strings=True)
    
    bib_database = btp.loads(bibtex_str,parser = parser)
    
    clean_bib = btp.bibdatabase.BibDatabase()
    
    for idx,entry in enumerate(bib_database.entries):
        names = entry['author'].split()
        if names[0][-1] == ',':
            surname = names[0][:-1].lower()
        else:
            surname = names[1].lower()
            
        surname = re.sub(r'\W+','',surname)
            
        year = entry['year']
        
        clean_title = re.sub(r'([^\s\w]|_)+', '',entry['title'].lower()).split()
        
        if clean_title[0] in skip_words:
            title = clean_title[1]
        else:
            title = clean_title[0]
        
    
        entry2 = copy.copy(entry)
        entry2['ID'] = f'{surname}{year}{title}'
        clean_bib.entries.append(entry2)
    
        if entry['ID'] != entry2['ID']:
            #print(names)
            #print(entry['title'])
            print(f'{surname}{year}{title}')
            print(entry['ID'])
            print('\n')
    
    with open(clean_bib_path, 'w') as bibtex_file:
        btp.dump(clean_bib, bibtex_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('bib_path', type = str, help = 'Path to bib file to clean')
    parser.add_argument('--skip',dest = 'skip_words' ,type = str,  default = "['a','the','an']")
    
    args = parser.parse_args()
    args.skip_words = ast.literal_eval(args.skip_words)
    
    fix_bibkeys(args.bib_path, skip_words = args.skip_words)