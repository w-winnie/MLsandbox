import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from collections import defaultdict
import matplotlib.patches as mpatches

# def visualize_graph(G, current_state, title=""):
#     color_map = ['green' if current_state[node] == 1 else 'red' for node in G.nodes]
#     nx.draw(G, node_color=color_map, with_labels=True)
#     plt.title(title)
#     plt.show()

def visualize_graph(G, node_attr, title=""):
    values = [node_attr[node] for node in G.nodes]
    unique_values = list(set(values))
    color_dict = {val: plt.cm.tab10(i) for i, val in enumerate(unique_values)}
    color_map = [color_dict[val] for val in values]
    legend_patches = [mpatches.Patch(color=color_dict[val], label=str(val)) for val in unique_values]
    plt.figure(figsize=(5, 5))
    nx.draw(G, node_color=color_map, with_labels=True)
    plt.title(title)
    plt.legend(handles=legend_patches, loc='best', fontsize='small')
    plt.show()


def plot_node_attribute_dist(nodes, attribute_name, title="Attribute Distribution"):
    values = [node[attribute_name] for node in nodes.values()]
    # print(f"Values for {attribute_name}: {values}")
    plt.figure(figsize=(5, 3))
    unique, counts = np.unique(values, return_counts=True)
    plt.bar(unique, counts, edgecolor='black', alpha=0.7)
    plt.xticks(rotation=45)
    plt.xlabel(attribute_name)
    plt.ylabel("Frequency")
    plt.title(title)
    plt.show()

def plot_node_attribute_grouped_dist(G, group_by, value_attr, title="Distribution", xlabel=None, ylabel=None, bins=10):
    groups = defaultdict(list)
    for node in G.nodes:
        group_value = G.nodes[node][group_by]
        value = G.nodes[node][value_attr]
        groups[group_value].append(value)

    plt.figure(figsize=(6, 3))
    for label, values in groups.items():
        plt.hist(values, bins=bins, alpha=0.6, label=f"{group_by}: {label}", edgecolor='black')
    
    plt.xlabel(xlabel or value_attr)
    plt.ylabel(ylabel or "Frequency")
    plt.title(title)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def plot_node_scatter(G, x_attr, y_attr, color_attr='current_action', 
                      title="Scatter Plot", xlabel=None, ylabel=None):
    x = [G.nodes[node][x_attr] for node in G.nodes]
    y = [G.nodes[node][y_attr] for node in G.nodes]
    colors = [G.nodes[node][color_attr] for node in G.nodes]

    plt.figure(figsize=(5, 3))
    scatter = plt.scatter(x, y, c=colors, cmap='coolwarm', alpha=0.8)
    plt.xlabel(xlabel or x_attr)
    plt.ylabel(ylabel or y_attr)
    plt.title(title)
    plt.colorbar(scatter, label=color_attr)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

