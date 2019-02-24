import nltk


def convert_tags(pos_tag):
    noun_tags = ("NN",
                 "NP",
                 "NNS",
                 "NPS")

    verb_tags = ("VB",
                 "VBD",
                 "VBG",
                 "VBN",
                 "VBP",
                 "VBZ",)
    
    if pos_tag in noun_tags:
        return "n"
    elif pos_tag in verb_tags:
        return "v"
    else:
        return "other"

def nltk_lesk(token_list, lemma_list, pos_tag_list):
    synset_list = []

    

    wordnet_tag_list = [convert_tags(pos_tag) for pos_tag in post_tag_list]
    
    for lemma, wn_tag in zip (lemma_list, wordnet_tag_list):
        if wn_tag in ("n", "v"):
            synset = nltk.wd.lesk(token_list, lemma, wn_tag)
        else:
            synset = O
        synset_list.append()
    
    return synset_list
