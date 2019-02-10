import os
from optparse import OptionParser
from candc import tokenize, get_drs

import logging as log
from lxml import etree


log.basicConfig(level=log.INFO)

# command line argument partsing
parser = OptionParser()
parser.add_option('-i',
                  '--input',
                  dest="input_file",
                  help="read text from FILE",
                  metavar="FILE")
parser.add_option('-d',
                  '--input-dir',
                  dest="input_dir",
                  help="read text files from DIRECTORY",
                  metavar="DIRECTORY")
parser.add_option('-o',
                  '--output',
                  dest="output_file",
                  help="write JSON to FILE",
                  metavar="FILE")
parser.add_option('-t',
                  '--tokenized',
                  action="store_true",
                  dest="tokenized",
                  help="do not tokenize input")
parser.add_option('-c',
                  '--comentions',
                  action="store_true",
                  dest="comentions",
                  help="output co-mentions")
(options, args) = parser.parse_args()


def create_drs_string(text):
    # tokenization
    if not options.tokenized:
        log.info("Tokenization")
        tokens = tokenize(text)
        if not tokens:
            log.error("error during tokenization of file '{0}', exiting".format(filename))
            return None
        tokenized = "\n".join([' '.join(sentence) for sentence in tokens[:-1]])
    else:
        tokenized = text

    #print(postag(tokenized))
    log.info("Parsing")
    drs_string = get_drs(tokenized)
    
    return drs_string

if options.input_file:
    documents = [options.input_file]
else:
    documents = [ join(options.input_dir,f) for f in listdir(options.input_dir) if isfile(join(options.input_dir,f)) ]

for filename in documents:
    # read file
    log.info("opening file {0}".format(filename))
    with open(filename) as f:
        text = f.read()
        
    drs_string = create_drs_string(text)
    log.info("Test for debugging")
    print("type drs_string: ", type(drs_string))
    print(drs_string)

    doc = etree.fromstring(drs_string) 
    
    with open(options.output_file, "w") as outfile:
        doc.write(outfile, pretty_print=True)
