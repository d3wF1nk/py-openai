import datetime
import json
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

    @property
    def descriptor(self):
        return self._description

    @staticmethod
    def execute(parameters):
        date_info = {
            "date": datetime.datetime.now().strftime(parameters["format"]),
        }
        return json.dumps(date_info)
