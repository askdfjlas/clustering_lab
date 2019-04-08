import clusters

missing = []  # Indexes of countries with missing values
data_matrix = []  # Matrix of csv values
data_range = range(2, 8)  # Useful sub-indexes


# Read the input file and populate data_matrix and missing
def read_file(input_f):
    data = open(input_f)

    count = -2
    for line in data:
        count += 1
        if count == -1:  # Skip headers
            continue

        arr = line.rstrip().split(',')
        if '' in arr:
            missing.append(count)

        data_matrix.append(arr)

    data.close()


# Write data_matrix to an output file
def write_output(output_f):
    output = open(output_f, "w")

    for line in data_matrix:
        for i in range(len(line)):
            output.write(line[i] + ('\n' if i == (len(line) - 1) else ','))

    output.close()


# Return the 3 most similar countries
def find_similar(country, available):
    similarities = []  # List of 3 tuples of (index, score) with highest score
    country_vector = [int(country[i]) for i in available]

    for i in range(len(data_matrix)):
        if '' in data_matrix[i]:  # Skip countries without a full set of data
            continue

        test_vector = [int(data_matrix[i][j]) for j in available]
        similarities = sorted(similarities + [(clusters.pearson(country_vector, test_vector), i)])[:3]

    return [data_matrix[i] for i in map(lambda x: x[1], similarities)]


# Fill in missing values for a country
def fill(country):
    available = list(data_range)
    country_missing = []

    for index in data_range:
        if country[index] == '':
            available.remove(index)
            country_missing.append(index)

    similar_countries = find_similar(country, available)

    # Fill in missing values with averages
    for index in country_missing:
        country[index] = str(round(sum(map(lambda x: int(x[index]), similar_countries))/3))


# Main function
def main(input_f, output_f):
    read_file(input_f)

    for index in missing:
        fill(data_matrix[index])

    write_output(output_f)


if __name__ == "__main__":
    main("data/dataset.csv", "data/preprocessed.csv")

    for l in data_matrix:
        print(l)
