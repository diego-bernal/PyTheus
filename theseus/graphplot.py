import matplotlib.pyplot as plt
import numpy as np
import matplotlib.collections as collections
import theseus.theseus as th
from cmath import polar 



def drawEdge(edge, verts, ind, mult,ax, scale_max=None, max_thickness=10,
             show_val = False):
    colors = ['blue', 'red', 'green', 'darkorange', 'purple', 'yellow', 'cyan']
    col1 = colors[int(edge[2])]
    col2 = colors[int(edge[3])]

    vert1 = np.array(verts[int(edge[0])])
    vert2 = np.array(verts[int(edge[1])])
    if not np.array_equal(vert1, vert2):
        diff = vert1 - vert2
        rect = [diff[1], -diff[0]]
        rect /= np.linalg.norm(rect)
        hp = (vert1 + vert2) / 2 + (2 * ind - mult + 1) * 0.05 * rect
    else:
        hp = vert1 * 1.2

    if scale_max is None:
        lw = max_thickness

    else:
        lw = np.max([abs(max_thickness * edge[4]) / scale_max, 0.5])

    try:
        transparency = 0.2 + abs(edge[4]) * 0.8
        transparency =  min(transparency,1)
    except IndexError:
        transparency = 1
    ax.plot([vert1[0], hp[0]], [vert1[1], hp[1]], color=col1, linewidth=lw,alpha=transparency)
    ax.plot([hp[0], vert2[0]], [hp[1], vert2[1]], col2, linewidth=lw,alpha=transparency)

    if show_val:
        
        if transparency > 0.5 and col1 == "blue" :
            font_col = 'white'
        else: font_col = 'black'

        ax.text(np.mean([0.9*vert1[0], hp[0]]), np.mean([0.9*vert1[1], hp[1]]),f"{edge[4]:.4f}",
                 bbox={'facecolor':col1 ,'alpha':transparency,'edgecolor':col2,'pad':1},c =font_col,
                 ha='center', va='center',rotation=0,fontweight ='heavy')
    try:
        if edge[4] < 0:
            ax.plot(hp[0], hp[1], marker="d", markersize=25, markeredgewidth="6", markeredgecolor="black",
                     color="white")
    except:
        pass


def graphPlot(graph, scaled_weights=False, show=True, max_thickness=10,
              weight_product=False, ax_fig = (), add_title= '',
              show_value_for_each_edge= False, fontsize= 30):
    edge_dict = th.edgeBleach(graph.edges)

    num_vertices = len(np.unique(np.array(graph.edges)[:, :2]))

    angles = np.linspace(0, 2 * np.pi * (num_vertices - 1) / num_vertices, num_vertices)

    rad = 0.9
    vertcoords = []
    for angle in angles:
        x = rad * np.cos(angle)
        y = rad * np.sin(angle)
        vertcoords.append(tuple([x, y]))

    vertnums = list(range(num_vertices))
    verts = dict(zip(vertnums, vertcoords))

    if scaled_weights:
        try:
            scale_max = np.max(np.abs(np.array(graph.edges)[:, 4]))
        except:
            scale_max = None
    else:
        scale_max = None
    
    if len(ax_fig) == 0:
        fig, ax = plt.subplots(figsize=(10, 10))
    else: 
        fig, ax = ax_fig
    
    for uc_edge in edge_dict.keys():
        mult = len(edge_dict[uc_edge])
        for ii, coloring in enumerate(edge_dict[uc_edge]):
            drawEdge(uc_edge + coloring + tuple([graph[tuple(uc_edge + coloring)]]), verts, ii, mult,ax,
                     scale_max=scale_max, max_thickness=max_thickness,
                     show_val = show_value_for_each_edge)

    circ = []
    for vert, coords in verts.items():
        circ.append(plt.Circle(coords, 0.1, alpha=0.5))
        ax.text(coords[0], coords[1], str(vert), zorder=11,
                ha='center', va='center', size=fontsize)
    circ = collections.PatchCollection(circ, zorder=10)
    ax.add_collection(circ)

    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([-1.1, 1.1])
    ax.axis('off')

    if weight_product:
        total_weight = np.product(graph.weights)
        if isinstance(total_weight, complex):
            wp = r"$ {0} \cdot e^{{  {1} i   }} $".format(
                *np.round(polar(total_weight),3))
        else: 
            wp = str(np.round(total_weight,3))
        ax.set_title( wp + str(add_title), fontsize=fontsize)
        
    if add_title != '' and weight_product is False :
        ax.set_title( str(add_title), fontsize=fontsize)
    
    if show:
        plt.show()
        plt.pause(0.01)
    else:
        pass
    return fig
