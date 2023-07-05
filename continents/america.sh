#!/bin/bash

countries=("argentina" "bolivia" "brazil" "canada" "chile" "colombia" "costa rica" "cuba" "dominican republic" "ecuador" "el salvador" "guatemala" "haiti" "honduras" "jamaica" "mexico" "nicaragua" "panama" "paraguay" "peru" "puerto rico" "suriname" "united states" "uruguay" "venezuela")

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
