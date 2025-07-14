from manim import *
from src.dsa.linked_list import Node, LinkedList
import heapq

class HeapNode:
    def __init__(self, value, list_idx, node_idx):
        self.value = value
        self.list_idx = list_idx
        self.node_idx = node_idx
    def __lt__(self, other):
        return self.value < other.value

class MergeKSortedListsBlackBoxScene(Scene):
    def construct(self):
        # 1. Visualize input: 4 sorted linked lists
        lists_data = [
            [1, 5, 9],
            [2, 6, 10],
            [3, 7, 11],
            [4, 8, 12],
        ]
        n_lists = len(lists_data)
        linked_lists = []
        visual_groups = []
        y_start = 2
        for i, data in enumerate(lists_data):
            ll = LinkedList()
            for v in data:
                ll.insert(v)
            vg = ll.get_visual().copy().move_to(UP * (y_start - i*1.5))
            visual_groups.append(vg)
            linked_lists.append(ll)
            self.add(vg)
        self.wait(1)
        # 2. Collapse 4 linked lists into their heads, and put them in the box
        node_objs = [ll.nodes for ll in linked_lists]
        heads = [nodes[0] for nodes in node_objs]
        # Draw the black box (min heap) in the top right corner
        box = Rectangle(width=3, height=1, color=WHITE, fill_color=BLACK, fill_opacity=0.8)
        box_label = Text("Min Heap", font_size=28).move_to(box.get_center())
        box_group = VGroup(box, box_label)
        # Move box to top right
        box_group.move_to([config.frame_width/2 - 2, config.frame_height/2 - 1, 0])
        self.play(FadeIn(box_group))
        self.wait(0.5)
        # Animate heads moving into the box
        for i, head in enumerate(heads):
            head_cpy = head.copy()
            self.add(head_cpy)
            target_pos = box.get_center() + RIGHT * (i-1.5) * 0.7 + box_group.get_center() - box.get_center()
            self.play(head_cpy.animate.move_to(target_pos), run_time=0.6)
            self.remove(head_cpy)
        self.wait(0.5)
        # Clear the input linked lists
        self.play(*[FadeOut(vg) for vg in visual_groups], run_time=0.7)
        self.wait(0.2)
        # 3. Merging loop
        merged_ll = LinkedList()
        # Helper to arrange merged list to fit screen
        def get_merged_visual():
            n = len(merged_ll.nodes)
            max_width = config.frame_width * 0.9
            node_width = 1.0
            if n > 1:
                buff = min(0.4, max(0.2, (max_width - n * node_width) / (n - 1)))
            else:
                buff = 0.7
            return VGroup(*merged_ll.nodes).arrange(RIGHT, buff=buff).move_to(DOWN * 2.5)
        merged_visual = get_merged_visual()
        self.add(merged_visual)
        # Initialize heap with the head of each list
        heap = []
        for i in range(n_lists):
            if node_objs[i]:
                heapq.heappush(heap, HeapNode(node_objs[i][0].value, i, 0))
        total_nodes = sum(len(lst) for lst in lists_data)
        for round in range(total_nodes):
            # Draw the smallest node from the box
            hn = heapq.heappop(heap)
            chosen_node = node_objs[hn.list_idx][hn.node_idx]
            # Animate node popping out of the box
            node_cpy = chosen_node.copy()
            self.add(node_cpy)
            # Compute the target position for the new node in the merged list
            temp_nodes = merged_ll.nodes + [node_cpy]
            n = len(temp_nodes)
            max_width = config.frame_width * 0.9
            node_width = 1.0
            if n > 1:
                buff = min(0.4, max(0.2, (max_width - n * node_width) / (n - 1)))
            else:
                buff = 0.7
            temp_group = VGroup(*temp_nodes).arrange(RIGHT, buff=buff).move_to(DOWN * 2.5)
            target_pos = temp_group[-1].get_center()
            self.play(node_cpy.animate.move_to(target_pos), run_time=0.7)
            # Append to the result list
            merged_ll.insert(hn.value)
            # Remove the animated node copy and update merged list visual
            self.remove(node_cpy)
            merged_visual = get_merged_visual()
            self.play(Transform(merged_ll.visual_list, merged_visual), run_time=0.4)
            # If the drawn node has a next, show the previous node, highlight its next arrow, then put the next node into the box
            if hn.node_idx + 1 < len(node_objs[hn.list_idx]):
                prev_node = node_objs[hn.list_idx][hn.node_idx]
                next_node = node_objs[hn.list_idx][hn.node_idx+1]
                # Show prev_node and next_node together
                prev_node_cpy = prev_node.copy().move_to(UP * 0.5 + LEFT * 2)
                # Hide the built-in next_arrow to avoid double arrow
                # prev_node_cpy.set_next_visible(False)
                # Position arrow to the right of prev_node
                arrow = Arrow(prev_node_cpy.get_right(), prev_node_cpy.get_right() + RIGHT * 0.7, buff=0.1, color=YELLOW)
                next_node_cpy = next_node.copy().move_to(arrow.get_end() + RIGHT * 0.7)
                self.add(prev_node_cpy, next_node_cpy)
                # self.play(Indicate(arrow), run_time=0.5)
                self.wait(0.2)
                # Animate next_node moving into the box
                target_pos = box.get_center() + RIGHT * (len(heap)-1.5) * 0.7 + box_group.get_center() - box.get_center()
                self.play(next_node_cpy.animate.move_to(target_pos), run_time=0.5)
                self.remove(prev_node_cpy, next_node_cpy, arrow)
                next_hn = HeapNode(next_node.value, hn.list_idx, hn.node_idx+1)
                heapq.heappush(heap, next_hn)
            self.wait(0.2)
        self.wait(2) 