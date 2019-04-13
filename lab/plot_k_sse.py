# Code to plot k vs SSE
import sys
import k_means
import matplotlib.pyplot as plt
import numpy as np
sys.path.append("..")

import clusters as utils

range_clusters = range(1, 50)  # Range of k to test


def main(input_f):
    (countries, vectors) = k_means.read_file(input_f)
    k_arr = []
    sse_arr = []

    for num in range_clusters:
        clusters = utils.kcluster(vectors, distance=k_means.distance_function, k=num)
        proper_clusters = []

        print(str(round((float(num)/50)*100)) + "%")
        for i in range(num):
            if len(clusters[i]) != 0:
                proper_clusters.append(clusters[i])

        k_arr.append(num)
        sse_arr.append(k_means.sse(proper_clusters, vectors))

    plt.plot(k_arr, sse_arr)
    plt.ylabel("SSE")
    plt.xlabel("k")
    plt.xticks(np.arange(0, 50, 2))
    plt.show()


if __name__ == "__main__":
    main("data/preprocessed.csv")
