import networkx as nx
import plotly.graph_objects as go
from MoebiusStrip import Strip, Universe, Gate
from MorbiusFlower import MorbiusFlower
import numpy as np

def visualize_flower_3d(flower, filename='morbius_structure_3d.html'):
    G = nx.DiGraph()
    
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
        # Guardamos info en el nodo para colorear y etiquetar
        G.add_node(gate_id, label=f"Gate {i}", group='gate', strip_index=i)
        
        # Recorrer la Strip (Universes)
        current = gate.next
        prev_id = gate_id
        
        visited_universes = {gate}
        
        u_index = 0
        while True:
            if current == gate:
                G.add_edge(prev_id, gate_id)
                break
            
            if current in visited_universes:
                break

            visited_universes.add(current)
            
            u_id = f"U_{i}_{u_index}"
            label = f"H:{current.heaven}<br>L:{current.hell}"
            
            G.add_node(u_id, label=label, group='universe', strip_index=i)
            G.add_edge(prev_id, u_id)
            
            prev_id = u_id
            current = current.next
            u_index += 1

    # Conectar las Gates (La estructura de la Flor)
    for i in range(len(gates)):
        current_gate_id = f"Gate_{i}"
        next_gate_index = (i + 1) % len(gates)
        next_gate_id = f"Gate_{next_gate_index}"
        G.add_edge(current_gate_id, next_gate_id, type='flower_connection')

    # Generar Layout 3D Simétrico tipo Moebius con Cintas (Ribbons)
    
    traces = []
    
    num_gates = len(gates)
    R = 15  # Radio mayor (Flor)
    r = 4   # Radio medio del Strip
    width = 1.5 # Ancho de la cinta (mitad)
    
    # Listas para nodos de texto (H y L)
    text_h_x, text_h_y, text_h_z, text_h_val = [], [], [], []
    text_l_x, text_l_y, text_l_z, text_l_val = [], [], [], []
    
    # Conexiones entre Gates
    gate_coords = []

    for i, gate in enumerate(gates):
        # Ángulo en la flor (0 a 2pi)
        theta = 2 * np.pi * i / num_gates
        
        # Centro del Strip actual
        cx = R * np.cos(theta)
        cy = R * np.sin(theta)
        cz = 0
        center = np.array([cx, cy, cz])
        
        # Vectores base para el anillo del strip
        # Normal (radial hacia afuera del toro)
        normal = np.array([np.cos(theta), np.sin(theta), 0])
        # Binormal (eje Z)
        binormal = np.array([0, 0, 1])
        
        # Torsión de Moebius: rotamos el plano del strip alrededor de la tangente del toro
        # Giramos 180 grados (pi) a lo largo de toda la flor
        twist_angle = np.pi * i / num_gates
        
        # Vectores rotados para el plano del strip
        # v1 y v2 definen el plano donde vive el anillo del strip
        v1 = normal * np.cos(twist_angle) + binormal * np.sin(twist_angle)
        v2 = -normal * np.sin(twist_angle) + binormal * np.cos(twist_angle)
        
        # Obtener nodos del strip
        strip_nodes = []
        current = gate
        while True:
            strip_nodes.append(current)
            current = current.next
            if current == gate:
                break
        
        num_universes = len(strip_nodes)
        
        # Coordenadas para la malla de la cinta
        x_strip, y_strip, z_strip = [], [], []
        
        # Vector normal al plano del strip para la torsión local
        n_plane = np.cross(v1, v2)

        # --- GENERACIÓN DE GEOMETRÍA (Cinta Suave) ---
        # Usamos un número fijo de segmentos para que la cinta se vea bien 
        # incluso si hay pocos universos (o solo 1).
        N_SEGMENTS = 60
        
        for k in range(N_SEGMENTS):
            phi = 2 * np.pi * k / N_SEGMENTS
            
            # Vector radial local
            local_radial = np.cos(phi) * v1 + np.sin(phi) * v2
            
            # Torsión de Moebius local
            local_twist = phi / 2.0
            width_vec = local_radial * np.cos(local_twist) + n_plane * np.sin(local_twist)
            
            # Centro de la cinta en este punto
            p_center = center + r * local_radial
            
            # Bordes
            pos_h = p_center + width * width_vec
            pos_l = p_center - width * width_vec
            
            x_strip.extend([pos_h[0], pos_l[0]])
            y_strip.extend([pos_h[1], pos_l[1]])
            z_strip.extend([pos_h[2], pos_l[2]])

        # Triangulación de la malla
        I, J, K = [], [], []
        n_verts = 2 * N_SEGMENTS
        for k in range(N_SEGMENTS):
            h0 = 2 * k
            l0 = 2 * k + 1
            h1 = (2 * k + 2) % n_verts
            l1 = (2 * k + 3) % n_verts
            
            I.append(h0); J.append(l0); K.append(h1)
            I.append(l0); J.append(l1); K.append(h1)

        # Color de la cinta
        colors = ['green', 'red', 'purple', 'orange', 'cyan', 'magenta']
        color = colors[i % len(colors)]
        
        traces.append(go.Mesh3d(
            x=x_strip, y=y_strip, z=z_strip,
            i=I, j=J, k=K,
            color=color,
            opacity=0.5,
            name=f'Strip {i}'
        ))

        # --- COLOCACIÓN DE NODOS Y ETIQUETAS ---
        gate_pos = None
        
        for j, node in enumerate(strip_nodes):
            # Ángulo dentro del strip
            phi = 2 * np.pi * j / num_universes
            
            # Recalculamos posición para el nodo específico
            local_radial = np.cos(phi) * v1 + np.sin(phi) * v2
            local_twist = phi / 2.0
            width_vec = local_radial * np.cos(local_twist) + n_plane * np.sin(local_twist)
            p_center = center + r * local_radial
            
            pos_h = p_center + width * width_vec
            pos_l = p_center - width * width_vec
            
            # Guardar info para textos
            text_h_x.append(pos_h[0])
            text_h_y.append(pos_h[1])
            text_h_z.append(pos_h[2])
            text_h_val.append(f"H: {node.heaven}")
            
            text_l_x.append(pos_l[0])
            text_l_y.append(pos_l[1])
            text_l_z.append(pos_l[2])
            text_l_val.append(f"L: {node.hell}")
            
            if node == gate:
                gate_pos = p_center
                gate_coords.append(gate_pos)

    # Trazas de Texto (Heaven y Hell)
    traces.append(go.Scatter3d(
        x=text_h_x, y=text_h_y, z=text_h_z,
        mode='text',
        text=text_h_val,
        textposition="top center",
        textfont=dict(color='white', size=8),
        name='Heaven Values'
    ))
    
    traces.append(go.Scatter3d(
        x=text_l_x, y=text_l_y, z=text_l_z,
        mode='text',
        text=text_l_val,
        textposition="bottom center",
        textfont=dict(color='black', size=8),
        name='Hell Values'
    ))

    # Conexiones entre Gates (Línea roja)
    gx, gy, gz = [], [], []
    for gp in gate_coords:
        gx.append(gp[0]); gy.append(gp[1]); gz.append(gp[2])
    # Cerrar el ciclo
    if gate_coords:
        gx.append(gate_coords[0][0])
        gy.append(gate_coords[0][1])
        gz.append(gate_coords[0][2])
        
    traces.append(go.Scatter3d(
        x=gx, y=gy, z=gz,
        mode='lines+markers',
        line=dict(color='yellow', width=5),
        marker=dict(size=5, color='yellow'),
        name='Gate Connections'
    ))

    # Configurar layout de la figura
    fig = go.Figure(data=traces,
                    layout=go.Layout(
                        title='Visualización 3D Morbius Structure (Moebius Ribbons)',
                        showlegend=True,
                        scene=dict(
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgb(50,50,50)"),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgb(50,50,50)"),
                            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False, backgroundcolor="rgb(50,50,50)"),
                        ),
                        paper_bgcolor="rgb(30,30,30)",
                        margin=dict(t=40, b=0, l=0, r=0)
                    ))

    fig.write_html(filename)
    print(f"Visualización 3D guardada en: {filename}")

if __name__ == "__main__":
    # Recreamos la estructura exacta de Pruebas.py
    print("Recreando estructura de Pruebas.py...")
    
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

    #Strip 5
    strip5 = Strip()
    strip5.append("A", "Z")
    strip5.append("B", "Y")

    strip6 = Strip()

    # Creación Flor
    flower = MorbiusFlower(strip2)
    flower.append(strip3)
    flower.append(strip4)
    flower.append(strip5)
    flower.add(0, strip1)
    flower.add(2, strip6)
    

    strip6.append("X1", "W1")
    strip6.append("X2", "W2")
    strip6.append("X3", "W3")
    strip6.add(0, "X0", "W0")
    # Operación final en Pruebas.py
    # flower.delete(3) # Comentado para visualizar los 4 strips

    print("Generando visualización 3D...")
    visualize_flower_3d(flower)
