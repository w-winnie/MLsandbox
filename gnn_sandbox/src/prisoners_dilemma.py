import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from strategies import *

def generate_social_network(num_nodes=20, k=4, p=0.3):
    G = nx.watts_strogatz_graph(n=num_nodes, k=k, p=p)
    return G

def initialize_actions(G, random_init=True): #all nodes randomly initialized
    for node in G.nodes:
        G.nodes[node]['current_action'] = np.random.choice([0, 1]) if random_init else 1

def initialize_agent_actions(G, config=None, random_init=True):
    strategy_types = list(STRATEGY_FUNCTIONS.keys())
    nodes = list(G.nodes)
    total_nodes = len(nodes)

    if config:
        strategy_counts = []
        assigned_nodes = 0
        for strategy in config:
            count = int(config[strategy] * total_nodes)
            strategy_counts.append((strategy, count))
            assigned_nodes += count
        remaining_nodes = total_nodes - assigned_nodes
        # If there are remaining nodes, assign them randomly
        remaining_strategies = np.random.choice(strategy_types, size=remaining_nodes)

        strategy_assignment = []
        for strategy, count in strategy_counts:
            strategy_assignment.extend([strategy] * count)
        strategy_assignment.extend(remaining_strategies)
        
        # Shuffle the assignments
        strategy_assignment = np.array(strategy_assignment)
        np.random.shuffle(strategy_assignment)
    else:
        # Assign all nodes randomly
        strategy_assignment = np.random.choice(strategy_types, size=total_nodes)

    # Assign strategies and initialize other attributes
    for node, strategy in zip(nodes, strategy_assignment):
        G.nodes[node]['strategy_type'] = strategy
        G.nodes[node]['current_action'] = np.random.choice([0, 1]) if random_init else 1
        G.nodes[node]['memory'] = {}
        G.nodes[node]['triggered'] = False
        G.nodes[node]['payoff'] = 0
        G.nodes[node]['prev_payoff'] = 0

payoff_matrix = {
    (1, 1): (3, 3),  # Both cooperate
    (1, 0): (0, 2),  # Cooperator gets 0, defector gets 2
    (0, 1): (2, 0),  # Defector gets 2, cooperator gets 0
    (0, 0): (0, 0)   # Both defect
}

def play_pd_round(G):
    payoffs = {node: 0 for node in G.nodes}
    for node in G.nodes:
        for neighbor in G.neighbors(node):
            s1 = G.nodes[node]['current_action']
            s2 = G.nodes[neighbor]['current_action']
            p1, p2 = payoff_matrix[(s1, s2)]
            payoffs[node] += p1
        G.nodes[node]['payoff'] = payoffs[node]

def update_actions(G):
    for node in G.nodes:
        payoffs = {n: G.nodes[n]['payoff'] for n in G.neighbors(node)}
        neighbor_payoffs = {neighbor: payoffs[neighbor] for neighbor in G.neighbors(node)}
        if neighbor_payoffs:
            best_neighbor = max(neighbor_payoffs, key=neighbor_payoffs.get)
            G.nodes[node]['current_action'] = G.nodes[best_neighbor]['current_action']

def update_agent_actions(G):        
    payoffs = {n: G.nodes[n]['payoff'] for n in G.neighbors(node)}     
    for node in G.nodes:
        strategy_type = G.nodes[node]['strategy_type']
        strategy_func = STRATEGY_FUNCTIONS[strategy_type]
        neighbors = list(G.neighbors(node))
        next_action = strategy_func(node, G, neighbors)
        G.nodes[node]['current_action'] = next_action
        G.nodes[node]['prev_payoff'] = payoffs[node]
        for neighbor in neighbors:
            G.nodes[node]['memory'][neighbor] = G.nodes[neighbor]['current_action']


if __name__ == "__main__":
    G = generate_social_network()
    strategies = initialize_actions(G)
    
    payoffs = play_pd_round(G, strategies)
    print("Payoffs:", payoffs)
    
    strategies = update_actions(G, strategies, payoffs)

# def initialize_agent_actions(G, config=None, random_init=True):
#     for node in G.nodes:
#         G.nodes[node]['strategy_type'] = config['strategy_type'] if config and 'strategy_type' in config else np.random.choice(list(STRATEGY_FUNCTIONS.keys()))
#         G.nodes[node]['current_action'] = np.random.choice([0, 1]) if random_init else 1
#         G.nodes[node]['memory'] = {}
#         G.nodes[node]['triggered'] = False
#         G.nodes[node]['payoff'] = 0
#         G.nodes[node]['prev_payoff'] = 0

# def initialize_strategies(G): #all agents randomly initialized
#     strategies = {node: np.random.choice([0, 1]) for node in G.nodes}
#     return strategies
#
# def play_pd_round(G, strategies):
#     payoffs = {node: 0 for node in G.nodes}
#     for node in G.nodes:
#         for neighbor in G.neighbors(node):
#             s1 = strategies[node]
#             s2 = strategies[neighbor]
#             p1, p2 = payoff_matrix[(s1, s2)]
#             payoffs[node] += p1  
#     return payoffs

# # All actors are initialized with the same strategy (mimic)
# def update_strategies(G, strategies, payoffs):
#     new_strategies = {}
#     for node in G.nodes:
#         neighbor_payoffs = {neighbor: payoffs[neighbor] for neighbor in G.neighbors(node)}
#         if neighbor_payoffs:  
#             best_neighbor = max(neighbor_payoffs, key=neighbor_payoffs.get)
#             new_strategies[node] = strategies[best_neighbor]  # Copy best neighbor
#         else:
#             new_strategies[node] = strategies[node]  # No change if isolated
#     return new_strategies

# def initialize_agent_strategies(G):
#     agents = {}
#     for node in G.nodes:
#         agents[node] = {
#             'strategy_type': np.random.choice(list(STRATEGY_FUNCTIONS.keys())),
#             'current_action': np.random.choice([0, 1]),
#             'memory': {},  # For tracking neighbor history
#             'triggered': False,  # For Grim Trigger
#             'prev_payoff': 0  # For Pavlov
#         }
#     return agents

# def update_actions(G, agents, payoffs):
#     for node in G.nodes:
#         strategy_type = agents[node]['strategy_type']
#         strategy_func = STRATEGY_FUNCTIONS[strategy_type]
#         neighbors = list(G.neighbors(node))
        
#         # Compute next action using the appropriate strategy
#         next_action = strategy_func(node, agents, neighbors)
#         agents[node]['current_action'] = next_action
        
#         # Update agent's payoff memory
#         agents[node]['prev_payoff'] = payoffs[node]
        
#         # Update memory of neighbor actions
#         for neighbor in neighbors:
#             agents[node]['memory'][neighbor] = agents[neighbor]['current_action']
