from db import DataBase
import os
import json


def convert_json_to_db(project_names: str):
    """
    Converts the json files to a database
    :param project_names: list of selected projects in /build/class_parser to convert to database
    :return:
    """
    for project_name in os.listdir("./build/class_parser"):
        if project_name not in project_names:
            continue
        # create new database for every project for faster querying and avoiding conflicts between projects
        db = DataBase()
        db.reset()
        db.create_tables()

        # insert project
        db.insert_project(str(project_name))

        n_classes = len(os.listdir("./build/class_parser/" + project_name))
        curr_class = 1
        # loop over all classes
        for class_name in os.listdir("./build/class_parser/" + project_name):
            if os.path.exists("./build/class_parser/" + project_name + "/" + class_name + "/class.json") \
                    and os.path.exists("./build/class_parser/" + project_name + "/" + class_name + "/methods.json"):
                class_file = open("./build/class_parser/" + project_name + "/" + class_name + "/class.json", "r")
                method_file = open("./build/class_parser/" + project_name + "/" + class_name + "/methods.json", "r")
                with class_file:
                    class_list = json.load(class_file)
                with method_file:
                    method_list = json.load(method_file)
                for class_dict in class_list:
                    # write to database
                    db.insert_class(
                                    project_name,
                                    class_dict.get("filepath"),
                                    class_dict.get("class_identifier"),
                                    class_dict.get("class_body")
                    )

                    for method_dict in method_list:
                        # write methods of class to database
                        db.insert_method(method_dict["method_identifier"],
                                         class_dict["class_identifier"],
                                         method_dict["method_full_text"])

                        methodId = db.get_method_id(method_dict["method_identifier"], class_dict["class_identifier"])

        curr_class = 1
        # create intra-project relations
        for class_name in os.listdir("./build/class_parser/" + project_name):

            if os.path.exists("./build/class_parser/" + project_name + "/" + class_name + "/class.json") \
                    and os.path.exists("./build/class_parser/" + project_name + "/" + class_name + "/methods.json"):
                class_file = open("./build/class_parser/" + project_name + "/" + class_name + "/class.json", "r")
                method_file = open("./build/class_parser/" + project_name + "/" + class_name + "/methods.json", "r")
                with class_file:
                    class_list = json.load(class_file)

                with method_file:
                    method_list = json.load(method_file)
                for class_dict in class_list:
                    for method_dict in method_list:
                        source_method_id = db.get_method_id(method_dict["method_identifier"],
                                                            class_dict["class_identifier"])