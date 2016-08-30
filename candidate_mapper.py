from mpl_toolkits.basemap import Basemap
from os.path import isfile
import matplotlib.pyplot as plt
import numpy as np
import pickle
import json


def main():

    while True:

        number_of_candidates = raw_input("How many candidates to map (0/1/2): ")

        if number_of_candidates not in ["0", "1", "2"]:
            print number_of_candidates + " candidate(s) is not a valid option. \n"

        elif number_of_candidates == "1":
            print "Available candidates are Bernie Sanders (1), Hillary Clinton (2), or Donald Trump (3). \n"
            selected_candidate = raw_input("Select candidate to map (1/2/3): ")

            if selected_candidate not in ["1", "2", "3"]:
                print "Invalid candidate selected. \n"

            else:
                generate_map(candidate1=selected_candidate, num=1)

        elif number_of_candidates == "2":
            print "Available candidates are Bernie Sanders (1), Hillary Clinton (2), or Donald Trump (3). \n"
            selected_candidate1 = raw_input("Select first candidate to map (1/2/3): ")
            selected_candidate2 = raw_input("Select second candidate to map(1/2/3): ")

            if selected_candidate1 not in ["1", "2", "3"] or selected_candidate2 not in ["1", "2", "3"]:
                print "Invalid candidate selected. \n"
            elif selected_candidate1 == selected_candidate2:
                print "Different candidates must be selected. \n"
            else:
                generate_map(candidate1=selected_candidate1, candidate2=selected_candidate2, num=2)

        elif number_of_candidates == "0":
            print "Quitting. \n"
            break


# Generates the necessary strings for input/output and map labeling
def generate_string_literals(candidate1, candidate2, num):
    if candidate1 is not None and num != 0:
        if num == 1:

            if candidate1 == "1":
                positive_filename = "Bernie_Positive_Coordinates.txt"
                negative_filename = "Bernie_Negative_Coordinates.txt"
                map_title = "Bernie Sanders Support on Twitter"
                figure_filename = "Sanders_Overall"

            elif candidate1 == "2":
                positive_filename = "Hillary_Positive_Coordinates.txt"
                negative_filename = "Hillary_Negative_Coordinates.txt"
                map_title = "Hillary Clinton Support on Twitter"
                figure_filename = "Clinton_Overall"

            elif candidate1 == "3":
                positive_filename = "Trump_Positive_Coordinates.txt"
                negative_filename = "Trump_Negative_Coordinates.txt"
                map_title = "Donald Trump Support on Twitter"
                figure_filename = "Trump_Overall"

            tick_labels = ["Negative", "Positive"]

        elif num == 2:
            if candidate1 in ["1", "2"] and candidate2 in ["1", "2"]:
                positive_filename = "Bernie_Positive_Coordinates.txt"
                negative_filename = "Hillary_Positive_Coordinates.txt"
                tick_labels = ["Clinton", "Sanders"]
                map_title = "Sanders vs Clinton Support on Twitter"
                figure_filename = "Sanders_Clinton_Overall"

            elif candidate1 in ["1", "3"] and candidate2 in ["1", "3"]:
                positive_filename = "Bernie_Positive_Coordinates.txt"
                negative_filename = "Trump_Positive_Coordinates.txt"
                tick_labels = ["Trump", "Sanders"]
                map_title = "Sanders vs Trump Support on Twitter"
                figure_filename = "Sanders_Trump_Overall"

            elif candidate1 in ["2", "3"] and candidate2 in ["2", "3"]:
                positive_filename = "Hillary_Positive_Coordinates.txt"
                negative_filename = "Trump_Positive_Coordinates.txt"
                tick_labels = ["Trump", "Clinton"]
                map_title = "Clinton vs Trump Support on Twitter"
                figure_filename = "Clinton_Trump_Overall"

    return positive_filename, negative_filename, map_title, figure_filename, tick_labels


# Generates a heatmap of candidate popularity using a hexbin, or loads a previously generated map
def generate_map(candidate1=None, candidate2=None, num=0):
    # bounding box for the lower 48 states
    west, south, east, north = -126.71, 24.31, -66.49, 49.93

    positive_filename, negative_filename, map_title, figure_filename, tick_labels = generate_string_literals(candidate1, candidate2, num)

    # check if the figure has already been pickled, if so then load it
    print "Checking for previously generated map...\n"

    if isfile(figure_filename + ".pkl"):
        print "Previously generated map available. Loading...\n"
        with open(figure_filename + ".pkl", "rb") as pickled_figure:
            fig = pickle.load(pickled_figure)
            plt.show()

    else:
        print "Previously generated map is not available. Generating new map...\n"
        with open(positive_filename, "r") as positive_input:
            positive_longitude = []
            positive_latitude = []

            for line in positive_input.readlines():
                try:
                    tweet = json.loads(line)
                except ValueError as e:
                    print "The following error has occurred: " + e.message

                if type(tweet["coordinates"]) is dict:
                    coordinates = tweet["coordinates"]["coordinates"]
                else:
                    coordinates = tweet["coordinates"]

                if coordinates is not None and west <= coordinates[0] <= east and south <= coordinates[1] <= north:
                    positive_longitude.append(coordinates[0])
                    positive_latitude.append(coordinates[1])

        with open(negative_filename, "r") as negative_input:
            negative_longitude = []
            negative_latitude = []

            for line in negative_input.readlines():
                try:
                    tweet = json.loads(line)
                except ValueError as e:
                    print "The following error has occurred: " + e.message

                # tweets geocoded by Twitter and tweets geocoded by us are structured slightly different
                if type(tweet["coordinates"]) is dict:
                    coordinates = tweet["coordinates"]["coordinates"]
                else:
                    coordinates = tweet["coordinates"]

                if coordinates is not None and west <= coordinates[0] <= east and south <= coordinates[1] <= north:
                    negative_longitude.append(coordinates[0])
                    negative_latitude.append(coordinates[1])

        plt.style.use("ggplot")

        # change DPI if resolution is unsuitable for your screen
        fig = plt.figure(dpi=300)
        ax = fig.add_subplot(111)

        map = Basemap(projection='merc', llcrnrlat=south, urcrnrlat=north,
                    llcrnrlon=west, urcrnrlon=east, resolution='h')

        map.drawcoastlines()
        map.drawstates()
        map.drawmapboundary(fill_color="aqua")
        map.fillcontinents(color='#D0F5A9', lake_color='aqua', zorder=0)

        # cut length of all four lists to length of smallest to equalize dataset
        if len(negative_longitude) > len(positive_longitude):
            negative_longitude = negative_longitude[0:len(positive_longitude)]
            negative_latitude = negative_latitude[0:len(positive_longitude)]
        elif len(negative_longitude) < len(positive_longitude):
            positive_longitude = positive_longitude[0:len(negative_longitude)]
            positive_latitude = positive_latitude[0:len(negative_longitude)]

        # the c array contains the values to be accumulated in each hexbin, which will then be summed
        c_positive = [1] * len(positive_longitude)
        c_negative = [-1] * len(negative_longitude)

        c_total = c_positive + c_negative
        long_total = positive_longitude + negative_longitude
        lat_total = positive_latitude + negative_latitude

        x, y = map(long_total, lat_total)

        hexbin = map.hexbin(np.array(x), np.array(y), C=np.array(c_total), reduce_C_function=np.sum, gridsize=18,
                       cmap=plt.cm.coolwarm, vmin=-10, vmax=10)

        color_bar = map.colorbar()
        color_bar.set_ticks([-10, 10])
        color_bar.set_ticklabels(ticklabels=tick_labels)

        plt.title(map_title)
        pickle.dump(fig, open(figure_filename + ".pkl", "wb"))
        plt.savefig(figure_filename + ".png", dpi=300, bbox_inches="tight")
        plt.show()


if __name__ == "__main__":
    main()