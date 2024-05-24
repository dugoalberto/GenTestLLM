import argparse

from together import Together

import db
from Python_parser import PythonCodeParser
from rich.console import Console
import argparse

from TestGenerator import TestGenerator
from json_to_db import convert_json_to_db
from scanner import FileSystemScanner

def project_choice(args):
    proj = args
    project = FileSystemScanner(proj)
    files = project.parse()
    for project in [project for project in files]:
        for file in files[project]["files"]:
            my_python_parser.parse_file(file, args.split('/')[-1])



if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description='A project which you want to parse and generate tests for.')
    argument_parser.add_argument('--parseProj', type=str, default=None, metavar=('Path_to_Project'),
                                 help='Insert the name of the project which you want to parse and generate tests for.')

    argument_parser.add_argument('--genTestClass', type=str, default=None, metavar=('Class_Name'),
                                 help='When database for projects was already created, test generation can be run in isolation '
                                      '(no parsing to json files or database generation).'
                                      'Insert the name of the class which you want to generate tests for.')

    argument_parser.add_argument('--genTestMethod', type=str, default=None ,nargs=2, metavar=('Name_Class', 'Method_Name'),
                                 help='When database for projects was already created, test generation can be run in isolation '
                                      '(no parsing to json files or database generation).'
                                      'Insert the name of the method and the class which you want to generate tests for.')

    args = argument_parser.parse_args()
    console = Console()
    my_python_parser = PythonCodeParser()

    if args.parseProj is not None:
        proj = args.parseProj.split('/')[-1]
        project_choice(args.parseProj)
        convert_json_to_db(proj)

    elif args.genTestClass is not None:
        file = args.genTestClass
        test = TestGenerator(file)
        test.generate_tests_for_class(file)

    elif args.genTestMethod is not None:
        class_, method = args.genTestMethod
        test = TestGenerator(method)
        test.generate_tests_for_class(class_, method)