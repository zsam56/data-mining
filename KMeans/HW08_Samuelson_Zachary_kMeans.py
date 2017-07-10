import math
import csv
import random
import copy
import matplotlib.pyplot as plt

"""
Zachary Samuelson
HW08: KMeans Clustering
"""

class Cluster:
    cluster_id = 0
    center_mass = []
    points = [] #a list of guest ids

    def __init__(self, id, com, p):
        self.cluster_id = id
        self.center_mass = com
        self.points = p

    def addPoint(self, p):
        self.points.append(p)

def main():
    # convert the csv file to our list
    with open('HW_08_KMEANS_DATA_v300.csv', 'r') as f:
        reader = csv.reader(f)
        data_list = list(reader)

    new_list = []
    for record in data_list:
        record = [float(i) for i in record]
        new_list.append(record)

    clusters_list = kmeans_helper(new_list)

    lowest_sse = 100000000000
    lowest_k = 0
    sse_list = []
    k_list = []
    k_five = []
    #compute the sum of squared errors
    for k_clusters in clusters_list:
        curr_sse = 0
        k_list.append(len(k_clusters))
        for cluster in k_clusters:
            for point in cluster.points:
                error = compute_euc_dist(point, cluster.center_mass)
                squared_error = error**2
                curr_sse += squared_error
        if (curr_sse < lowest_sse):
            lowest_sse = curr_sse
            lowest_k = len(k_clusters)
        sse_list.append(curr_sse)
        if (len(k_clusters) == 5):
            k_five = k_clusters
            print(curr_sse)

    k_five_com = []
    colors = ['r', 'g', 'b', 'y', 'm']
    index = 0
    for cluster in k_five:
        x_points = []
        y_points = []
        for points in cluster.points:
            del points[2]
            x_points.append(points[0])
            y_points.append(points[1])
        plt.scatter(x_points, y_points, c=colors[index])
        index += 1
    plt.show()



def compute_euc_dist(record1, record2):
    euc_dist = 0.0
    for num1, num2 in zip(record1, record2):
        euc_dist += (float(num1) - float(num2))**2

    return math.sqrt(euc_dist)

def compute_center_of_mass(records):
    index = 0
    columns = []
    com = []
    #make a copy of records
    new_records = copy.deepcopy(records)

    if (len(new_records) > 0):
        while (index < len(new_records[0])):
            column = [x[index] for x in new_records]
            columns.append(column)
            index += 1

    com_ind = 0
    for col in columns:
        num = (sum(col)) / (len(col))
        com.append(num)
        com_ind += 1

    return com

def kmeans_helper(data_list):
    clusters_list = []
    new_clust = []
    for k in range(1, 21):
        #choose k amount of random points
        clusters = []
        for j in range(1, k+1):
            index = int(random.uniform(0.0, float(len(data_list))))
            point = data_list[index]
            new_cluster = Cluster(j, point, [point])
            clusters.append(new_cluster)

        new_clust = kmeans(clusters, data_list)
        clusters_list.append(new_clust)
    return clusters_list


def kmeans(clusters, data_list):
    #reset all points to empty list
    for cluster in clusters:
        cluster.points = []

    # assign data points to a cluster
    for point in data_list:
        lowest_distance = 99999999
        low_cluster = None
        for cluster in clusters:
            distance_to_center = compute_euc_dist(point, cluster.center_mass)
            if (distance_to_center < lowest_distance):
                lowest_distance = distance_to_center
                low_cluster = cluster
        low_cluster.addPoint(point)

    # recompute centers
    done_clusts = 0
    for cluster in clusters:
        new_com = compute_center_of_mass(cluster.points)
        if (compute_euc_dist(new_com, cluster.center_mass) < .05):
            done_clusts += 1
        cluster.center_mass = new_com

    if (done_clusts == len(clusters)):
        return clusters

    return kmeans(clusters, data_list)

main()

