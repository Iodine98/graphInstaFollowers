from typing import List, Dict

from pyvis.network import Network


class Graph:
    def __init__(self, usr_name, user_followers, first_degree_users: int = -1, **kwargs):
        """
        :param kwargs: A Network instance from pyvis.Network
        :param usr_name: The current username passed in main.py
        :param user_followers: user_followers object
        :param first_degree_users: number of first degree users in graph (-1 means all of them)
       """
        self.nodes: Dict[str, int] = {}
        self.reference = 0
        self.usr_name: str = usr_name
        self.user_followers: Dict[str, List[str]] = user_followers
        self.first_degree_users: int = first_degree_users
        self.followers_list = list(self.user_followers.keys())[0:self.first_degree_users]
        self.net = kwargs.get('network', Network(height='100%', width='100%', bgcolor='#222222', font_color='white'))
        self.net.barnes_hut(spring_length=90, spring_strength=0.01)

    def add_node(self, usr_name: str):
        self.net.add_node(self.reference, label=usr_name)
        self.nodes[usr_name] = self.reference
        self.reference += 1

    def add_first_degree_followers(self):
        for follower in self.followers_list:
            if follower == self.usr_name:
                continue
            self.add_node(follower)

    def add_second_degree_followers(self):
        for follower in self.followers_list:
            start = self.nodes[follower]
            for follower_of_follower in self.user_followers[follower]:
                if follower_of_follower in self.nodes:
                    end = self.nodes[follower_of_follower]
                else:
                    self.add_node(follower_of_follower)
                    end = self.nodes[follower_of_follower]
                self.net.add_edge(start, end)

    def render(self):
        self.add_node(self.usr_name)
        self.add_first_degree_followers()
        self.add_second_degree_followers()
        self.net.show('net.html')
