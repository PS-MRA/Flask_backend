import csv
input_csv = "screen_condition.csv"
current_screen = "home"
with open(input_csv) as csvfile:
    reader = csv.DictReader(csvfile)
    core = []
    for row in reader:
        core.append(row)


for c in core:
    if c["Current_Screen"] == current_screen and c["Clickable_Condition"]=="TRUE" :
