import configparser

import tiktoken
from transformers import AutoTokenizer

from db import DataBase
from prompt_templates.prompt_template_1 import prompt_template_1
from prompt_templates.prompt_template_2 import prompt_template_2
from prompt_templates.system_prompt import system_prompt


class PromptBuilder:
    def __init__(self):
        """
        This class is responsible for constructing the prompt for the LLM given a reference to a method in the database
        :param db_name: the name of the database
        :param max_tokens: the maximum number of tokens allowed in the prompt
        """
        self.db = DataBase()

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.USE_MODEL = self.config.getboolean('MODEL', 'USE_MODEL')

        if self.USE_MODEL:
            self.MODEL_PATH = self.config.get('MODEL', 'MODEL_PATH')

        self.max_tokens = int(self.config.get('MODEL', 'MODEL_MAX_INPUT_TOKENS'))

    def construct_initial_prompt(self, method_id):
        method = self.db.get_method_by_id(method_id)
        method_name = method["methodIdentifier"]
        class_name = method["classIdentifier"]
        size = 1
        prompt = ""
        while size <= 4 and self.check_token_limit(
                self._generate_prompts_with_different_size(method_name, class_name, method)):
            prompt = self._generate_prompts_with_different_size(method_name, class_name, method)
            size += 1

        return prompt

    def construct_initial_prompt_class(self, class_identifier):
        class_ = self.db.get_class(class_identifier)
        class_name = class_identifier
        size = 1
        prompt = self._generate_prompts_for_class(class_name, class_)
        while size <= 4 and self.check_token_limit(self._generate_prompts_for_class(class_name, class_)):
            prompt = self._generate_prompts_for_class(class_name, class_)
            size += 1
        return prompt

    def construct_initial_prompt_method(self, method_identifier, class_identifier):
        method_id = self.db.get_method_id(method_identifier, class_identifier)
        method = self.db.get_method_by_id(method_id)
        size = 1
        while size <= 4 and self.check_token_limit(self._generate_prompts_for_method_(method, class_identifier)):
            prompt = self._generate_prompts_for_method_(method, class_identifier)
            size += 1
        return prompt

    def construct_error_prompt(self, method_id, error_message):
        pass

    @staticmethod
    def construct_code_prompt_from_dict_list(code_list, language_identifier, is_method):
        """
        Constructs a prompt from a list of code snippets.
        :param code_list: the list of code snippets
        :param language_identifier: the language identifier
        :param is_method: True if the code snippets are methods, False otherwise
        :return: Single string containing all code snippets wrapped in code blocks
        """
        prompt = ""
        for code in code_list:
            if is_method:
                prompt += "This is the method: " + str(code["methodIdentifier"]) + " of the class " + str(
                    code["classIdentifier"]) + ":\n"
            prompt += "```" + language_identifier + "\n"
            prompt += str(code["fullText"])
            prompt += "\n```\n"
        return prompt if prompt != "" else "No relations found."

    def check_token_limit(self, prompt: str):
        """
        Checks if the prompt is too long for the given token limit.
        :param prompt: the prompt to check
        :param token_limit: the token limit to check against
        :return: True if the prompt is too long, False otherwise
        """
        if self.USE_MODEL:
            tokens = self.tokenize_with_model(prompt, self.MODEL_PATH)
        else:
            tokens = self.tokenize_with_tiktoken(prompt)
        return len(tokens) < self.max_tokens

    def tokenize_with_model(self, prompt: str, model_path: str):
        """
        Generates a list of tokens for the prompt.
        Uses the Llama tokenizer provided by llama-cpp-python.
        :param prompt: the prompt to generate tokens for
        :param model_path: the path to the model to use
        :return: A list of integers representing the tokens
        """
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        tokens = tokenizer.encode(prompt, truncation=True, max_length=self.max_tokens)
        return tokens

    @staticmethod
    def tokenize_with_tiktoken(prompt: str):
        """
        Generates a list of tokens for the prompt using tiktoken with the cl100k_base encoding.
        Using this method can be useful when running the application with OpenAI models, as they use
        the same encoding.
        :param prompt: the prompt to generate tokens for
        :return: A list of integers representing the tokens
        """
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(prompt)
        return tokens

    @staticmethod
    def _generate_prompts_with_different_size(method_name: str,
                                              class_name: str,
                                              method: dict):
            prompt_template = "\n".join(
                [
                    system_prompt,
                    prompt_template_1
                ])

            return prompt_template.format(
                method_name=method_name,
                class_name=class_name,
                method_code=method["fullText"],
                testing_framework="Unittest",
                mocking_framework="MagicMock",
            )
    @staticmethod
    def _generate_prompts_for_class(class_name: str,
                                              class_: dict):
            prompt_template = "\n".join(
                [
                    system_prompt,
                    prompt_template_2
                ])

            return prompt_template.format(
                class_name=class_name,
                class_code=class_["fullText"],
                testing_framework="Unittest",
                mocking_framework="MagicMock",
            )
    @staticmethod
    def _generate_prompts_for_method_(method: dict,
                                              class_: str):

            prompt_template = "\n".join(
                [
                    system_prompt,
                    prompt_template_1
                ])

            return prompt_template.format(
                method_name=method["methodIdentifier"],
                class_name=class_,
                method_code = method["fullText"],
                testing_framework="Unittest",
                mocking_framework="MagicMock",
            )


