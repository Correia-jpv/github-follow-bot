#!/bin/bash

countries=("afghanistan" "armenia" "azerbaijan" "bahrain" "bangladesh" "bhutan" "brunei" "cambodia" "china" "cyprus" "georgia" "india" "indonesia" "iran" "iraq" "israel" "japan" "jordan" "kazakhstan" "kuwait" "kyrgyzstan" "laos" "lebanon" "malaysia" "maldives" "mongolia" "myanmar" "nepal" "north korea" "oman" "pakistan" "palestine" "philippines" "qatar" "russia" "saudi arabia" "singapore" "south korea" "sri lanka" "syria" "taiwan" "tajikistan" "thailand" "timor-leste" "turkey" "turkmenistan" "united arab emirates" "uzbekistan" "vietnam" "yemen")

num_shells=5  # Specify the number of shells you want to create
command_count=3  # Specify the number of times the bot_follow.py command should be executed

# Loop to run Python script with different countries
for ((i=1; i<=$num_shells; i++))
do
    for country in "${countries[@]}"
    do
        for ((j=1; j<=$command_count; j++))
        do
            python bot_follow.py -p "$country" -m 400 -smax 20 
        done
    done
done
