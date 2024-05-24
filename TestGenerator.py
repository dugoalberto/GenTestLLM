import configparser
import re
from datetime import datetime
from timeout_decorator import timeout
import requests
from openai import OpenAI
import os
import configparser
import logging

from together import Together

from PromptBuilder import PromptBuilder
from Python_parser import PythonCodeParser
from db import DataBase
from llm import HuggingFaceLlm, TogetherLlm
from utils import log_to_csv, make_dir_if_not_exists, write_file


class TestGenerator:
    def __init__(self, project_name):
        print("Initializing Test Generator")
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.USE_HUGGINGFACE = self.config.getboolean('INFERENCE', 'USE_HUGGINGFACE')
        self.USE_TOGETHER_INFERENCE = self.config.getboolean('INFERENCE', 'USE_TOGETHER_INFERENCE')

        if self.USE_HUGGINGFACE and self.USE_HUGGINGFACE:
            raise Exception("Cannot use both HuggingFace and Local Web Server for inference")
        elif self.USE_HUGGINGFACE:
            self.llm = HuggingFaceLlm()
        elif self.USE_TOGETHER_INFERENCE:
            self.llm = TogetherLlm()
        print("LLM initialized", self.llm)
        self.client = OpenAI(base_url="http://localhost:8000/v1", api_key="lm-studio")
        #self.client = OpenAI(api_key="your_api")
        #self.client = OpenAI(base_url="http://padova.zucchetti/", api_key="not-needed")

        self.project_name = project_name

        self.current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.db = DataBase()
        self.prompt_constructor = PromptBuilder()
        self.python_parser = PythonCodeParser()
    def generate_target_filepath(self,  target: str):
        filepath = self.db.get_filepath_for_class(target)
        filepath = filepath.split('/')
        start_idx = filepath.index('Assertion') + 1
        filepath = filepath[start_idx:-1]
        filepath_prefix = ['build', 'generated_tests', target]
        execution_folder_prefix = ['execution']

        execution_filepath = os.path.join(*(filepath_prefix + execution_folder_prefix))
        prompt_path = os.path.join(*(['build', 'prompts', target] + filepath))

        return {
            'execution_filepath': execution_filepath,
            'prompt_path': prompt_path
        }
    def get_answer(self, prompt):
        print("> Prompt created, querying LLM")
        if prompt:
            logging.info("Prompt created: " + prompt)
        else:
            Exception("Prompt is None")
        if self.llm:
            print("Using Together API")
            answer = self.llm(prompt)
        else:
            print("Using Local LLM")
            answer = self.client.chat.completions.create(
                model="local-model",
                messages=[
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=512,
            )
        return answer
    def create_target_folders(self, filepaths):
        # create folder if not exists
        for folder in filepaths:
            if folder != "build":
                make_dir_if_not_exists(filepaths[folder])
    @staticmethod
    def clean_code(code: str):
        # Rimuove tutto prima della parola 'class'
        code = re.sub(r'^[\s\S]*?(?=class)', '', code)
        # Rimuove tutte le triple virgolette e il loro contenuto
        code = re.sub(r'\`\`\`[\s\S]*?\`\`\`', '', code)
        return code
    @timeout(20, use_signals=True)
    def generate_tests_for_class(self, class_identifier:str, method=None):
        try:
            logging.info("Generating test for class " + str(class_identifier))
            if method:
                prompt = self.prompt_constructor.construct_initial_prompt_method(method, class_identifier)
            else:
                prompt = self.prompt_constructor.construct_initial_prompt_class(str(class_identifier))
            logging.info("Prompt created: " + prompt)
            if prompt:
                answer = self.get_answer(prompt)
                if not answer:
                    logging.info("Could not extract answer from LLM, skipping class")
                    return
                filepaths = self.generate_target_filepath(class_identifier)
                if self.USE_TOGETHER_INFERENCE:
                    answerToInsert = self.clean_code(answer['choices'][0]['message']['content'])
                else:
                    answerToInsert = self.clean_code(answer.choices[0].message.content)

                self.create_target_folders(filepaths)
                write_file(filepaths['prompt_path'], class_identifier + "_prompt.md", "", prompt)
                write_file(filepaths['execution_filepath'], class_identifier + "_test.py", "", answerToInsert)

                print("> Wrote test to file, compiling...")

        except Exception as e:
            logging.exception("Exception occurred " + str(e))
            print("Exception occurred " + str(e))
            print("Skipping class")
            log_to_csv(self.project_name, class_identifier,
                       "Other Error", 1, str(e))
            return