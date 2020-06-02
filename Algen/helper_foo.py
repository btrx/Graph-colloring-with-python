""" Helper Functions and Objects
"""

import matplotlib.pyplot as plt  # Drawing graphs
import networkx as nx  # Generating of graphs
import numpy as np


# Define the main data structure
class World_Map:
    def __init__(self, colors, adjacency_list):
        """
        Initialization of World_Map object

        :param colors: String of 'r', 'g' or 'b' - e.g. 'rbbgrgbg'
        :type colors: str
        :param adjacency_list: adjacency list - list tetangga antara tiap titik
        :type adjacency_list: list of lists
        """
        self.colors = colors  # string .. i-th element represents color - 3 possible colours 'r','g' and 'b'
        self.adjacency_list = adjacency_list  # list of lists
        self.n_nodes = len(self.colors)
        self.fitness, self.graph_nx = self.__convert_to_nxgraph(self.colors, self.adjacency_list)

    # The networks package offers amazing visualization features
    def __convert_to_nxgraph(self, colors, adjacency_list):
        """
        Generates a networkx graph object and in the meantime calculates fitness

        :param colors: String of 'r', 'g' or 'b' - e.g. 'rbbgrgbg'
        :type colors: str
        :param adjacency_list: adjacency list - list of neighbours for each node
        :type adjacency_list: list of lists
        :return: (fitness, networkx graph object)
        :rtype: (int, netowrkx Graph)
        """
        G = nx.Graph()
        counter = 0  # the number of edges connecting same colors
        number_of_edges_twice = 0

        for index, node_color in enumerate(colors):
            G.add_node(index, color=node_color)  # Index the label
            for neighbour in adjacency_list[index]:
                # input edge
                G.add_edge(index, neighbour, illegal=False)  # illegal bool denotes whether nodes of the same color
                number_of_edges_twice += 1
                if node_color == colors[neighbour]:
                    G[index][neighbour]['illegal'] = True
                    counter += 1

        return number_of_edges_twice / 2 - counter / 2, G

    def print_me(self, figure_number=-1, figure_title=''):
        """
        Prints a graph representing the object

        :param figure_number: number of the figure
        :type figure_number: int
        :param figure_title: name of the figure
        :type figure_title: str

        """
        color_mapping = {True: 'r', False: 'g'}

        node_list = self.graph_nx.nodes(data=True)
        edge_list = self.graph_nx.edges(data=True)

        colors_nodes = [element[1]['color'] for element in node_list]
        colors_edges = [color_mapping[element[2]['illegal']] for element in edge_list]
        plt.figure(figure_number)
        plt.title(figure_title)
        nx.draw_networkx(self.graph_nx, with_labels=True, node_color=colors_nodes, edge_color=colors_edges)
        plt.draw()


# Generate graph acak
def generate_random_graph(number_of_nodes, probability_of_edge):
    """Generate graph dengan jumlah garis = jumlah_titk * kemungkinan_adanya_garis

    :param number_of_nodes: jumlah titik pada graf
    :type number_of_nodes: int
    :param probability_of_edge: Kemungkinan adanya garis dari dua titik
    :type probability_of_edge: float
    :return: (jumlah garis, list kedekatan)
    :rtype: (int, list of lists)
    """

    G = nx.fast_gnp_random_graph(number_of_nodes, probability_of_edge, seed=None, directed=False)
    edges = []
    for i in range(number_of_nodes):
        temp1 = G.adj[i]
        edges.append(list(G.adj[i].keys()))
    return G.number_of_edges(), edges


# Generate populasi awal acak
def generate_random_initial_population(population_size, n_nodes, al):
    """Buat populasi awal acak

    :param population_size: ukuran populasi
    :type population_size: int
    :param n_nodes: jumlah titik
    :type n_nodes: int
    :param al: list kedekatan
    :type al: list of lists
    :return: populasi acak
    :rtype: list of World_Map
    """
    input_population = []

    # Buat populasi awal acak
    for _ in range(population_size):
        color_list = np.random.choice(['r', 'b', 'g'], n_nodes, replace=True)
        color_string = "".join(color_list)
        input_population.append(World_Map(color_string, al))
    print('A random population of ' + str(population_size) + ' people was created')

    return input_population


# Mengacak evolusi
def evolution(input_population, n_generations, population_size, percentage_to_keep=0.1, genetic_op='SPC'):
    """Mengupdate generasi tiap iterasi

    :param input_population: input populasi
    :type input_population: list of World_Map
    :param n_generations: jumlah generasi yang akan disimulasi
    :type n_generations: int
    :param population_size: ukuran populasi - ukuran konstan sepanjang evolusi
    :type population_size: int
    :param percentage_to_keep:  persentase parent terbaik lanjut ke generasi selanjutnya, dalam (0,1)
    :type percentage_to_keep: float
    :param genetic_op: operasi genetik (crossover/mutasi)
    :type genetic_op: str
    :return: (for each generation list of fitness of each person, for each generation the fittest person)
    :rtype: (list of lists, list of World_Map)
    """
    # We will find the histogram for each generation and the fittest person
    results_fitness = []
    results_fittest = []

    for i in range(n_generations):
        print('Your population is in the ' + str(i + 1) + '-th generation')
        # Menyimpan hasil
        fitness_list, ix, fittest_coloring = find_fittest(input_population)
        results_fitness.append(fitness_list)
        results_fittest.append(fittest_coloring)
        # Print fitness terbaik
        print('The fittest person is: ' + str(max(fitness_list)))

        # Update populasi
        output_population = population_update(input_population, population_size,
                                              percentage_to_keep=percentage_to_keep, genetic_op=genetic_op)
        input_population = output_population

    return results_fitness, results_fittest


# Find fittest
def find_fittest(input_population):
    """Dalam populasi, mencari gen terbaik

    :param input_population: input populasi
    :type input_population: list of World_Map
    :return: (list nilai fitness untuk seluruh populasi, index gen terbaik, gen terbaik)
    :rtype: (list, int, World_Map)
    """
    fitness_list = [person.fitness for person in input_population]
    ix = np.argmax(fitness_list)
    return fitness_list, ix, input_population[ix]


# Update populasi
def population_update(input_population, output_population_size, percentage_to_keep=0.1, genetic_op='SPC'):
    """Langkah update populasi

    :param input_population: input populasi
    :type input_population: list of World_Map
    :param output_population_size: ukuran output populasi
    :type output_population_size: int
    :param percentage_to_keep: persentase parent terbaik untuk lanjut ke generasi selanjutnya, in (0,1)
    :type percentage_to_keep: float
    :param genetic_op: operator genetik yang dilakukan dalam evolusi
    :type genetic_op: str
    :return: output populasi
    :rtype: list of World_Map
    """
    input_population_size = len(input_population)
    output_population = []

    # Menyimpan input populasi terbaik sebesar x persen ke output_population
    input_population.sort(key=lambda x: x.fitness, reverse=True)
    output_population += input_population[:int(input_population_size * percentage_to_keep)]

    # Membuat list pasangan
    list_of_parent_pairs = parent_selection(input_population, input_population_size // 2)

    # Evolusi populasi baru
    pair_index = 0
    while len(output_population) < output_population_size:
        child_1, child_2 = genetic_operator(list_of_parent_pairs[pair_index], method=genetic_op)
        output_population.append(child_1)
        output_population.append(child_2)
        pair_index += 1

    return output_population


# Membuat list pasangan dari input populasi
def parent_selection(input_population, number_of_pairs):
    """Membuat pasangan dari input populasi

    :param input_population: input populasi
    :type input_population: list of World_Map
    :param number_of_pairs: jumlah pasangan yang diinginkan -> output populasi = 2 * number_of_pairs
    :type number_of_pairs: int
    :return: pasangan parent dari input populasi
    :rtype: list of pairs of World_Map
    """

    input_n = len(input_population)

    # Menggunkan metode Fitness proportional selection
    # karena fitness non-negative, dapat menggunakan formula  fitness_i/sum(fitness)
    fitness_sum = sum([person.fitness for person in input_population])
    probabilities = np.array([person.fitness / fitness_sum for person in input_population])

    I_x = np.random.choice(np.arange(0, input_n), number_of_pairs, p=probabilities)
    I_y = np.random.choice(np.arange(0, input_n), number_of_pairs, p=probabilities)

    return [(input_population[I_x[i]], input_population[I_y[i]]) for i in range(number_of_pairs)]


# Operator genetik
def genetic_operator(pair_of_parents, method='SPC'):
    """Untuk setiap pasangan parent memberikan output pasangan children berdasarkan operator genetik yang digunakan

    :param pair_of_parents: pasangan parent
    :type pair_of_parents: pair of World_Map
    :param method: metoder operator genetik. 'SPC' - single point crossover; 'mutation'
    :type method: str
    :return: pair of children
    :rtype: pair of World_Map
    """

    n_nodes = pair_of_parents[0].n_nodes
    al = pair_of_parents[0].adjacency_list

    if method == 'mutation':
        # Metode ini tidak membutuhkan pasangan parent karena inputnya hanya satu

        node1 = np.random.randint(0, n_nodes)
        node2 = np.random.randint(0, n_nodes)

        mapper = {'r': ['b', 'g'], 'b': ['r', 'g'], 'g': ['r', 'b']}

        child_one_colors = pair_of_parents[0].colors
        child_two_colors = pair_of_parents[1].colors

        child_one_colors = child_one_colors[:node1] + np.random.choice(mapper[child_one_colors[node1]],
                                                                       1)[0] + child_one_colors[node1 + 1:]
        child_two_colors = child_two_colors[:node2] + np.random.choice(mapper[child_two_colors[node2]],
                                                                       1)[0] + child_two_colors[node2 + 1:]

        return World_Map(child_one_colors, al), World_Map(child_two_colors, al)

    if method == 'SPC':  # Single point crossover
        # Memilih titik acak kemudian
        # Semua warna disebelah kiri dari Parent 1, dan sebelah kanan dari Parent 2
        point = np.random.randint(0, n_nodes)

        parent_1_colors = pair_of_parents[0].colors
        parent_2_colors = pair_of_parents[0].colors

        child_one_colors = parent_1_colors[:point] + parent_2_colors[point:]
        child_two_colors = parent_2_colors[:point] + parent_1_colors[point:]

        return (World_Map(child_one_colors, al), World_Map(child_two_colors, al))


# Memvisualisasikan hasil
def visualize_results(results_fitness, results_fittest, number_of_generations_to_visualize=6):
    """Visualisasi evolusi

    :param results_fitness: list semua gen untuk setiap generasi
    :type results_fitness: list of lists
    :param results_fittest: list gen terbaik untuk setiap generasi
    :type results_fittest: list of World_Map
    :param number_of_generations_to_visualize: jumlah generasi yang akan ditampilkan - min: 2, generasi pertama dan terakhir
    :type number_of_generations_to_visualize: int
    :return: Plot the graf gen terbaik dan histogram untuk setiap generasi
    """

    # Important
    total_generations = len(results_fitness)

    # Pick generations to visualize
    I = list(
        np.random.choice(list(range(1, total_generations - 1)), number_of_generations_to_visualize - 2, replace=False))
    I += [0, total_generations - 1]
    I.sort()
    print("Visualized generations: ",end='')
    print(I)

    # Main
    for i, order in enumerate(I):
        # print fittest
        results_fittest[order].print_me(figure_number=i,
                                        figure_title='generation: ' + str(order + 1) + ', fitness: ' + str(
                                            results_fittest[order].fitness))
        # Print histogram
        plt.figure(-i - 1)  # means nothing
        plt.hist(results_fitness[order])
        plt.title('Generation_number: ' + str(order + 1))
        plt.draw()
