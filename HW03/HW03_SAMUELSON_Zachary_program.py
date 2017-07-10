import matplotlib.pyplot as plt
import numpy as np
import csv
import math
"""
HW03
Zachary Samuelson
2/2017

This program will find the threshold that produces the
lowest misclassification rate with regards to a list
of car speeds
"""

def main():
    #list of speeds
    speed_list = []
    speeds_clean = []
    #convert the csv file to our list
    with open('CLASSIFIED_TRAINING_SET_FOR_RECKLESS_DRIVERS.csv', 'r') as f:
        reader = csv.reader(f)
        speed_list = list(reader)

    #clean our list
    index = 1
    while (index < len(speed_list)):
        #strip whitespace
        speed_list[index][0].strip()
        speed_list[index][1].strip()
        #convert entries to floats/integers, round speeds to nearest half
        speed_list[index][0] = 0.5 * math.ceil(float(speed_list[index][0])*2.0)
        speed_list[index][1] = int(speed_list[index][1])

        speeds_clean.append(speed_list[index])

        index += 1

    #sort by speeds
    speeds_sorted = sorted(speeds_clean, key=lambda x: x[0])

    #find the speed threshold that produces the lowest misclassification rate
    best_misclass_rate = 999
    best_threshold = 0
    misclass_rate_array = []
    true_pos_array = []
    false_pos_array = []
    speeds = []
    main_index = 0
    for threshold in speeds_sorted:
        speeds.append(threshold[0])
        index_lower = main_index-1
        index_upper = main_index
        false_neg = 0
        false_pos = 0
        true_pos = 0

        """
        loop through speeds lower than
        threshold. if these speeds are reckless
        they'd be false negatives
        """
        while (index_lower > 0):
            if (speeds_sorted[index_lower][1]):
                false_neg += 1
            index_lower -= 1

        """
        loop through speeds greater than
        threshold. if these speeds are not
        reckless they'd be false positives
        """
        while (index_upper != len(speeds_sorted)):
            if (not speeds_sorted[index_upper][1]):
                false_pos += 1
            else:
                true_pos += 1 #record true positives for ROC curve
            index_upper += 1

        # add false positives and negatives for this threshold
        total_missed = false_pos + false_neg
        miss_rate = total_missed / (len(speeds_sorted) * 1.0)
        misclass_rate_array.append(miss_rate)
        # if new miss rate is lower, set best to the new one
        if (miss_rate <= best_misclass_rate):
            best_misclass_rate = miss_rate
            best_threshold = threshold[0]

        #record false/true positive rate for ROC curve
        false_pos_rate = false_pos/(len(speeds_sorted) * 1.0)
        true_pos_rate = true_pos/(len(speeds_sorted) * 1.0)
        false_pos_array.append(false_pos_rate)
        true_pos_array.append(true_pos_rate)

        if (threshold[0] == 58.0):
            print true_pos_rate

        main_index += 1

    print("Best Threshold: " + str(best_threshold) + "mph")
    print("Best Missclassification Rate: " + str(best_misclass_rate))

    # graph misclassification rate against speeds
    plt.plot(speeds, misclass_rate_array)
    plt.xlabel("Speed Used for Threshold(mph)")
    plt.ylabel("Misclassification Rate")
    plt.title("Misclassification Rate vs. Speeds Used for Thresholds")
    plt.show()

    # graph ROC curve
    plt.plot(false_pos_array, true_pos_array, marker='o')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve for Speed Thresholds")
    plt.show()





main();