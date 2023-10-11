import datetime
import json
import subprocess
from abc import ABC, abstractmethod


class FunctionInterface(ABC):

    @abstractmethod
    def descriptor(self):
        pass

    @staticmethod
    @abstractmethod
    def execute(parameters):
        pass


class DatetimeFunction(FunctionInterface):

    def descriptor(self):
        return self._description

    @staticmethod
    def execute(parameters):
        return json.dumps({
            "date": datetime.datetime.now().strftime(parameters["format"]),
        })

    def __init__(self):
        self._description = {
            "name": "datetime_function",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["%d/%m/%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"]
                    },
                },
                "required": ["format"],
            }}


class SystemFunction(FunctionInterface):

    def descriptor(self):
        return self._description

    @staticmethod
    def execute(parameters):
        decoded_out = ""
        try:
            output = subprocess.check_output(parameters["cmd"], shell=True)
            decoded_out = output.decode("utf-8")
        except subprocess.CalledProcessError as e:
            decoded_out = e.output.decode("utf-8")
        finally:
            print(f'executed_cmd: {parameters["cmd"]} \noutput: {decoded_out}')
            return json.dumps({
                "output": decoded_out,
            })

    def __init__(self):
        self._description = {
            "name": "system_function",
            "description": "Execute a command on local-host and return output",
            "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "The cmd to execute, e.g. ls -lat | grep '.txt'",
                    }
                },
                "required": ["cmd"],
            }}
