from manim import *
from dsa.linked_list import LinkedList

# === Editable Input ===
node_values = [3, 2, 0, -4, 5, 1]  # List of node values
cycle_pos = 2  # Index to which the last node points (set to None for no cycle)

def pointer_move_anims(pointer, label, from_idx, to_idx, nodes, cycle_path=None, is_cycle_move=False, label_offset=UP*0.1, pointer_offset=UP*0.3):
    """
    Returns a list of animations for moving a pointer and its label.
    If is_cycle_move is True, moves along the cycle_path.
    Otherwise, moves directly to the target node.
    """
    if is_cycle_move and cycle_path is not None:
        return [
            MoveAlongPath(pointer, cycle_path),
            MoveAlongPath(label, cycle_path)
        ]
    else:
        return [
            pointer.animate.move_to(nodes[to_idx].box.get_top() + pointer_offset),
            label.animate.next_to(nodes[to_idx].box.get_top() + pointer_offset, UP, buff=0.1)
        ]

class LinkedListCycleScene(Scene):
    def construct(self):
        # Create the linked list visually
        ll = LinkedList()
        anims = []
        for v in node_values:
            anims += ll.insert(v)
        self.play(*anims)
        self.wait(0.5)
        nodes = ll.nodes
        self.play(ll.get_visual().animate.center())
        self.wait(0.5)

        # Draw cycle arrow if needed
        cycle_arrow = None
        cycle_path = None
        if cycle_pos is not None and 0 <= cycle_pos < len(nodes):
            start = nodes[-1].box.get_right()
            end = nodes[cycle_pos].box.get_bottom()
            cycle_arrow = CurvedArrow(start, end, angle=-PI/2, color=YELLOW)
            cycle_path = ArcBetweenPoints(start, end, angle=-PI/2)
            self.play(Create(cycle_arrow))
            self.wait(0.5)

        # Tortoise and Hare pointers
        tortoise = Dot(nodes[0].box.get_top() + UP*0.3, color=GREEN).scale(1.2)
        hare = Dot(nodes[0].box.get_top() + UP*0.7, color=RED).scale(1.2)
        slow_label = Text("slow", font_size=24, color=GREEN).next_to(tortoise, UP, buff=0.1)
        fast_label = Text("fast", font_size=24, color=RED).next_to(hare, UP, buff=0.1)
        self.play(FadeIn(tortoise), FadeIn(hare), FadeIn(slow_label), FadeIn(fast_label))
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
            # Move hare by 2, but track intermediate step
            hare_path = []
            temp_hare = hare_idx
            for _ in range(2):
                if temp_hare+1 < len(nodes):
                    temp_hare += 1
                    hare_path.append(temp_hare)
                elif cycle_pos is not None:
                    temp_hare = cycle_pos
                    hare_path.append(temp_hare)
                else:
                    temp_hare = None
                    break
            next_hare = temp_hare
            if next_tort is None or next_hare is None:
                break
            # Animate tortoise
            tortoise_cycle_move = (tort_idx+1 >= len(nodes) and next_tort == cycle_pos and cycle_path is not None)
            tortoise_anims = pointer_move_anims(
                tortoise, slow_label, tort_idx, next_tort, nodes,
                cycle_path=cycle_path, is_cycle_move=tortoise_cycle_move,
                label_offset=UP*0.1, pointer_offset=UP*0.3
            )
            # Animate hare (handle 2-step move with possible cycle crossing)
            if len(hare_path) == 2 and hare_path[0] == len(nodes)-1 and hare_path[1] == cycle_pos and cycle_path is not None:
                # Step 1: move to last node
                hare_anims = pointer_move_anims(
                    hare, fast_label, hare_idx, hare_path[0], nodes,
                    cycle_path=None, is_cycle_move=False,
                    label_offset=UP*0.1, pointer_offset=UP*0.7
                )
                self.play(*tortoise_anims, *hare_anims, run_time=0.4)
                # Step 2: move along cycle path
                hare_anims = pointer_move_anims(
                    hare, fast_label, hare_path[0], hare_path[1], nodes,
                    cycle_path=cycle_path, is_cycle_move=True,
                    label_offset=UP*0.1, pointer_offset=UP*0.7
                )
                self.play(*hare_anims, run_time=0.4)
            else:
                hare_cycle_move = (hare_idx+2 >= len(nodes) and next_hare == cycle_pos and cycle_path is not None)
                hare_anims = pointer_move_anims(
                    hare, fast_label, hare_idx, next_hare, nodes,
                    cycle_path=cycle_path, is_cycle_move=hare_cycle_move,
                    label_offset=UP*0.1, pointer_offset=UP*0.7
                )
                self.play(*tortoise_anims, *hare_anims, run_time=0.8)
            tort_idx = next_tort
            hare_idx = next_hare
            steps += 1
            if tort_idx == hare_idx:
                met = True
                break
        if met:
            # Highlight meeting node
            self.play(
                nodes[tort_idx].box.animate.set_fill(YELLOW, opacity=0.5),
                nodes[tort_idx].text.animate.set_color(YELLOW),
                Indicate(nodes[tort_idx].box, color=YELLOW),
                run_time=1.2
            )
            self.wait(1)
        else:
            self.wait(0.5)
            self.play(FadeOut(tortoise), FadeOut(hare), FadeOut(slow_label), FadeOut(fast_label))
            self.wait(0.5)

# Instructions:
# 1. Edit node_values and cycle_pos at the top as needed.
# 2. Run: manim -pql src/linked_list_cycle.py LinkedListCycleScene 