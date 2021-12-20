# The code of course project in Advanced Artificial Intelligence  

* This is the code of course project in Advanced Artificial Intelligence.This project uses ***NSGA-II*** to solve the problem of ***Multiple Traveling Salesmen Problem***.
* The baseline code is from https://github.com/Anupal/GA-for-mTSP ,we have do some adjust to make it more suitable for our experiment.
* The population select algorithm in our improve was mainly based on the NSGA-II:https://github.com/haris989/NSGA-II ;most of the code was based on the arifield's work:https://github.com/ariefield/MTSP-Genetic


## Contributors
>The names of contributors are not in particular order.

|**NAME**	|	**ID**	|**CONTRIBUTION**|
|-------|-------|---|
|<center>Lei Chenyang<center>|<center>12132336<center>|<center>1/3</center>|
|<center>Chen Yuxiang<center>|<center>12132330<center>|<center>1/3</center>|
|<center>Zhang Zhicheng<center>|<center>12132375<center>|<center>1/3</center>|


## Operating instructions
###Repeate our experiment result
 **Change** the dir to `baseline/code/`, and run the shell `repeat_test.sh`, 
 you will get the baseline result saved in the `baseline_run_data.json`<br/>
**Change** the dir ro `mtsp_nsga_ii/code/`, and run the python file `repeat_test.py`,
you will get the improved GA result saved in the `ours_run_data.json`<br/>
**Move** the two `.json` file you get in the previous step to `summary_figure/`.Run `polt_figure.py`and `summary.py` ,you will get the result figure and table of this two algorithm we represent in  our report.
> Note: It needs a lot of time to run the experiment, as we repeat 30 times in each dataset.
###2.Just run the improve GA algorithm
**Change** the dir ro `mtsp_nsga_ii/code/`
* If you just want to obtain the results of six data sets stored in **mtsp_nsga_ii/data**, you can run **mtsp_nsga_ii/code/repeat_test.py**.   
* If you add a new data set in **mtsp_nsga_ii/data**, please remember to add the the name of new data set to the parameter  **`problem_name_list`**, which can be found in **mtsp_nsga_ii/code/repeat_test.py**, and then run **mtsp_nsga_ii/code/repeat_test.py**.  
* If you want to modify **the number of traveling salesman**, **the number of populations**, **the number of trainings**, **mutation rate**, and **the number of program repetitions**, you can modify **`num_travellers`**, **`population_size`** , **`generations`**, **`mutation_rate`** and **`repeat_times`** separately. You can find them in **mtsp_nsga_ii/code/repeat_test.py**.

## File manifest  
─MTSP_NSGA_II-master
    │  README.md
    │
    ├─.idea
    │  │  .gitignore
    │  │  deployment.xml
    │  │  misc.xml
    │  │  modules.xml
    │  │  MTSP_NSGA_II.iml
    │  │  other.xml
    │  │  vcs.xml
    │  │  workspace.xml
    │  │
    │  └─inspectionProfiles
    │          profiles_settings.xml
    │          Project_Default.xml
    │
    ├─baseline
    │  │  dustbin.py
    │  │  galogic.py
    │  │  globals.py
    │  │  main.py
    │  │  nodenum.py
    │  │  population.py
    │  │  README.md
    │  │  repeat_test.sh
    │  │  route.py
    │  │  routemanager.py
    │  │
    │  └─data
    │          mtsp100.txt
    │          mtsp150.txt
    │          mtsp51.txt
    │          pr152.txt
    │          pr226.txt
    │          pr76.txt
    │
    ├─code
    │  └─__pycache__
    │          chromosome.cpython-36.pyc
    │          GA.cpython-36.pyc
    │          globalManager.cpython-36.pyc
    │          Node.cpython-36.pyc
    │          nodeManager.cpython-36.pyc
    │          Population.cpython-36.pyc
    │          test.cpython-36.pyc
    │          test2.cpython-36.pyc
    │
    ├─mtsp_nsga_ii
    │  ├─code
    │  │      chromosome.py
    │  │      ga.py
    │  │      node.py
    │  │      nodemanager.py
    │  │      nsga_ii.py
    │  │      repeat_test.py
    │  │
    │  └─data
    │          mtsp100.txt
    │          mtsp150.txt
    │          mtsp51.txt
    │          pr152.txt
    │          pr226.txt
    │          pr76.txt
    │
    └─summary_figure
            baseline_run_data.json
            ours_run_data.json
            plot_figure.py
            summary.py
            unite.svg  
                 
                   
   