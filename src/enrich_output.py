from xml_tools import information_for_wordnet, insert_tags_for_token
from lesk import nltk_lesk


def enrich_plain_with_lesk(root):
    token_list, lemma_list, pos_tag_list = information_for_wordnet(root)
    synset_list = nltk_lesk(token_list, lemma_list, pos_tag_list)

    tag_list_list = [["wordnet", synset] for synset in synset_list]

    new_root = insert_tags_for_token(root, tag_list_list)

    return root
