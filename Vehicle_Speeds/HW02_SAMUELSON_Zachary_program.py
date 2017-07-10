import matplotlib.pyplot as plt
import numpy as np
import csv
import math
"""
Otsu's Method
Zachary Samuelson
2/2017

This program will use Otsu's method to separate
vehicle speeds into clusters
"""

def main():
    #list of speeds
    speed_list = []
    speeds = []
    #convert the csv file to our list
    with open('CLASSIFIED_TRAINING_SET_FOR_RECKLESS_DRIVERS.csv', 'r') as f:
        reader = csv.reader(f)
        speed_list = list(reader)

    #convert the list we get back into a list of float nums
    for array in speed_list:
        for speed in array:
            intSpeed = float(speed)
            speeds.append(intSpeed)

    #the bins for the histogram
    bins = [40.0, 42.0, 44.0, 46.0, 48.0, 50.0, 52.0, 54.0, 56.0, 58.0, 60.0,
            62.0, 64.0, 66.0, 68.0, 70.0, 72.0, 74.0, 76.0, 78.0, 80.0]
    #plot the histogram
    plt.hist(speeds, bins)
    plt.title("Number of Cars at Various Speeds")
    plt.xlabel("Speeds (mph)")
    plt.ylabel("Number of Cars")
    plt.show()

    #sort our list of speeds
    speeds.sort()

    #declare variables to max value
    best_mixed_variance = math.inf
    best_threshold = math.inf
    main_index = 0

    #array for graphing our variances against speeds
    mixed_variance_array = []

    """
    use Otsu's method to find the best threshold at
    which to cluster our data
    """
    for threshold in speeds:
        wt_under = (main_index+1.0)/(len(speeds))
        wt_over = (len(speeds) - (main_index + 1.0)) / len(speeds)
        if main_index == (len(speeds)-1):
            var_under = (np.std(speeds[0:main_index+1])) ** 2
            var_over = (np.std(speeds[main_index:(len(speeds))])) ** 2
        else:
            var_under = (np.std(speeds[0:main_index+1]))**2
            var_over = (np.std(speeds[main_index + 1:(len(speeds))])) ** 2

        mixed_variance = (wt_under*var_under) + (wt_over*var_over)
        mixed_variance_array.append(mixed_variance)

        #if the current variance is less than our current best
        #set best to current
        if mixed_variance < best_mixed_variance:
            best_mixed_variance = mixed_variance
            best_threshold = threshold
        main_index += 1

    print("Best Threshold: " + str(best_threshold) + " mph")
    print("Best Mixed Variance: " + str(best_mixed_variance))

    #graph variances against speeds
    plt.plot(speeds, mixed_variance_array)
    plt.xlabel("Speed Used for Threshold(mph)")
    plt.ylabel("Mixed Variances")
    plt.title("Mixed Variances for Different Thresholds")
    plt.show()





main()