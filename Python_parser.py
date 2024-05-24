import json
from typing import List
import tree_sitter_python as tspython
from tree_sitter import Language, Parser
import os


class PythonCodeParser:
    """
    This class is responsible for parsing the Python code.
    """

    def __init__(self):
        """
        This method initializes the PythonCodeParser class and builds the parser.
        """
        PYTHON_LANGUAGE = Language(tspython.language(), 'python')

        self.parser = Parser()
        self.parser.set_language(PYTHON_LANGUAGE)

    def parse_file(self, filepath, project_name):
        with open(filepath, 'r') as file:
            try:
                file_content = file.read()
            except IOError:
                return {}

        tree = self.parser.parse(bytes(file_content, "utf8"))
        classes = PythonCodeParser.extract_classes_of_tree(tree)
        # extract metadata for each class in the file and extract methods of the class
        class_output_list = []
        for class_node in classes:
            class_output = PythonCodeParser.extract_class_information(project_name, class_node, filepath)
            method_output = PythonCodeParser.extract_all_method_information(class_node,
                                                                            class_output.get("class_identifier"),
                                                                            filepath)
            self.write_method_file(method_output, project_name, class_output.get("class_identifier"))
            class_output_list.append(class_output)
        if class_output_list:
            self.write_class_file(class_output_list, project_name, class_output.get("class_identifier"))

    @staticmethod
    def extract_class_information(project_name, class_node, filepath):
        class_identifier = [item.text for item in class_node.children if item.type == "identifier"][0].decode("utf-8")
        class_body = class_node.text.decode("utf-8")
        class_output = PythonCodeParser.construct_class_output_dict(project_name,
                                                                    filepath,
                                                                    class_identifier,
                                                                    class_body)

        return class_output


    @staticmethod
    def extract_all_method_information(class_node, class_identifier, filepath):
        """
        This method extracts information about a method including its identifier, parameters and full text.
        :param class_node: A method node produced by tree-sitter.
        :param class_identifier: Identifier of the class the method belongs to.
        :param filepath: Filepath of the Python file the method belongs to.
        :return: Dictionary containing all relevant information.
        """

        class_body = [item for item in class_node.children if item.type == "block"][0]
        class_methods = [node for node in class_body.children if node.type == "function_definition"]

        method_output_list = []
        for method in class_methods:
            method_identifier = [item.text for item in method.children if item.type == "identifier"][0].decode("utf-8")
            method_full_text = method.text.decode("utf-8")
            if method.prev_named_sibling is not None and (
                    method.prev_named_sibling.type == "comment" or method.prev_named_sibling.type == "block_comment"):
                method_full_text = method.prev_named_sibling.text.decode("utf-8") + "\n" + method_full_text
            method_output_list.append(PythonCodeParser.construct_method_output_dict(filepath,
                                                                                    class_identifier,
                                                                                    method_identifier,
                                                                                    method_full_text)
                                      )

        return method_output_list

    @staticmethod
    def extract_classes_of_tree(tree_node):
        """
        This method returns all Python classes of a tree node.
        :param tree_node: Tree returned by the tree-sitter parser.
        :return: List of classes.
        """
        classes = [node for node in tree_node.root_node.children if node.type == "class_definition"]

        return classes

    @staticmethod
    def find_nodes_with_type(node, node_type: str = None):
        """
        This method traverses all children nodes of the given node and
        returns a list of all nodes with the specified type.
        :param node: A node produced by tree-sitter.
        :param result: A list of nodes with the specified type.
        :param node_type: A string specifying the type of nodes to return.
        :return: List of nodes with the specified type.
        """
        result = []
        def dfs(node, node_type):
            if node.type == node_type:
                result.append(node)

            for child in node.children:
                dfs(child, node_type)

        dfs(node, node_type)

        return result



    @staticmethod
    def construct_class_output_dict(project_name, filepath, class_identifier, class_body):
        class_output = {
            "project_name": project_name,
            "filepath": filepath,
            "class_identifier": class_identifier,
            "class_body": class_body
        }

        return class_output

    @staticmethod
    def construct_method_output_dict(filepath, class_identifier, method_identifier,
                                     method_full_text):
        method_output = {
            "filepath": filepath,
            "method_identifier": method_identifier,
            "class_identifier": class_identifier,
            "method_full_text": method_full_text
        }
        return method_output
    @staticmethod
    def write_method_file(method_output_list, project_name, class_identifier):
        try:
            if not os.path.exists(f"./build/class_parser/{project_name}/{class_identifier}"):
                os.makedirs(f"./build/class_parser/{project_name}/{class_identifier}")
            with open(f"./build/class_parser/{project_name}/{class_identifier}/methods.json", "w") as file:
                file.write(json.dumps(method_output_list))
        except Exception as e:
            print(e)

    @staticmethod
    def write_class_file(class_output_list, project_name, class_identifier):
        try:
            if not os.path.exists(f"./build/class_parser/{project_name}/{class_identifier}"):
                os.makedirs(f"./build/class_parser/{project_name}/{class_identifier}")
            with open(f"./build/class_parser/{project_name}/{class_identifier}/class.json", "w") as file:
                file.write(json.dumps(class_output_list))
        except Exception as e:
            print(e)

    @staticmethod
    def extract_method_invocation_argument_types(method_invocation, variable_declarations):
        """
        This method extracts the types of the arguments of a method invocation.
        :param method_invocation: Method invocation to extract the argument types from.
        :param variable_declarations: Dictionary containing the variable declarations of the method.
        The keys are the names of the variables and the values are the types of the variables.
        :return: List of argument types following the order of the arguments in the method invocation.
        """
        arguments = [child for child in method_invocation.children if child.type == 'argument_list']
        argument_types = []
        for arg in arguments:
            if arg.type == "argument_list":
                arg = arg.text.decode("utf-8")
                if arg in variable_declarations:
                    argument_types.append(variable_declarations[arg])
        return argument_types

    @staticmethod
    def extract_variable_declarations_of_method(method_body):
        """
        This method extracts all variable declarations of a method.
        :param method_body: Method body to extract the variable declarations from.
        :return: string containing the names of the variables.
        """
        declarations = PythonCodeParser.find_nodes_with_type(method_body, "attribute")
        variable_name = []
        for declaration in declarations:
            variable_name.append(declaration.text.decode("utf-8"))
        return variable_name

    def extract_class_name(self, filepath: str):
        """
        Extract the name of the class given a filepath to a Python file.
        :param filepath: Path to the Python file.
        :return: Name of the class.
        """
        with open(filepath, 'r') as file:
            try:
                file_content = file.read()
            except IOError:
                return {}

        tree = self.parser.parse(bytes(file_content, "utf8"))
        class_declaration = [node for node in tree.root_node.children if node.type == "class_declaration"]
        if class_declaration:
            class_declaration = class_declaration[0]
            class_name = \
            [node.text.decode("utf-8") for node in class_declaration.children if node.type == "identifier"][0]
            return class_name
        else:
            return None

