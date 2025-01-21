import json

from src.core.app_config import APP_ROOT


class Settings(object):
    # Get the app path
    json_file = "settings.json"
    settings_path = APP_ROOT / json_file
    if not settings_path.is_file():
        print(f"WARNING: \"settings.json\" not found! Check in the folder {settings_path}")

    # Initialize settings
    def __init__(self) -> None:
        super(Settings, self).__init__()

        # Settings dict
        self.items = {}

        # Deserialize
        self.deserialize()

    # Serialize JSON
    def serialize(self):
        # Write JSON file
        with open(self.settings_path, "w", encoding="utf-8") as write:
            json.dump(self.items, write, indent=4)

    # Deserialize JSON
    def deserialize(self):
        # Read JSON file
        with open(self.settings_path, "r", encoding="utf-8") as reader:
            settings = json.loads(reader.read())
            self.items = settings
