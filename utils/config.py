import json

class Config:
    def get_val(self, value):
        datapath = "config.json"
        with open(datapath) as json_file:
            json_dict = json.load(json_file)
        return json_dict[value]

