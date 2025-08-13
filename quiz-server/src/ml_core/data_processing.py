"""
    Class will contain all the functions necessary for preprocessing data, e.g. tokenization, converting to dataframes
"""

from typing import List, Dict, Any
import pandas as pd

class DataPrepocessor:
    # functions to preprocess data
    # e.g. store in pandas df, tokenise, lemmatization

    def tokenise(self, text: str):
        return text.split("\n")

    def convert_to_df(self, user: Dict[str,Any], answers: List[Dict[str, Any]], logs: List[Dict[str, Any]]):
        # initialize dictionary to create df
        data_dict= {}

        # loop through answers and then logs for following structure:
        # (index)    user_id    answer    question    log_action    log_time
        for answer in answers:
            data_dict["user_id"] = user["id"]
            data_dict["answer"] = answer["answer"]
            data_dict["question"] = answer["question"]
            data_dict["correct_answer"] = answer["correctAnswer"]
            for log in logs:
                data_dict["log_action"] = log["action"]
                data_dict["log_time"] = log["time"]
        print(data_dict)

        # add index attribute for automatic indexing, otherwise, ValueError for index not existing
        df = pd.DataFrame(data_dict, index=[0])
        return df