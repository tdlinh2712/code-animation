from manim import *

class Node(VGroup):
    def __init__(self, value, show_prev=False):
        super().__init__()
        self.value = value
        self.show_prev = show_prev
        self.box = Circle(radius=0.5, color=WHITE)
        self.text = Text(str(value), font_size=28).move_to(self.box.get_center())
        self.add(self.box, self.text)
        self.next_arrow = Arrow(self.box.get_right(), self.box.get_right() + RIGHT * 0.8, buff=0.1, color=YELLOW)
        self.add(self.next_arrow)
        if show_prev:
            self.prev_arrow = Arrow(self.box.get_left(), self.box.get_left() + LEFT * 0.8, buff=0.1, color=BLUE)
            self.add(self.prev_arrow)
        else:
            self.prev_arrow = None
    def set_next_visible(self, visible=True):
        self.next_arrow.set_opacity(1 if visible else 0)
    def set_prev_visible(self, visible=True):
        if self.prev_arrow:
            self.prev_arrow.set_opacity(1 if visible else 0)

class LinkedList:
    def __init__(self, show_prev=False):
        self.head = None
        self.nodes = []  # List of Node VGroups
        self.visual_list = VGroup()
        self.show_prev = show_prev

    def insert(self, value, index=None):
        """Insert value at index (default: end). Returns animations."""
        node = Node(value, show_prev=self.show_prev)
        if index is None or index > len(self.nodes):
            index = len(self.nodes)
        self.nodes.insert(index, node)
        # Arrange nodes visually
        # Dynamically adjust spacing to fit all nodes within the screen width
        max_width = config["frame_width"] * 0.9  # leave some margin
        node_width = 1.0  # Approximate width per node (circle + arrow + buffer)
        n = len(self.nodes)
        if n > 1:
            # Calculate buffer so that total width fits max_width
            buff = min(0.4, max(0.2, (max_width - n * node_width) / (n - 1)))
        else:
            buff = 0.7
        self.visual_list = VGroup(*self.nodes).arrange(RIGHT, buff=buff)
        # Update arrows
        for i, n in enumerate(self.nodes):
            n.set_next_visible(i < len(self.nodes) - 1)
            if self.show_prev:
                n.set_prev_visible(i > 0)
        return [Create(node), self.visual_list.animate.center()]

    def delete(self, index):
        """Delete node at index. Returns animations."""
        if 0 <= index < len(self.nodes):
            node = self.nodes.pop(index)
            self.visual_list = VGroup(*self.nodes).arrange(RIGHT, buff=0.7)
            # Update arrows
            for i, n in enumerate(self.nodes):
                n.set_next_visible(i < len(self.nodes) - 1)
                if self.show_prev:
                    n.set_prev_visible(i > 0)
            return [FadeOut(node), self.visual_list.animate.center()]
        return []
    
    def get_visual(self):
        return self.visual_list 