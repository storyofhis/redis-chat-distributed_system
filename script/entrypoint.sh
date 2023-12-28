sudo chmod -R a+rwx /home/jovyan
P=$(python3 /script/genpass.py)
jupyter-lab --no-browser --allow-root --ip=0.0.0.0 --NotebookApp.token='' --NotebookApp.password=$P  --NotebookApp.ip='0.0.0.0' --Notebook.autoreload=True --NotebookApp.notebook_dir=/home/jovyan/work --allow-root
