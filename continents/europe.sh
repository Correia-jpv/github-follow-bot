#!/bin/bash

countries=("albania" "andorra" "austria" "belarus" "belgium" "bosnia and herzegovina" "bulgaria" "croatia" "cyprus" "czech republic" "denmark" "estonia" "finland" "france" "germany" "greece" "hungary" "iceland" "ireland" "italy" "kosovo" "latvia" "liechtenstein" "lithuania" "luxembourg" "malta" "moldova" "monaco" "montenegro" "netherlands" "north macedonia" "norway" "poland" "portugal" "romania" "russia" "san marino" "serbia" "slovakia" "slovenia" "spain" "sweden" "switzerland" "ukraine" "united kingdom" "vatican city")

num_shells=${#countries[@]}  # Set the number of shells to the total number of countries
command_count=3  # Specify the number of times the bot_follow.py command should be executed

# Loop to run Python script with different countries
for ((i=0; i<$num_shells; i++))
do
    country="${countries[$i]}"
    for ((j=1; j<=$command_count; j++))
    do
        python bot_follow.py -p "$country" -m 4000 -smax 20 
    done
done
