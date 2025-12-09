import networkx as nx
import matplotlib.pyplot as plt
from MoebiusStrip import Strip, Universe, Gate
from MorbiusFlower import MorbiusFlower
import Pruebas

def visualize_flower_nx(flower, filename='morbius_structure_nx.png'):
    G = nx.DiGraph()
    
    # Colores para los nodos
    labels = {}
    
    # Iterar sobre las Gates en la Flor
    gates = []
    try:
        for gate in flower:
            gates.append(gate)
    except Exception as e:
        print(f"Error iterando la flor: {e}")
        return

    # Construir el grafo
    for i, gate in enumerate(gates):
        gate_id = f"Gate_{i}"
        G.add_node(gate_id, label=f"Gate {i}", type='gate')
        labels[gate_id] = f"Gate {i}"
        
        # Recorrer la Strip (Universes)
        current = gate.next
        prev_id = gate_id
        
        visited_universes = {gate} # Usamos objetos para identidad
        
        u_index = 0
        while True:
            if current == gate: # Volvimos al inicio (Gate)
                G.add_edge(prev_id, gate_id, color='black')
                break
            
            if current in visited_universes:
                break

            visited_universes.add(current)
            
            u_id = f"U_{i}_{u_index}"
            label = f"H:{current.heaven}\nL:{current.hell}"
            
            G.add_node(u_id, label=label, type='universe')
            labels[u_id] = label
            
            G.add_edge(prev_id, u_id, color='black')
            
            prev_id = u_id
            current = current.next
            u_index += 1

    # Conectar las Gates (La estructura de la Flor)
    for i in range(len(gates)):
        current_gate_id = f"Gate_{i}"
        next_gate_index = (i + 1) % len(gates) 
        next_gate_id = f"Gate_{next_gate_index}"
        
        G.add_edge(current_gate_id, next_gate_id, color='red', weight=2)

    # Dibujar
    plt.figure(figsize=(12, 8))
    
    # Layout
    pos = nx.kamada_kawai_layout(G) 
    
    # Dibujar nodos
    node_colors = []
    for node in G.nodes():
        if G.nodes[node].get('type') == 'gate':
            node_colors.append('lightblue')
        else:
            node_colors.append('lightgreen')

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    # Dibujar aristas
    edges = G.edges()
    edge_colors = [G[u][v].get('color', 'black') for u, v in edges]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, arrowstyle='->', arrowsize=20)
    
    plt.title("Visualización de Estructura MorbiusFlower")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Visualización guardada en: {filename}")
    plt.close()

if __name__ == "__main__":
    # Recreamos la estructura de Pruebas.py
    
    # Strip 1
    strip1 = Strip()
    for i in range(1, 6):
        strip1.append(i, i+5)
    strip1.add(3, "Hola", "Mundo")

    # Strip 2
    strip2 = Strip()
    for i in range(10, 16):
        strip2.append(i, i+5)
    strip2.delete(3)

    # Strip 3
    strip3 = Strip()
    for i in range(20, 26):
        strip3.append(i, i+5)

    # Strip 4
    strip4 = Strip()
    for i in range(30, 36):
        strip4.append(i, i+5)

    # Flor
    flower = MorbiusFlower(strip2)
    flower.append(strip3)
    flower.append(strip4)
    flower.add(0, strip1)

    print("Generando visualización con NetworkX...")
    visualize_flower_nx(flower)
