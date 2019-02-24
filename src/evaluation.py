import os
from os.path import join

import logging as log
import pandas as pd

from xml_tools import load_xml, all_evaluation_data

class evaluator:
    def __init__(self,
                 starting_directory,
                 standard_name="en.drs.xml",
                 evaluation_name="en.boxer.drs.xml",
                 output_name="full_data.tsv"):

        self.read = False
        self.starting_directory = starting_directory
        self.standard_name = standard_name
        self.evaluation_name = evaluation_name
        self.output_name = output_name


    def read_in_data(self):
        full_data_list = []
        
        for walk_return in os.walk(self.starting_directory):
        directory = walk_return[0]
        head, tail = os.path.split(directory)
        _, second_tail = os.path.split(head)
        file_id = second_tail + "_" + tail

        standard_file = join(directory, self.standard_name)
        evaluation_file = join(directory, self.evaluation_name)
        
        if not os.isfile(standard_file) or not os.isfile(evaluation_file):
            continue

        with open(standard_file, "r") as sf, open(evaluation_file, "r") as ef:
            standard_tree = load_xml(sf)
            evaluation_tree = load_xml(ef)

            s_data, e_data, results = self.compare_trees(standard_tree, evaluation_tree)
            file_dict_list = self.create_file_dict_list(s_data, e_data, results, file_id)
            
            full_data_list.extend(file_dict_list)

        self.data = pd.DataFrame(full_data_list)
        self.read = True


    def compare_trees(self, standard_tree, evaluation_tree):
        results = []
        
        s_synsets, s_from_list, s_to_list = all_evaluation_data(standard_tree)
        e_synsets, e_from_list, e_to_list = all_evaluation_data(evaluation_tree)

        current_e_position = 0

        e_data = []
        s_data = []
        
        for current_s_position, s_syn in enumerate(s_synsets):
            s_from = s_from_list[current_s_position]
            e_from = e_from_list[current_e_position]

            s_to = s_to_list[current_s_position]
            e_to = e_to_list[current_e_position]

            e_syn = e_synsets[current_e_position]

            while s_from > e_from:
                e_data.append((e_from, e_to, e_syn))
                
                current_e_position += 1
                e_from = e_from_list[current_e_position]
                e_to = e_to_list[current_e_position]
                e_syn = e_synsets[current_e_position]
            
            if s_from < e_from:
                results.append(False)
                s_data.append((s_from, s_to, s_syn))
            elif s_from == e_from and s_to == e_to and s_syn == e_syn:
                results.append(True)
                e_data.append((e_from, e_to, e_syn))
                s_data.append((s_from, s_to, s_syn))  
                current_e_position += 1
            else:
                s_data.append((s_from, s_to, s_syn))  
                results.append(False)
        
        return s_data, e_data, results

    def create_file_dict_list(self, s_data, e_data, results, file_id):
        dict_list = []
        
        for s_row, e_row, result_value in zip(s_data, e_data, results):
            s_from, s_to, s_syn = s_row
            e_from, e_to, e_syn = e_row

            current_dict = {
                "result": result_value,
                "s_from": s_from,
                "s_to": s_to,
                "s_syn": s_syn,
                "e_from": e_from,
                "e_to": e_to,
                "e_syn": e_syn,
                "file_id": file_id
            }

            dict_list.append(current_dict)

        return dict_list
        
        
    def save_data(self, directory=None):
        assert self.read, "Data need to be read in before saving"

        if directory == None:
            directory = self.starting_directory

        file_path = join(directory, self.output_name)
        self.data.to_csv(file_path, sep="\t", encoding="utf-8", header=True)

    
    def calculate_micro_accuracy(self):
        assert self.read, "Data need to be read in before micro-averaged accuracy can be calculated"
        
        correct_number = self.data["result"].count(True)
        return correct_number / len(self.data["result"])
        

    def calculate_macro_accuracy(self):
        assert self.read, "Data need to be read in before micro-averaged accuracy can be calculated"
        pass
    
    def significance_test(self):
        pass

    
