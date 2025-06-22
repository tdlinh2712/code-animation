from manim import *
from dsa.linked_list import LinkedList

class LinkedListScene(MovingCameraScene):
    def construct(self):
        ll = LinkedList()
        # Initial empty list
        self.play(Create(ll.get_visual()))
        self.wait(0.5)

        # Insert elements
        for i in range(1, 6):
            anims = ll.insert(i)
            self.play(*anims)
            self.wait(0.5)

        # Traverse
        # Need to play each animation indivisually so the color is applied correctly
        for node in ll.nodes:
            self.play(node.box.animate.set_color(PURE_GREEN))
            self.play(Wait(0.5))
            self.play(node.box.animate.set_color(WHITE))
        self.wait(1) 