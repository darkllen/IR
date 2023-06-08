from base.base import BaseSerializer
import json

class JsonSerializer(BaseSerializer):
    
    def serialize(self, obj, file_path: str) -> None:
        with open(file_path, 'w') as f:
            json.dump(obj, f, sort_keys=True)


    def deserealize(self, file_path: str):
        with open(file_path, 'r') as f:
            return json.load(f)
