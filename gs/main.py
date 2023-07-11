import time
from UI import UI
import json

def main():
    # tk
    with open('./config.json') as ui_config_file:
        ui_config = json.load(ui_config_file)
    
    UI().start(ui_config["tk_config"])

if __name__ == "__main__":
    main()

