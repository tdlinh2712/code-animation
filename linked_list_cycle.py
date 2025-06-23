from manim import *

# === Editable Input ===
node_values = [3, 2, 0, -4]  # List of node values
cycle_pos = 1  # Index to which the last node points (set to None for no cycle)

class LinkedListCycleScene(Scene):
    def construct(self):
        node_radius = 0.5
        node_gap = 2.2
        start_x = -((len(node_values)-1)/2) * node_gap
        y_level = 1

        # Create node circles and labels
        nodes = []
        for i, val in enumerate(node_values):
            node = Circle(radius=node_radius, color=WHITE).move_to([start_x + i*node_gap, y_level, 0])
            label = Text(str(val), font_size=32).move_to(node.get_center())
            nodes.append(VGroup(node, label))

        # Draw nodes
        self.play(*[FadeIn(n) for n in nodes])
        self.wait(0.5)

        # Draw arrows (next pointers)
        arrows = []
        for i in range(len(nodes)-1):
            start = nodes[i][0].get_right()
            end = nodes[i+1][0].get_left()
            arrow = Arrow(start, end, buff=0.1, color=BLUE)
            arrows.append(arrow)
        # Cycle arrow
        if cycle_pos is not None and 0 <= cycle_pos < len(nodes):
            start = nodes[-1][0].get_right()
            end = nodes[cycle_pos][0].get_bottom()
            cycle_arrow = CurvedArrow(start, end, angle=-PI/2, color=YELLOW)
            arrows.append(cycle_arrow)
        self.play(*[GrowArrow(a) for a in arrows])
        self.wait(0.5)

        # Tortoise and Hare pointers
        tortoise = Dot(nodes[0][0].get_top() + UP*0.3, color=GREEN).scale(1.2)
        hare = Dot(nodes[0][0].get_top() + UP*0.7, color=RED).scale(1.2)
        tortoise_label = Text("T", font_size=24, color=GREEN).next_to(tortoise, UP, buff=0.1)
        hare_label = Text("H", font_size=24, color=RED).next_to(hare, UP, buff=0.1)
        self.play(FadeIn(tortoise), FadeIn(hare), FadeIn(tortoise_label), FadeIn(hare_label))
        self.wait(0.5)

        # Animate movement
        tort_idx = 0
        hare_idx = 0
        steps = 0
        met = False
        max_steps = len(node_values)*2 + 2  # Prevent infinite loop
        while steps < max_steps:
            # Move tortoise by 1
            next_tort = (tort_idx+1) if tort_idx+1 < len(nodes) else (cycle_pos if cycle_pos is not None else None)
            # Move hare by 2
            next_hare = hare_idx
            for _ in range(2):
                if next_hare+1 < len(nodes):
                    next_hare += 1
                elif cycle_pos is not None:
                    next_hare = cycle_pos
                else:
                    next_hare = None
                    break
            if next_tort is None or next_hare is None:
                break
            # Animate movement
            self.play(
                tortoise.animate.move_to(nodes[next_tort][0].get_top() + UP*0.3),
                tortoise_label.animate.next_to(nodes[next_tort][0].get_top() + UP*0.3, UP, buff=0.1),
                hare.animate.move_to(nodes[next_hare][0].get_top() + UP*0.7),
                hare_label.animate.next_to(nodes[next_hare][0].get_top() + UP*0.7, UP, buff=0.1),
                run_time=0.8
            )
            tort_idx = next_tort
            hare_idx = next_hare
            steps += 1
            if tort_idx == hare_idx:
                met = True
                break
        if met:
            # Highlight meeting node
            self.play(
                nodes[tort_idx][0].animate.set_fill(YELLOW, opacity=0.5),
                nodes[tort_idx][1].animate.set_color(YELLOW),
                Indicate(nodes[tort_idx][0], color=YELLOW),
                run_time=1.2
            )
            self.wait(1)
        else:
            self.wait(0.5)
            self.play(FadeOut(tortoise), FadeOut(hare), FadeOut(tortoise_label), FadeOut(hare_label))
            self.wait(0.5)

# Instructions:
# 1. Edit node_values and cycle_pos at the top as needed.
# 2. Run: manim -pql linked_list_cycle.py LinkedListCycleScene