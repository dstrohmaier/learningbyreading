import os
from os.path import join

from optparse import OptionParser
from candc import tokenize, get_drs

import logging as log
from lxml import etree

parser = OptionParser()
parser.add_option('-d',
                  '--input-dir',
                  dest="input_dir",
                  help="read en_raw text files from DIRECTORY",
                  metavar="DIRECTORY")
parser.add_option('-s',
                  '--semantics',
                  dest="semantics",
                  help="boxer semantics options")
(options, args) = parser.parse_args()


def create_drs_string(text, semantics):
    # tokenization
    log.info("Tokenization")
    tokens = tokenize(text)
    if not tokens:
        log.error("error during tokenization of file '{0}', exiting".format(filename))
        return None
    tokenized = "\n".join([' '.join(sentence) for sentence in tokens[:-1]])

    #print(postag(tokenized))
    log.info("Parsing")
    drs_string = get_drs(tokenized, semantics)
    
    return drs_string


def create_directory_data(directory_to_walk):
    for walk_return in os.walk(directory_to_walk):
        directory = walk_return[0]

        text_file = join(directory, "en.raw")
        
        if not os.isfile(text_file):
            continue
            
        with open(text_file, "r") as infile:
            text = infile.read()
            text += "\n<EOF>"
                
        drs_string = create_drs_string(text, options.semantics)

        root = etree.fromstring(drs_string) 
        doc = etree.ElementTree(root)

        output_file = join(directory, "en.boxer.drs.xml")
        with open(output_file, "w") as outfile:
            doc.write(outfile, pretty_print=True)

create_directory_data(options.input_dir)
