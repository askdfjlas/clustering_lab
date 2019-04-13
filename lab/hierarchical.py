import sys
import k_means
from math import *

sys.path.append("..")

import clusters as utils

distance_function = utils.pearson
num_clusters = 7


def get_all(cluster, ids):  # Get all IDs in a cluster
    if cluster.id < 0:
        if cluster.left is not None:
            get_all(cluster.left, ids)
        if cluster.right is not None:
            get_all(cluster.right, ids)
    else:
        ids.append(cluster.id)


def main(input_f):
    (countries, vectors) = k_means.read_file(input_f)

    clusters = utils.hcluster(vectors, distance=distance_function)
    utils.drawdendrogram(clusters, list(map(lambda x: x[1], countries)), jpeg='data/hierarchical.jpg')

    # Self-picked clusters from the graph which I considered good
    good_clusters = [clusters.left, clusters.right.left, clusters.right.right.left.left,
                     clusters.right.right.left.right.left, clusters.right.right.left.right.right,
                     clusters.right.right.right.right, clusters.right.right.right.left]

    cluster_level = []

    for cluster in good_clusters:
        country_ids = []
        get_all(cluster, country_ids)
        cluster_level.append(country_ids)

    for i in range(num_clusters):
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in cluster_level[i]])

    print("SSE: " + str(k_means.sse(cluster_level, vectors)))


if __name__ == "__main__":
    main("data/preprocessed.csv")