from os.path import join

from xml_tools import load_xml, text_from_tag_type_for_token, all_token_synsets

def retrieve_single_wordnet_test():
   #  should find wordnet of this token:
   #  <tagtoken xml:id="i1005">
   #    <tags>
   #      <tag type="verbnet" n="0">[]</tag>
   #      <tag type="tok">school</tag>
   #      <tag type="cat">n</tag>
   #      <tag type="sym">school</tag>
   #      <tag type="lemma">school</tag>
   #      <tag type="from">9</tag>
   #      <tag type="to">15</tag>
   #      <tag type="pos">NN</tag>
   #      <tag type="sem">CON</tag>
   #      <tag type="wordnet">school.n.02</tag>
   #    </tags>
   # </tagtoken>

    
    
    file_path = join("..", "data", "gold", "p02", "d0945", "en.drs.xml")
    # supposed to be called from learningbyreading folder, not learn*/src
    tree = load_xml(file_path)
    root = tree.getroot()

    text = text_from_tag_type_for_token(root, "9", "15", "school", "wordnet")
    
    if text == "school.n.02":
        print("Test works: {} == school.n.02".format(text))
    else:
        print("Test failed: {} != school.n.02".format(text))

def retrieve_all_wordnet_test():
    file_path = join("..", "data", "gold", "p02", "d0945", "en.drs.xml")
    # supposed to be called from learningbyreading folder, not learn*/src
    tree = load_xml(file_path)
    root = tree.getroot()

    synsets_list = all_token_synsets(root)
    goal = ["O", "be.v.03", "O", "O", "school.n.02", "O"]
    
    if synsets_list == goal:
        print("Test works: {} == {}".format(synsets_list, goal))
    else:
        print("Test failed: {} != {}".format(synsets_list, goal))

        
if __name__ == "__main__":
    print("testing retrieval of single wordnet from single xml_file")
    retrieve_single_wordnet_test()

    print("************")
    print("testing retrieval of all token wordnets from single xml_file")
    retrieve_all_wordnet_test()
