import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime


# Searching for the lines we want and adding them to the textfile.
def table_to_txt(file, output):
    for line in file:
        words = line.split()
        if "Gal.Center" in words and "XRT" in words:
            output.write(line.split("Gal.Center")[1])

        elif "GALACTICCENTER" in words and "XRT" in words:
            output.write(line.split("GALACTICCENTER")[1])

    output.close()

# Get the needed information.
def get_info(stripped_file, dictionary):

    # Get OBSID, date and exposure time
    for line in stripped_file:

        items = line.split()
        obsid = str(items[0])
        date = str(items[7])
        exptime = float(items[10])

        # Add these to the dictionary
        dictionary[obsid] = [obsid, date, exptime]

    return dictionary

# Get the counts from the other textfile
def get_counts(counts_file):

    dictionary = {}

    # Get the OBSID and counts
    for line in counts_file:

        items = line.split()

        if "Doing" in items:
            OBSID = str(items[2].split("/")[6])
            dictionary[OBSID] = None

        if "100%" not in items and "Doing" not in items and "Total" not in items:
            counts = items[0]
            dictionary[OBSID] = int(counts)
    
    return dictionary

# Subtracts the two dictionaries, puts 0 if negative
def subtract_background(counts, background):
    total = {}

    for key in counts.keys():
        difference = counts[key] - (background[key] / 3)
        if difference < 0:
            total[key] = 0

        else:
            total[key] = difference

    return total

# Combines the information of the two dictionaries.
def combine(counts_dict, id_dict, total_dict):

    for item in counts_dict:
        if item in id_dict:
            total_dict[item] = id_dict[item] + [counts_dict[item]]

    return total_dict

# Checks what needs to be done for the plot and puts that info into a dataframe.
def reduction(item, index, counts_dict, id_dict):
   
    if index == "data":
        total_dict = counts_dict

    elif index == "reduced":
        background_file = open("Data/b" + item + ".txt", 'r')
        background_dict = get_counts(background_file)
        total_dict = subtract_background(counts_dict, background_dict)

    elif index == "background":
        background_file = open("Data/b" + item + ".txt", 'r')
        background_dict = get_counts(background_file)
        total_dict = background_dict

    # Combines the two dictionaries and uses Pandas to do further analysis.
    combined_dict = combine(total_dict, id_dict, {})
    dataframe = pd.DataFrame.from_dict(combined_dict, orient='index', columns=["OBSID","Date","Exptime","Counts"])
    dataframe["Countrate"] = dataframe["Counts"] / dataframe["Exptime"]
    
    if index != "data":
        dataframe["Background"] = list(background_dict.values())
        dataframe["Countrate background"] = dataframe["Background"] / dataframe["Exptime"]

    return dataframe

# Calculates the days since the first day and returns the list.
def days_since(dataframe):

    first_day = datetime.strptime(dataframe['Date'][0], "%Y-%m-%d")
    list = []

    for index in range(len(dataframe['Date'])):
        
        current_day = datetime.strptime(dataframe['Date'][index], "%Y-%m-%d")
        list.append((current_day - first_day).days)

    return list

# Make a plot of the wanted information
def plot(todo, lijst, id_dict):
    
    for item in lijst:

        # Read the counts file and extract it's information.
        counts_file = open("Data/d" + item + ".txt", 'r')
        counts_dict = get_counts(counts_file)

        options = {"data":["data"], "reduced":["reduced"], "both":["data", "background"], "background":["background"]}

        # Does the data-reduction requested.
        for index in options[todo]:
            
            # Puts the counts into the dataframe.
            dataframe = reduction(item, index, counts_dict, id_dict)

            # Calculates the amount of days since first day
            dataframe["Days since"] = days_since(dataframe)
            print(dataframe.to_string())

            # Plot the dataframe
            dates = dataframe["Days since"].to_list()
            values = dataframe["Countrate"].to_list()
            plt.plot(dates, values, label = "Name of object")
    
    plt.xlabel('Days (since first observation of the year)', fontsize=15)
    plt.ylabel(r'Intensity (counts sec$^{-1}$)', fontsize=15)
    plt.xlim(0,)
    plt.ylim(0,)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.minorticks_on()
    plt.grid()
    plt.legend(loc='upper right', fontsize=12)
    plt.tight_layout()
    plt.savefig("Figure.png", dpi=500)
    plt.show()

# Main function that gets executed and calls all other functions.
def main(todo, lijst):

    # Reading in the file
    file = open("observations.txt", "r")
    output = open("stripped_observations.txt", "w")

    # Read the input file and adds the correct lines to output.txt.
    table_to_txt(file, output)

    # Get the important information and put it in a dictionary.
    stripped_file = open("stripped_observations.txt", "r")
    id_dict = get_info(stripped_file, dict())

    # Plots the information
    plot(todo, lijst, id_dict)

main("reduced", ['290347-2006'])