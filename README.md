Each sandbox is different projects - set each sandbox as its own workspace while trying it out - might be easier  

You would need a .env file and a data folder in each workspace as well - i could create a dummy one and upload but i was lazy sorry!


## Project Structure

MLsandbox/
├── README.md
├── astro_sandbox/          # Astronomy experiments and models
│ ├── environment.yml       # Conda environment YAML
│ ├── requirements.txt      # pip requirements.txt
│ ├── notes.md              # setup instructions
│ ├── data/                 # Input data
│ │ ├── eclipse/                # subfolder project name
│ │ └── starspectra/            # subfolder project name
│ ├── data_output/          # Data output folder
│ │ ├── eclipse/                # subfolder project name
│ │ └── starspectra/            # subfolder project name
│ │ ├── logs/                       # project - logs
│ │ │ ├── 20251029-185145/
│ │ │ │ ├── train/
│ │ │ │ └── validation/
│ │ ├── models/                     # project models
│ │ │ ├── best_model.h5
│ │ │ ├── best_model.keras
│ │ │ └── 4.2.0
│ │ └── plots/                      # project plots
│ │ ├── spectrum_10000_57346_426.png
│ ├── notebooks/                    # notebooks
│ │ ├── eclipses.ipynb
│ │ ├── eclipses_visualize.ipynb
│ │ ├── sandbox.ipynb
│ │ └── starspectra_classifier.ipynb
│ ├── rough/                        # work in progress or other files gitignored
│ └── src/                          # .py code or scripts if any
│
├── gnn_sandbox/                    # Graph neural network simulations
│ ├── environment.yml
│ ├── requirements.txt
│ ├── notes.md
│ ├── data/
│ ├── notebooks/
│ │ ├── agent_behaviour_prediction.ipynb
│ │ ├── best_strategy_prediction.ipynb
│ │ ├── network_evolution.ipynb
│ │ ├── prisoner_dilemma.ipynb
│ │ └── sandbox_social_networks.ipynb
│ └── src/
│ ├── init.py
│ ├── config.json
│ ├── plotting_func.py
│ ├── prisoner_dilemma.py
│ ├── strategies.py
│ └── utils.py
│
├── llm_sandbox/                   # LLM experiments
│ ├── environment.yml
│ ├── requirements.txt
│ ├── notes.md
│ ├── data/
│ ├── notebooks/
| ├── AIvsAI.ipynb
| ├── embeddings_combination_alternative.ipynb
| ├── embeddings_vector_algebra.ipynb
| ├── embeddings_weighted_average.ipynb
| ├── github_brochure.ipynb
| ├── llm_connector_notebook.ipynb
| ├── rss_feed_and_summarizer.ipynb
| ├── summarizer_tool.ipynb
│ ├── rough/
│ └── src/
│
└── other_ml_sandbox/           # Miscellaneous ML experiments
├── notes.md
├── optimizers.ipynb
├── optimizers_basic.ipynb
├── data/
└── data_output/
└── logs/
