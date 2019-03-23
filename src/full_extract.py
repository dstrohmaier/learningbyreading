import os
from os.path import join

from optparse import OptionParser
from candc import postag, tokenize, get_drs

import logging as log
from lxml import etree
from xml_tools import insert_tags_for_token, all_tokens

log.basicConfig(level=log.INFO)

parser = OptionParser()
parser.add_option('-d',
                  '--input-dir',
                  dest="input_dir",
                  help="read en_raw text files from DIRECTORY",
                  metavar="DIRECTORY")
parser.add_option('-s',
                  '--semantics',
                  dest="semantics",
                  default="drs",
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
    
    return drs_string, tokenized


def create_offsets(text, token_list):
    current = 0
    offset_list = []
    
    for token in token_list:
        token_len = len(token)
        while text[current:current+token_len] != token:
            current += 1

        offset_list.append((current, current+token_len))
        current += token_len

    return offset_list

def create_xml(drs_string, text, tokenized):
    log.info("creating xml")
    assert type(drs_string) == str, "drs_string has to be string is {} instead".format(type(drs_string))
    
    root = etree.fromstring(drs_string) 

    #pos_text = postag(tokenized)
    #pos_list = extract_pos_list(pos_text)

    token_list = all_tokens(root)

    compare_token_list = tokenized.split()
    if compare_token_list[-1] == "<EOF>":
        compare_token_list = compare_token_list[:-1] # get rid of my EOF
    #print("List of tokens: ", token_list)

    if token_list != compare_token_list:
        log.warning("token_list != compare_token_list\n***\ntoken_list: {}\n***\ncompare_token_list: {}".format(token_list, compare_token_list))
    
    offset_list = create_offsets(text, token_list)
    tag_list_list = []
    
    for i, token in enumerate(token_list):
        tag_list = [#("tok", token_list[i]),
                    #("pos", pos_list[i]),
                    ("from", str(offset_list[i][0])),
                    ("to", str(offset_list[i][1]))
        ]

        tag_list_list.append(tag_list)

    root = insert_tags_for_token(root, tag_list_list)
    doc = etree.ElementTree(root)
    
    return doc
    
def create_directory_data(directory_to_walk):
    log.info("starting to walk directory: {}".format(directory_to_walk))
    for walk_return in os.walk(directory_to_walk):
        directory = walk_return[0]

        text_file = join(directory, "en.raw")
        
        if not os.path.isfile(text_file):
            continue

        log.info("In directory: {}".format(directory))
        
        with open(text_file, "r") as infile:
            text = infile.read()
            text += "\n<EOF>"
                
        drs_string, tokenized = create_drs_string(text, options.semantics)

        doc = create_xml(drs_string, text, tokenized)

        output_file = join(directory, "en.boxer.drs.xml")
        with open(output_file, "w") as outfile:
            doc.write(outfile, pretty_print=True)

create_directory_data(options.input_dir)