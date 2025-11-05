Set up environment: 

conda create --name ml_sandbox python=3.11  -y
conda activate ml_sandbox  
pip install numpy pandas matplotlib scikit-learn seaborn  
conda env export > environment.yml  
pip freeze > requirements.txt  

To recreate from environment.yml file:  
conda env create -f environment.yml  