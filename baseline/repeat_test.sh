#!/bin/bash

arr=("mtsp51" "mtsp100" "mtsp150" "pr76" "pr152" "pr226")
# shellcheck disable=SC1073
for problem_name in ${arr[@]}
do
  for i in {1..30}
  do
    python main.py -r "./" -p $problem_name -o "baseline_run_data.json"
  done
done
