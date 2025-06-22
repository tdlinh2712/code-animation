from manim import *
from dsa.linked_list import LinkedList, Node

class ReverseLinkedListScene(MovingCameraScene):
    def construct(self):
        ll = LinkedList()
        # Create initial list
        for i in range(1, 4):
            self.play(*ll.insert(i))
            self.wait(0.2)
        self.play(ll.get_visual().animate.center())
        self.wait(0.5)
        self.play(*ll.insert("null"))

        # Create a standalone 'null' node to the left of the head
        null_node = Node("null")
        null_node.move_to(ll.nodes[0].get_left() + LEFT * 1.5)
        self.add(null_node)
        null_node.set_next_visible(False)

        # Set up pointers
        prev_ptr = self.make_pointer("prev", null_node.box, direction=DOWN, color=BLUE)
        cur_ptr = self.make_pointer("cur", ll.nodes[0].box, direction=UP, color=YELLOW)
        next_ptr = self.make_pointer("next", ll.nodes[1].box, direction=UP, color=GREEN)
        self.add(prev_ptr, cur_ptr, next_ptr)

        prev = null_node
        cur_idx = 0
        while cur_idx < len(ll.nodes) - 1:
            cur = ll.nodes[cur_idx]
            next_node = ll.nodes[cur_idx+1] if cur_idx+1 < len(ll.nodes) else None

            # Animate pointers
            self.play(cur_ptr.animate.next_to(cur, UP, buff=0.5))
            if prev is not None:
                self.play(prev_ptr.animate.next_to(prev.box, DOWN, buff=0.5))
            if next_node:
                self.play(next_ptr.animate.next_to(next_node.box, UP, buff=0.5))
            else:
                self.play(next_ptr.animate.next_to(cur.box, RIGHT, buff=0.5))
            self.wait(0.3)

            # Reverse the arrow for current node
            self.play(cur.next_arrow.animate.put_start_and_end_on(cur.box.get_left(), prev.box.get_right() if prev else(cur.box.get_left() + LEFT * 0.8 )))
            self.wait(0.2)

            # Move prev and cur forward
            prev = cur
            cur_idx += 1

        # Final pointer positions
        cur = ll.nodes[cur_idx]
        self.play(cur_ptr.animate.next_to(cur.box, UP, buff=0.5))
        self.play(prev_ptr.animate.next_to(prev.box, DOWN, buff=0.5))
        self.wait(1)

    def make_pointer(self, label, node, direction=UP, color=YELLOW):
        arrow = Arrow(ORIGIN, direction, buff=0, color=color).scale(0.5)
        group = VGroup(arrow, Text(label, font_size=28, color=color).next_to(arrow, direction, buff=0.1))
        group.next_to(node, direction, buff=0.5)
        return group 