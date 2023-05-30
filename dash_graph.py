from typing import List, Dict, Set
from dash import Dash, html
import dash_cytoscape as cyto

# cyto.load_extra_layouts()
app = Dash(__name__)


class Graph:
    def __init__(self, user_followers, **kwargs):
        """
        :param kwargs: A Network instance from pyvis.Network
        :param usr_name: The current username passed in main.py
        :param user_followers: user_followers object
        :param first_degree_users: number of first degree users in graph (-1 means all of them)
       """
        self.user_followers: Dict[str, List[str]] = user_followers
        self.profiles: Set[str] = self.get_unique_profile_set()
        self.nodes = self.create_nodes()
        self.edges = self.create_edges()
        if 'cyto_settings' in kwargs:
            self.cyto_settings = kwargs['cyto_settings']
        else:
            self.cyto_settings = {
                'id': 'cytoscape-insta-graph',
                'style': {'width': '100%', 'height': '1040px'},
                'layout': {
                    'name': 'cose'
                }
            }

    def get_unique_profile_set(self) -> Set[str]:
        unique_profiles = set()
        for labels in self.user_followers.values():
            for label in labels:
                unique_profiles.add(label)
        return unique_profiles

    def create_nodes(self):
        return [
            {'data': {'id': label, 'label': label}, }
            for label in self.profiles
        ]

    def create_edges(self):
        return [
            {'data': {'source': source, 'target': target}}
            for source, targets in self.user_followers.items()
            for target in targets
        ]

    def render_layout(self, debug=False):
        if debug:
            print("nodes", self.nodes)
            print("edges", self.edges)
        app.layout = html.Div(
            [
                cyto.Cytoscape(elements=self.nodes + self.edges, **self.cyto_settings)
            ]
        )
