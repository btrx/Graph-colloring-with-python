import tkinter as tk
from helper_foo import *

def getParameter():

    get_node = int(float(ent_nodes.get()))
    get_population = int(float(ent_population.get()))
    get_generation = int(float(ent_generation.get()))
    get_adjacency = float(ent_adjacency.get())/100
    get_parent_percentage = float(ent_parent_percentage.get())/100
    get_genetic = genetic.get()
    return get_node, get_population, get_generation, get_adjacency, get_parent_percentage, get_genetic

def generate():

    # Get parameter from gui
    n_nodes, population_size, n_generations, adjacency, percentage_of_parents_to_keep, genetic_op = getParameter()
    print(n_nodes, population_size, n_generations, adjacency, percentage_of_parents_to_keep, genetic_op)
    
    number_of_edges, al = generate_random_graph(n_nodes, adjacency)  # Generate garis penghubung acak dengan probabilitas
    print("Number of edges: " + str(number_of_edges))

    # MAIN ALGORITHM
    # Acak populasi awal
    input_population = generate_random_initial_population(population_size, n_nodes, al)
    # Mulai iterasi 
    results_fitness, results_fittest = evolution(input_population, n_generations, population_size,
                                                 percentage_to_keep=percentage_of_parents_to_keep,
                                                 genetic_op=genetic_op)

    # VISUALIZE
    visualize_results(results_fitness, results_fittest, 4)
    plt.show()
    pass

window = tk.Tk()
window.title("Graph Coloring")
window.resizable(0, 0)

genetic = tk.StringVar(None, "mutation")

frm_main = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=2)
frm1 = tk.Frame(master=frm_main)
frm1.grid(row=0, column=0, padx=4, pady=4, sticky="n")
frm2 = tk.Frame(master=frm_main)
frm2.grid(row=0, column=1, padx=4, pady=4, sticky="n")
frm_btn = tk.Frame(master=window)

lbl_nodes = tk.Label(master=frm1, text="Jumlah Titik")
lbl_nodes.grid(row=0, column=0, sticky="w")
ent_nodes = tk.Entry(master=frm1)
ent_nodes.grid(row=1, column=0, sticky="w")
ent_nodes.insert(0, "18")

lbl_population = tk.Label(master=frm1, text="Ukuran Populasi")
lbl_population.grid(row=2, column=0, sticky="w")
ent_population = tk.Entry(master=frm1,)
ent_population.grid(row=3, column=0, sticky="w")
ent_population.insert(0, "100")

lbl_generation = tk.Label(master=frm1, text="Jumlah Generasi")
lbl_generation.grid(row=4, column=0, sticky="w")
ent_generation = tk.Entry(master=frm1)
ent_generation.grid(row=5, column=0, sticky="w")
ent_generation.insert(0, "100")

lbl_adjacency = tk.Label(master=frm2, text="% Probabilitas garis penghubung")
lbl_adjacency.grid(row=0, column=0, sticky="w")
ent_adjacency = tk.Entry(master=frm2)
ent_adjacency.grid(row=1, column=0, sticky="w")
ent_adjacency.insert(0, "35")

lbl_parent_percentage = tk.Label(master=frm2, text="% Gen lanjut ke Generasi berikutnya")
lbl_parent_percentage.grid(row=2, column=0, sticky="w")
ent_parent_percentage = tk.Entry(master=frm2)
ent_parent_percentage.grid(row=3, column=0, sticky="w")
ent_parent_percentage.insert(0, "10")

lbl_gen_op = tk.Label(master=frm2, text="Jenis Evolusi")
lbl_gen_op.grid(row=4, column=0, sticky="w")
go1 = tk.Radiobutton(master=frm2, text="Mutasi", variable=genetic, value="mutation")
go2 = tk.Radiobutton(master=frm2, text="Crossover", variable=genetic, value="SPC")
go1.grid(row=5, column=0, sticky="w")
go2.grid(row=5, column=0, sticky="e")
# ent_gen_op = tk.Entry(master=frm2)
# ent_gen_op.grid(row=3, column=0, sticky="w")
# ent_gen_op.insert(0, "mutation")

btn = tk.Button(master=frm_btn, text="Generate", command=generate)
btn.pack()

frm_main.pack(padx=4, pady=4)
frm_btn.pack(ipady=2, side=tk.TOP)

window.mainloop()
