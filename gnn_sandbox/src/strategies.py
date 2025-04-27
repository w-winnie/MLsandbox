import numpy as np

# Strategy: Always Cooperate
# This strategy always cooperates, regardless of the actions of others.
def always_cooperate(node, G, neighbors):
    return 1

# Strategy: Always Defect
# This strategy always defects, regardless of the actions of others.
def always_defect(node, G, neighbors):
    return 0

# Strategy: Tit-for-Tat (TFT)
# This strategy cooperates until neighbor defected in the last round
def tit_for_tat(node, G, neighbors):
    if not neighbors:
        return 1
    # Mirror last move of first neighbor
    return G.nodes[node]['memory'].get(neighbors[0], 1)

# Strategy: Tit-for-Two-Tats (TFTT)
# This strategy cooperates until neighbor defected in the last two rounds
def tit_for_two_tats(node, G, neighbors):
    if not neighbors:
        return 1
    recent_defects = sum(G.nodes[node]['memory'].get(neigh, 1) == 0 for neigh in neighbors)
    return 0 if recent_defects >= 2 else 1

# Strategy: Grim Trigger
def grim_trigger(node, G, neighbors):
    if G.nodes[node]['triggered']:
        return 0
    if any(G.nodes[node]['memory'].get(neigh, 1) == 0 for neigh in neighbors):
        G.nodes[node]['triggered'] = True
        return 0
    return 1

# Strategy: Pavlov (Win-Stay, Lose-Shift)
def pavlov(node, G, neighbors):
    if G.nodes[node]['prev_payoff'] >= 3:
        return G.nodes[node]['current_action']  # Stay
    else:
        return 1 - G.nodes[node]['current_action']  # Switch

# Strategy: Prober
def prober(node, G, neighbors):
    if np.random.rand() < 0.1:  # 10% chance to defect
        return 0
    return G.nodes[node]['memory'].get(neighbors[0], 1) if neighbors else 1

# Strategy: Generous Tit-for-Tat (GTFT)
def generous_tft(node, G, neighbors):
    if not neighbors:
        return 1
    if np.random.rand() > 0.3:  # 70% chance to copy neighbor's last move
        return G.nodes[node]['memory'].get(neighbors[0], 1)
    return 1  # Forgive

# Strategy: Random
def random_strategy(node, G, neighbors):
    return np.random.choice([0, 1])

# Strategy: Zero-Determinant Extortionate (ZD Extortion)
def zd_extortion(node, G, neighbors):
    if not neighbors:
        return 1
    last_action = G.nodes[node]['memory'].get(neighbors[0], 1)
    if last_action == 1 and G.nodes[node]['prev_payoff'] >= 3:
        return 1
    return 0

# Startegy: imitator
def imitator(node, G, neighbors):
    if not neighbors:
        return G.nodes[node]['current_action']
    neighbor_payoffs = {neighbor: G.nodes[neighbor]['prev_payoff'] for neighbor in neighbors}
    best_neighbor = max(neighbor_payoffs, key=neighbor_payoffs.get)
    return G.nodes[best_neighbor]['current_action']


# Mapping strategy names to functions
STRATEGY_FUNCTIONS = {
    'Always_C': always_cooperate,
    'Always_D': always_defect,
    'TFT': tit_for_tat,
    'TFTT': tit_for_two_tats,
    'Grim': grim_trigger,
    'Pavlov': pavlov,
    'Prober': prober,
    'GTFT': generous_tft,
    'Random': random_strategy,
    'ZD_Extortion': zd_extortion,
    'Imitator': imitator
}