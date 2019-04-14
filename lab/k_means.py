# Clustering with basic k-means
import sys
import word_cloud
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


def write_output(country_clusters, output_f):
    output = open(output_f, "w")
    output.write("[['Country', 'Value'],\n")

    for i in range(len(country_clusters)):
        cluster = country_clusters[i]

        for country in cluster:
            output.write("['" + country + "', " + str(i) + "],\n")  # Manually fix the end

    output.close()


def make_word_clouds(clusters, vectors):
    # First open the keywords file
    keyword_file = open("data/dimensions_keywords.csv")
    lines = keyword_file.read().split('\n')
    keywords = []
    for i in range(len(lines)):
        if i == 0:
            continue

        keywords.append(lines[i].split(',')[1:])

    for j in range(len(clusters)):
        cluster = clusters[j]
        words = []
        centroid = get_centroid(cluster, vectors)

        for i in range(len(centroid)):
            if centroid[i] > 50:
                label = 0
            else:
                label = 1

            words.append((keywords[i][label].split(' '), (centroid[i] if centroid[i] > 50 else 100 - centroid[i])))

        d = {}
        for (word_list, weight) in words:
            for word in word_list:
                if word in d:
                    d[word] += weight/100
                else:
                    d[word] = weight/100

        word_counts = [(w, count/15) for w, count in d.items()]
        word_cloud.create_cloud("clouds/{}.png".format(str(j)), word_counts)


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
    country_clusters = []  # Clusters of country names instead of indexes
    for i in range(num_clusters):
        if len(clusters[i]) == 0:
            continue

        proper_clusters.append(clusters[i])
        print('cluster {}:'.format(i + 1))
        print([countries[r] for r in clusters[i]])
        country_clusters.append([countries[r][1] for r in clusters[i]])

    print("SSE: " + str(sse(proper_clusters, vectors)))

    write_output(country_clusters, output_f)
    make_word_clouds(clusters, vectors)


if __name__ == "__main__":
    main("data/preprocessed.csv", "data/country_clusters.json")
