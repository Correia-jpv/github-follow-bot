#!/bin/bash

countries=("algeria" "angola" "benin" "botswana" "burkina faso" "burundi" "cape verde" "central african republic" "chad" "comoros" "democratic republic of the congo" "republic of the congo" "djibouti" "egypt" "equatorial guinea" "eritrea" "eswatini" "ethiopia" "gabon" "gambia" "ghana" "guinea" "guinea-bissau" "ivory coast" "kenya" "lesotho" "liberia" "libya" "madagascar" "malawi" "mali" "mauritania" "mauritius" "morocco" "mozambique" "namibia" "niger" "nigeria" "rwanda" "são tomé and príncipe" "senegal" "seychelles" "sierra leone" "somalia" "south africa" "south sudan" "sudan" "tanzania" "togo" "tunisia" "uganda" "zambia" "zimbabwe")

num_shells=20  # Specify the number of shells you want to create
command_count=20  # Specify the number of times the bot_follow.py command should be executed

# Loop to run Python script with different countries
for ((i=1; i<=$num_shells; i++))
do
    for country in "${countries[@]}"
    do
        for ((j=1; j<=$command_count; j++))
        do
            python bot_follow.py -p "$country" -m 4000 -smax 20
        done
    done
done
