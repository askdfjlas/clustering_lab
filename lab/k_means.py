# Clustering with basic k-means
import sys
sys.path.append("..")

import clusters as utils

data_range = range(2, 8)  # Useful sub-indexes
num_clusters = 7
distance_function = utils.pearson


def read_file(input_f):
    countries = []
    vectors = []

    data = open(input_f)

    for line in data:
        arr = line.rstrip().split(',')

        countries.append((arr[0], arr[1]))
        vectors.append([int(arr[i]) for i in data_range])

    data.close()
    return countries, vectors


def get_centroid(cluster, vectors):
    centroid = [0 for i in range(len(vectors[0]))]

    for index in cluster:
        for i in range(len(vectors[0])):
            centroid[i] += vectors[index][i]  # Store sums

    centroid = [round(centroid[i]/len(cluster)) for i in range(len(centroid))]  # Then take averages
    return centroid


def sse(clusters, vectors):
    score = 0

    for cluster in clusters:
        centroid = get_centroid(cluster, vectors)

        for country in cluster:
            score += pow(distance_function(vectors[country], centroid), 2)

    return score


def main(input_f, output_f):
    (countries, vectors) = read_file(input_f)
    print(countries)
    print(vectors)

    clusters = utils.kcluster(vectors, distance=distance_function, k=num_clusters)
    proper_clusters = []  # Nonempty clusters
    for i in range(num_clusters):
        if len(clusters[i]) == 0:
            continue

        proper_clusters.append(clusters[i])
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in clusters[i]])

    print("SSE: " + str(sse(proper_clusters, vectors)))


if __name__ == "__main__":
    main("data/preprocessed.csv", "")