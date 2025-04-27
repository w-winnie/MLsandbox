Set up environment: 

conda create --name gnn_prisoner python=3.9  
conda activate gnn_prisoner  
pip install networkx numpy matplotlib torch torch-geometric pandas scikit-learn  
conda env export > environment.yml  
pip freeze > requirements.txt  

To recreate from environment.yml file:  
conda env create -f environment.yml  


Notebooks: 

prisoner_dilemma.ipynb -  to understand the problem and generate data for training  
agent_behaviour_prediction.ipynb - to predict how agent behaves in the next round  
best_strategy_prediction.ipynb - to predict best strategy for agent for best rewards
network_evolution.ipynb - to predict how the network looks like over time
sandbox_social_networks.ipynb - to understand more and experiment the network we're using  


Some good resources to read more:  

prisoner's dilemma:  
https://youtu.be/mScpHTIi-kM?si=qoaPpNPs_Rb97Bap  
https://ablconnect.harvard.edu/prisoners-dilemma-game  
https://www.cs.cmu.edu/~./nilanjan/pubs/conference/socialcom10.pdf  
https://gsurma.medium.com/prison-escape-solving-prisoners-dilemma-with-machine-learning-c194600b0b71  

watts strogatz graph:  
https://www.kth.se/social/files/5605669af2765468be471eda/lecture%204%20%282015%29.pdf  
https://snap.stanford.edu/class/cs224w-readings/watts98smallworld.pdf  
