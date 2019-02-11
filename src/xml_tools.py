from lxml import etree

def insert_tags_for_token(root, tag_list_list):
    tags_element_list = root.findall("tags")
    assert len(tags_element_list) == len(tag_list_list), "Length of tags_element_list and tag_list_list has to be equal, currently {} != {}".format(len(tags_element_list), len(tag_list_list))
    
    for tags, tag_list in zip(tags_element_list, tag_list_list):
        for tag_type, tag_text in tag_list:
            kwargs = {"type": tag_type}
            new_tag = etree.SubElement(tags, "tag", **kwargs)
            new_tag.text = tag_text

    return root
