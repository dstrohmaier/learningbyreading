import os
from optparse import OptionParser
from candc import tokenize, get_all, get_fol

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


def create_drs(text):
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

    log.info("Parsing")
    drs = get_all(tokenized)
    #fol = get_fol(tokenized)

    return tokenized, drs


def create_tags(text, tokenized, drs, i):
    tag_list = [("tok", tokenized[i]),
    ]

    return tag_list

def create_xml(text, tokenized, drs):
    print("tokenized: ", tokenized)
    
    root = etree.Element("xdrs-output",
                         version="'boxer v1.00'")
    doc = etree.ElementTree(root)
    
    xdrs = etree.SubElement(root, "xdrs")
    tagged_tokens = etree.SubElement(xdrs, "taggedtokens")
    for i, token in enumerate(tokenized):
        tag_token = etree.SubElement(tagged_tokens, "tagtoken")
        tags = etree.SubElement(tag_token, "tags")
        for tag, tag_text in create_tags(text, tokenized, drs, i):
            new_tag = etree.SubElement(tags, tag)
            new_tag.text = tag_text

    return doc

if options.input_file:
    documents = [options.input_file]
else:
    documents = [ join(options.input_dir,f) for f in listdir(options.input_dir) if isfile(join(options.input_dir,f)) ]

for filename in documents:
    # read file
    log.info("opening file {0}".format(filename))
    with open(filename) as f:
        text = f.read()
        

    tokenized, drs = create_drs(text)
    doc = create_xml(text, tokenized, drs)

    with open(options.output_file, "w") as outfile:
        doc.write(outfile)
