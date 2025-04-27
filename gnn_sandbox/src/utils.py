import os
import json

def analyze_strategy_performance(G):
    strategy_data = {}
    
    for node in G.nodes:
        strategy = G.nodes[node]['strategy_type']
        payoff = G.nodes[node]['payoff']
        
        if strategy not in strategy_data:
            strategy_data[strategy] = {
                'total_payoff': 0,
                'count': 0,
                'min_payoff': float('inf'),
                'max_payoff': float('-inf')
            }
        
        strategy_data[strategy]['total_payoff'] += payoff
        strategy_data[strategy]['count'] += 1
        strategy_data[strategy]['min_payoff'] = min(strategy_data[strategy]['min_payoff'], payoff)
        strategy_data[strategy]['max_payoff'] = max(strategy_data[strategy]['max_payoff'], payoff)
        
    strategy_summary = []
    for strategy, data in strategy_data.items():
        avg_payoff = data['total_payoff'] / data['count']
        strategy_summary.append({
            'strategy': strategy,
            'average_payoff': avg_payoff,
            'min_payoff': data['min_payoff'],
            'max_payoff': data['max_payoff'],
            'total_payoff': data['total_payoff'],
            'total_nodes': data['count']
        })
    
    strategy_summary.sort(key=lambda x: x['average_payoff'], reverse=True)
    
    print(f"{'Strategy':<15}{'Avg Payoff':<12}{'Min Payoff':<12}{'Max Payoff':<12}{'Total Payoff':<15}{'Node Count':<10}")
    for entry in strategy_summary:
        print(f"{entry['strategy']:<15}{entry['average_payoff']:<12.2f}{entry['min_payoff']:<12.2f}"
              f"{entry['max_payoff']:<12.2f}{entry['total_payoff']:<15.2f}{entry['total_nodes']:<10}")


def load_config(config_path="src/config.json"):
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('strategy_distribution', {})
    else:
        return None  # No config
