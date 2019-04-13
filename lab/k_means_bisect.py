import sys
import k_means
sys.path.append("..")

import clusters as utils

distance_function = utils.pearson
num_clusters = 7


def kcluster_bisect(clusters, vectors, distance=utils.euclidean, k=4):
    if len(clusters) == k:
        return clusters

    max_sse = None
    cluster_index = None
    for i in range(len(clusters)):  # Compute cluster with highest SSE
        cluster = clusters[i]
        score = 0

        centroid = k_means.get_centroid(cluster, vectors)

        for country in cluster:
            score += pow(distance(vectors[country], centroid), 2)

        if max_sse is None or score > max_sse:
            max_sse = score
            cluster_index = i

    original_indexes = []  # Save actual indexes of the chosen cluster relative to the original vectors
    for index in clusters[cluster_index]:
        original_indexes.append(index)

    new_clusters = utils.kcluster([vectors[index] for index in clusters.pop(cluster_index)], distance=distance, k=2)
    for cluster in new_clusters:
        for i in range(len(cluster)):
            cluster[i] = original_indexes[cluster[i]]  # Convert back to original vector indexes

    return kcluster_bisect(clusters + new_clusters, vectors, distance=distance, k=k)


def main(input_f, output_f):
    (countries, vectors) = k_means.read_file(input_f)

    clusters = kcluster_bisect([list(range(len(vectors)))], vectors, distance=distance_function, k=num_clusters)
    proper_clusters = []  # Nonempty clusters
    for i in range(num_clusters):
        if len(clusters[i]) == 0:
            continue

        proper_clusters.append(clusters[i])
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in clusters[i]])

    print("SSE: " + str(k_means.sse(proper_clusters, vectors)))


if __name__ == "__main__":
    main("data/preprocessed.csv", "")