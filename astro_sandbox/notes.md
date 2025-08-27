Set up environment:  
  
cd astro_sandbox  
conda create --name astro_sandbox python=3.9  
conda activate astro_sandbox  
pip install numpy matplotlib pandas scikit-learn astropy spicepy  
conda env export > environment.yml  
pip freeze > requirements.txt  

To recreate from environment.yml file:  
conda env create -f environment.yml  