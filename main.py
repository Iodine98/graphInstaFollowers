import os
from typing import Dict, List

from pathlib import Path

import json
from dash_graph import Graph, app
from client import Client


def initialize_user_followers() -> Dict[str, List[str]]:
    try:
        with open(file_path, 'r') as f_file:
            return json.loads(f_file.read())
    except FileNotFoundError:
        with open(file_path, 'x') as _:
            pass
        with open(file_path, 'r') as f_file:
            return json.loads(f_file.read())


# Create a Instaclient object. Place as driver_path argument the path that leads to where you
# saved the chromedriver.exe file
file_path = Path.cwd() / 'followers.json'
# USR_NAME: str = os.getenv('USERNAME', input("Please enter your user name: "))
# with Client(USR_NAME, file_path) as client:
#     client.scrape(0, 51, 30)
user_followers: Dict[str, List[str]] = initialize_user_followers()
graph_instance = Graph(user_followers)
graph_instance.render_layout(debug=True)
app.run_server()
