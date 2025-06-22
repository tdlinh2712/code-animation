from manim import *

class Stack:
    def __init__(self):
        self.items = []
        self.visual_stack = VGroup()
        self.top_pointer = Arrow(RIGHT, LEFT, color=BLUE)
        self.top_label = Text("Top").next_to(self.top_pointer, RIGHT)
        self.pointer_group = VGroup(self.top_pointer, self.top_label)
        self.pointer_group.next_to(self.visual_stack, RIGHT)

    def push(self, item):
        self.items.append(item)
        box = Rectangle(width=2, height=1, color=WHITE)
        text = Text(str(item)).move_to(box.get_center())
        element = VGroup(box, text)
        
        if self.visual_stack:
            element.next_to(self.visual_stack, UP, buff=0)
        
        self.visual_stack.add(element)
        return self.get_push_animation(element)

    def pop(self):
        if not self.is_empty():
            self.items.pop()
            element_to_remove = self.visual_stack[-1]
            self.visual_stack.remove(element_to_remove)
            return self.get_pop_animation(element_to_remove)
        return None

    def get_pointer_animation(self):
        """Returns the animation to move the pointer to the correct target."""
        if self.visual_stack:
            target = self.visual_stack[-1] # The current top element
            return self.pointer_group.animate.next_to(target, RIGHT)
        else:
            # If stack is empty, point to where the stack would be
            return self.pointer_group.animate.next_to(self.visual_stack, RIGHT)

    def is_empty(self):
        return not self.items

    def get_push_animation(self, element):
        return [
            Create(element),
            self.visual_stack.animate.center(),
        ]

    def get_pop_animation(self, element):
        # Step 1: Fade out the element and center the stack
        anim1 = [
            FadeOut(element),
            self.visual_stack.animate.center(),
        ]
        return anim1