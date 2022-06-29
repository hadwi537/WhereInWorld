First Time setup:
run (from project root):

"conda env create -f whereInWorld_env.yaml"

start conda environement:

"conda activate whereInWorld" 

then to run scripts use:

(From whereInWorld directory)
python core.py <  ../tests/input.txt 

To exit the program:
"Exit"

To export the environement: (It depends on the OS)

* Opt 1:
"conda env export --from-history > whereInWorld_env.yaml"

*Opt 2:
Everything (not recommended - will fail on other OS)
"conda env export > whereInWorld_env.yaml" 


To delete environment:

* first deativate env if its running:
"conda decativate"

* Then remove
"conda env remove -n whereInWorld