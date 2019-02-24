import logging as log
from lxml import etree

log.basicConfig(level=log.INFO)

def load_xml(file_path):
    tree = etree.parse(file_path)
    return tree

def insert_tags_for_token(root, tag_list_list):
    tags_element_list = root.findall(".//tags")
    
    #print(root)
    #print(etree.tostring(root))
    #print(tags_element_list)
    #print(type(tags_element_list))
    
    assert len(tags_element_list) == len(tag_list_list), "Length of tags_element_list and tag_list_list has to be equal, currently {} != {}\n***\ntags_element_list: {}\n***\ntag_list_list: {}".format(len(tags_element_list), len(tag_list_list), tags_element_list, tag_list_list)
    
    for tags, tag_list in zip(tags_element_list, tag_list_list):
        previous_tags = tags.findall("tag")
        last_tag = previous_tags[-1]
        for tag_type, tag_text in tag_list:
            kwargs = {"type": tag_type}
            new_tag = etree.Element("tag", **kwargs)
            new_tag.text = tag_text
            last_tag.addnext(new_tag)
            last_tag = new_tag

    return root


def information_for_wordnet(root):
    token_list = root.xpath(".//tags/tag[@type='tok']/text()")
    lemma_list = root.xpath(".//tags/tag[@type='lemma']/text()")
    pos_list = root.xpath(".//tags/tag[@type='pos']/text()")

    return token_list, lemma_list, pos_list

def tags_from_all_tag_type(root, type_name):
    tags_element_list = root.xpath(".//tags/tag[@type='{}']/..".format(type_name))

    #print(tags_element_list)
    return tags_element_list



def all_token_synsets(root):
    synsets = root.xpath(".//tags/tag[@type='wordnet']/text()")
    return synsets

def all_tokens(root):
    token_list = root.xpath(".//tags/tag[@type='tok']/text()")
    return token_list


def all_evaluation_data(root):
    synsets = root.xpath(".//tags/tag[@type='wordnet']/text()")
    from_list = root.xpath(".//tags/tag[@type='from']/text()")
    to_list = root.xpath(".//tags/tag[@type='wordnet']/text()")

    
    return synsets, from_list, to_list

def text_from_tag_type_for_token(root, token_start, token_end, token_name, type_name):
    #print("started text_from_tag_type_for_token")
    
    for tags_element in tags_from_all_tag_type(root, type_name):
        #print("new tags_element: ", tags_element)
        start_cond = False
        end_cond = False
        name_cond = False
        
        text = None
        
        children = tags_element.getchildren()

        for child in children:
            #print("new child: ", child)
            if child.attrib["type"] == "from" and child.text == token_start:
                #print("start_cond found")
                start_cond = True
            elif child.attrib["type"] == "to" and child.text == token_end:
                #print("end_cond found")
                end_cond = True
            elif child.attrib["type"] == "tok" and child.text == token_name:
                #print("name_cond found")
                name_cond = True
            

            if child.attrib["type"] == type_name:
                text = child.text

        if all((start_cond, end_cond, name_cond, text)):
            return text
    #text = root.xpath(".//tags/tag[type='{}']/../tag[type='tok']".format(type_name))
    # should I rather raise an error, if nothing is found?

    log.error("Did not find token when looking in xml file")
    
    return None
