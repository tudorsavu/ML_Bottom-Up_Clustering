import numpy as np
import collections.abc
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

x = [1, 2, 4, 8, 9]
y = [1, 1, 1, 1, 1]


def euclidean_distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** (1 / 2)


def chebyshev_distance(p1, p2):
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))


metrics = {
    "euclidean": euclidean_distance,
    "chebyshev": chebyshev_distance
}


# helper functions:
def flatten(l, fl=False):
    if isinstance(l, collections.Iterable):
        if fl:
            return [float(a) for i in l for a in flatten(i)]
        else:
            return [int(a) for i in l for a in flatten(i)]
    else:
        if fl:
            return [float(l)]
        else:
            return [int(l)]


def create_distance_matrix(x, y, metric="euclidean"):
    # prima linie si coloana vor contine indicele punctelor,
    mat = np.zeros((len(x) + 1, len(y) + 1))
    for i in range(1, len(x) + 1):
        mat[0][i] = i - 1
        mat[i][0] = i - 1
    for i in range(2, len(x) + 1):
        j = 1
        while j < mat[i][0] + 1:
            mat[i][j] = metrics[metric]((x[i - 1], y[i - 1]), (x[j - 1], y[j - 1]))
            mat[j][i] = mat[i][j]
            j += 1
    # print(mat)
    return mat.tolist()


def pretty_print(mat):
    print("\n")
    for it in range(0, len(mat)):
        print(mat[it])


def avg(args):
    if len(args) == 0:
        return 0.0
    return sum(args) / len(args)


def get_avg_distance(copy, c_indices, it, mat):
    other_ind = [i + 1 for i in flatten(mat[it][0])]
    # print("my clust indices: ", c_indices, "others indices: ", other_ind)
    distances = [copy[i][j] for i in other_ind for j in c_indices]
    # print('distances:', distances, "avg=",avg(distances))
    return avg(distances)


def calculate_initial_centroid_xy(x, y, cluster):
    c1 = flatten(cluster[0])
    c2 = flatten(cluster[1])
    x_coord_avg = avg([x[i] for i in c1 + c2])
    y_coord_avg = avg([y[i] for i in c1 + c2])
    # print(x_coord, y_coord)
    return tuple((x_coord_avg, y_coord_avg))


def calculate_centroid_xy(x, y, others):
    x_coord_avg = avg([x[i] for i in others])
    y_coord_avg = avg([y[i] for i in others])
    # print(x_coord, y_coord)
    return tuple((x_coord_avg, y_coord_avg))


def get_distace_with_centroids(centroid, it, mat, x, y):
    other_instances = [i for i in flatten(mat[it][0])]
    other_centroid = calculate_centroid_xy(x, y, other_instances)
    # print("distance: ", euclidean_distance(centroid, other_centroid))
    return euclidean_distance(centroid, other_centroid)


def get_distance_with_ward_formula(centroid, it, mat, x, y, cluster):
    other_instances = [i for i in flatten(mat[it][0])]
    other_centroid = calculate_centroid_xy(x, y, other_instances)
    # print("distance: ", euclidean_distance(centroid, other_centroid))
    n_A = len(other_instances)
    n_B = len(flatten(cluster))
    print(n_A,n_B)
    return (n_A*n_B/(n_A+n_B)) * euclidean_distance(centroid, other_centroid)


# main functions:


def create_link_mat(size, points, distances):  # linkage matrix for dendrogram function
    lin_mat = np.zeros((size, 4))
    for i in range(0, len(lin_mat)):
        lin_mat[i][2] = distances[i]

    for it in range(0, size):
        if points[it][0] not in points:
            lin_mat[it][0] = points[it][0]
        if points[it][1] not in points:
            lin_mat[it][1] = points[it][1]
        if points[it][0] in points:
            lin_mat[it][0] = [i + size + 1 for i in range(0, len(points)) if points[i] == points[it][0]][0]
        if points[it][1] in points:
            lin_mat[it][1] = [i + size + 1 for i in range(0, len(points)) if points[i] == points[it][1]][0]

    # print(lin_mat)
    return lin_mat


def linkage(x, y, method="single", metric="euclidean"):
    if method == "centroids" or method == "ward":
        metric = "euclidean"
    mat = create_distance_matrix(x, y, metric)
    copy = create_distance_matrix(x, y, metric)
    # pretty_print(copy)
    points = []
    distances = []
    centroids = []
    while len(mat) > 2:
        min_distance_and_index = min([[mat[i][j], i, j] for i in range(2, len(mat)) for j in range(1, i)])
        distances.append((min_distance_and_index[0]))
        c = [min_distance_and_index[1], min_distance_and_index[2]]
        cluster = [mat[0][c[1]], mat[c[0]][0]]
        c_indices = [i + 1 for i in flatten(mat[c[0]][0]) + flatten(mat[0][c[1]])]
        centroid = calculate_initial_centroid_xy(x, y, cluster)
        centroids.append(centroid)
        it = 1
        while it < len(mat):
            if it not in [c[0], c[1]]:
                if method == "single":
                    update_val = min(mat[it][c[0]], mat[it][c[1]])
                if method == "complete":
                    update_val = max(mat[it][c[0]], mat[it][c[1]])
                if method == "average":
                    update_val = get_avg_distance(copy, c_indices, it, mat)
                if method == "centroids":
                    update_val = get_distace_with_centroids(centroid, it, mat, x, y)
                if method == "ward":
                    update_val = get_distance_with_ward_formula(centroid, it, mat, x, y, cluster)
                mat[it][c[0]] = update_val
                mat[it][c[1]] = update_val
                mat[c[0]][it] = update_val
                mat[c[1]][it] = update_val
            it += 1
        mat[0][c[0]] = cluster
        mat[c[0]][0] = cluster
        points.append(cluster)
        del mat[c[1]]
        for it in range(0, len(mat)):
            del mat[it][c[1]]
    pretty_print(mat)
    if method == "ward":
        centroids = []
    linkage_matrix = create_link_mat(len(x) - 1, points, distances)
    return [flatten(l) for l in points], linkage_matrix, centroids


# linkage(x, y, method="ward")
# create_distance_matrix(x, y)
