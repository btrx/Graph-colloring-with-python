
from algen import *

"""Pencarian solusi dari pewarnaan graf dengan menggunakan algoritma genetik"""

# PARAMETERS
population_size = 100  # Konstanta populasi
n_nodes = 18  # Jumlah negara = jumlah node dalam graf
number_of_edges, al = generate_random_graph(n_nodes, 0.35)  # Generate garis penghubung acak dengan probabilitas
n_generations = 100 # Jumlah generasi
genetic_op = 'mutation'
""" Isi genetic_op dengan 'SPC' / 'mutation'
'SPC' = Single Point Crossover / One-Cut-Point Crossover node 'n' acak, anak 
node pertama sama dengan orangtua node pertama dan seterusnya
'mutation' = Mutasi node acak dengan mengganti warnanya secara random.
"""
percentage_of_parents_to_keep = 0.1  # Persentase populasi terbaik lanjut ke generasi berikutnya

# Jumlah garis penghubung
print("Number of edges: " + str(number_of_edges))

# MAIN ALGORITHM
# Acak populasi awal
input_population = generate_random_initial_population(population_size, n_nodes, al)
# Mulai iterasi 
results_fitness, results_fittest = evolution(input_population, n_generations, population_size,
                                             percentage_to_keep=percentage_of_parents_to_keep,
                                             genetic_op=genetic_op)

# VISUALIZE
visualize_results(results_fitness, results_fittest, 2)
plt.show()
