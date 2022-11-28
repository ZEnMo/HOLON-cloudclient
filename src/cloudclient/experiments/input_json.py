import json


class InputJSON:
    def __init__(self, name, path, sheet_name, file_name):
        self.write_to_path = path / f"{name}_{sheet_name}.txt"

    def as_json(self, write_result=True):
        if write_result:
            self._write()
        return json.loads(self.data)

    def _write(self, formatted: bool = True):
        with open(self.write_to_path, "w") as outfile:
            if formatted:
                outfile.write(json.dumps(json.loads(self.data), indent=2))
            else:
                outfile.writelines([self.data])
