
import os
import warnings

from openai import OpenAI
from transformers import pipeline

from utils import measure_execution_time
import requests
from dotenv import load_dotenv
import configparser
import logging


class LocalServerLlm(OpenAI):
    """
    This class can be used to make the langchain API work with a local server hosted through
    the llama-cpp-python project.
    """

    def __init__(self):
        print(">> LocalServerLlm init")
        config = configparser.ConfigParser()
        config.read('config.ini')
        os.environ[
            "OPENAI_API_KEY"
        ] = "lm-studio"  # can be anything
        os.environ["OPENAI_API_BASE"] = f"http://localhost:{config.get('INFERENCE', 'LOCAL_WEB_SERVER_PORT')}/v1"
        os.environ["OPENAI_API_HOST"] = f"http://localhost:{config.get('INFERENCE', 'LOCAL_WEB_SERVER_PORT')}"
        warnings.filterwarnings("ignore")
        super().__init__()

class HuggingFaceLlm:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.MODEL_MAX_OUTPUT_TOKENS = self.config.getint('INFERENCE', 'MODEL_MAX_OUTPUT_TOKENS')
        self.API_URL = self.config.get('INFERENCE', 'HUGGINGFACE_INFERENCE_URL')

        load_dotenv()
        self.headers = {"Authorization": f"Bearer **************************************"}
    def query(self, payload):
        response = requests.post(self.API_URL, headers=self.headers, json=payload).json()

        return response
    @measure_execution_time(">> LLM query")
    def __call__(self, message):
        result = self.query({
            "inputs": message,
            "parameters": {
                "max_new_tokens": self.MODEL_MAX_OUTPUT_TOKENS,
                "return_full_text": True,
                "temperature": 0.5,
                "max_time": 100,
            },
            "options": {
                "use_cache": False,
                "wait_for_model": True,
            }
        })
        if result:
            logging.info(f"LLM response: {result}")
            return result[0]["generated_text"]

class TogetherLlm:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.MODEL_MAX_OUTPUT_TOKENS = self.config.getint('INFERENCE', 'MODEL_MAX_OUTPUT_TOKENS')
        self.url = self.config.get('INFERENCE', 'TOGETHER_INFERENCE_URL')
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": "Bearer ********************************"
        }
    def query(self, payload):
        response = requests.post(self.url, headers=self.headers, json=payload).json()
        print(response)
        return response
    @measure_execution_time(">> LLM query")
    def __call__(self, prompt):
        result = self.query(
            payload={
                "model": "codellama/CodeLlama-7b-Instruct-hf",
                "prompt": "<s>[INST]" + prompt + "[/INST]",
                "max_tokens": 512,
                "stop": ["</s>", "[/INST]"],
                "temperature": 0.4,
                "top_p": 0.7,
                "top_k": 50,
                "repetition_penalty": 1,
                "n": 1
            }
        )
        if result:
            return result
