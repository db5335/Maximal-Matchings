from manim import *

'''
Reads a file containing information about the simulation of a run of the maximal
matching algorithm presented in the following paper and produces a visualization.

https://arxiv.org/abs/2104.09096

Author: Dominick Banasik
'''

# -ql for 480p
# -qm for 720p
# -qh for 1080p 60fps
# -qk for 4k 60fps

DEFAULT_COLOR = DARK_GRAY
SENDING_COLOR = BLUE
LISTENING_COLOR = YELLOW
MATCHING_COLOR = RED

# Change filename here
with open('output.txt') as file:
    name = file.readline()
    n_est = int(file.readline())
    d_est = int(file.readline())
    c = int(file.readline())
    
    n = int(file.readline())
    vertices = list(range(n))

    m = int(file.readline())

    positions = []
    for i in range(n):
        (x, y) = file.readline().split(' ')
        positions.append((float(x), float(y), 0))

    edges = []
    for i in range(m):
        (u, v) = file.readline().split(' ')
        edges.append((int(u), int(v)))
        edges.append((int(v), int(u)))

    rounds = []
    for line in file.readlines():
        if line == '\n':
            rounds.append([])
        else:
            rounds.append(list(map(int, line.split(' '))))
    rounds.append([])

class Algo(Scene):
    def construct(self):
        edge_config = {
            "stroke_color": DARK_GRAY,
            "tip_config": {"tip_length": 0, "tip_width": 0}
        }

        # g = DiGraph(vertices, edges, layout="circular", layout_scale=3, edge_config=edge_config)

        layout = {}
        for v in vertices:
            layout[v] = positions[v]


        # Change graph layout here

        g = DiGraph(vertices, edges, layout=layout, edge_config=edge_config)
        # g = DiGraph(vertices, edges, layout="circular", layout_scale=3, edge_config=edge_config)
        text = Text("1").to_corner(UR)
        self.add(text)

        
        # Change text in upper left corner here

        # name = Tex("Clique\\\\$n=12$\\\\$\Delta=11$", tex_environment=None).to_corner(UL)
        name = Tex("Planar Graph\\\\$n=50$\\\\$\Delta=10$", tex_environment=None).to_corner(UL)
        self.add(name)


        self.add(g)
        for v in vertices:
            g[v].set_fill(DEFAULT_COLOR)
        self.wait(0.05)

        animations = []
        matched = []
        permanent = []
        for i in range(len(rounds)):
            print(f'{i} / {len(rounds)}')
            if i % 6 == 0:
                for v in vertices:
                    if v not in matched:
                        g[v].set_fill(DEFAULT_COLOR)
                for v in rounds[i]:
                    g[v].set_fill(SENDING_COLOR)
                    nbrs = list(filter(lambda edge: edge[0] == v, edges))
                    for nbr in nbrs:
                        g.edges[nbr].set_z_index(-2)
                    animations.append(g.animate.remove_edges(*nbrs))
                    animations.append(g.animate.add_edges(*nbrs, edge_config={"stroke_color": SENDING_COLOR}))
                if i < len(rounds) - 1:
                    for v in rounds[i + 1]:
                        g[v].set_fill(LISTENING_COLOR)
            elif i % 6 == 1:
                for v in rounds[i - 1]:
                    nbrs = list(filter(lambda edge: edge[0] == v, edges))
                    for nbr in nbrs:
                        g.edges[nbr].set_z_index(2)
                    animations.append(g.animate.remove_edges(*nbrs))
                    animations.append(g.animate.add_edges(*nbrs, edge_config={"stroke_color": DEFAULT_COLOR}))
            elif i % 6 == 2:
                for v in rounds[i]:
                    nbrs = list(filter(lambda edge: edge[0] == v, edges))
                    for nbr in nbrs:
                        g.edges[nbr].set_z_index(-2)
                    animations.append(g.animate.remove_edges(*nbrs))
                    animations.append(g.animate.add_edges(*nbrs, edge_config={"stroke_color": LISTENING_COLOR}))
            elif i % 6 == 3:
                for v in rounds[i - 1]:
                    nbrs = list(filter(lambda edge: edge[0] == v, edges))
                    for nbr in nbrs:
                        g.edges[nbr].set_z_index(0)
                    animations.append(g.animate.remove_edges(*nbrs))
                    animations.append(g.animate.add_edges(*nbrs, edge_config={"stroke_color": DEFAULT_COLOR}))
            elif i % 6 == 4:
                for v in rounds[i]:
                    matched.append(v)
                    g[v].set_fill(MATCHING_COLOR)
                    nbrs = list(filter(lambda edge: edge[0] == v, edges))
                    for nbr in nbrs:
                        g.edges[nbr].set_z_index(-2)
                    animations.append(g.animate.remove_edges(*nbrs))
                    animations.append(g.animate.add_edges(*nbrs, edge_config={"stroke_color": MATCHING_COLOR}))
                    nbr = list(filter(lambda edge: edge[1] in rounds[i + 1], nbrs))[0]
                    permanent.append(nbr)
            elif i % 6 == 5:
                for v in rounds[i - 1]:
                    matched.append(v)
                    nbrs = list(filter(lambda edge: edge[0] == v and edge[1] not in rounds[i], edges))
                    for nbr in nbrs:
                        g.edges[nbr].set_z_index(0)
                    animations.append(g.animate.remove_edges(*nbrs))
                    animations.append(g.animate.add_edges(*nbrs, edge_config={"stroke_color": DEFAULT_COLOR}))
            if len(animations) > 0:
                for edge in permanent:
                    g.edges[edge].set_z_index(3)
                g.update_edges(g)
                if i % 6 == 0 and i < len(rounds) - 1:
                    new_text = Text(str(i // 6 + 1)).to_corner(UR)
                    animations.append(ReplacementTransform(text, new_text))
                    text = new_text
                self.play(*animations, run_time=0.3)
                for nbr in permanent:
                    matched.append(nbr[1])
                    g[nbr[1]].set_fill(MATCHING_COLOR)
                permanent = []
                animations = []
            else:
                if i % 6 == 0 and i < len(rounds) - 1:
                    new_text = Text(str(i // 6 + 1)).to_corner(UR)
                    self.play(ReplacementTransform(text, new_text), run_time=0.05)
                    text = new_text
                else:
                    self.wait(0.05)
                pass