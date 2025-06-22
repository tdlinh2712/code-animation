from manim import *
import os
from dsa.stack import Stack

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
        box = Rectangle(width=1, height=1, color=WHITE)
        text = Text(str(item)).move_to(box.get_center())
        element = VGroup(box, text)
        
        if self.visual_stack:
            element.next_to(self.visual_stack, UP, buff=0)
        
        self.visual_stack.add(element)
        return self.get_push_animation(element)

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            element_to_remove = self.visual_stack[-1]
            self.visual_stack.remove(element_to_remove)
            return self.get_pop_animation(element_to_remove)
        return None

    def top(self):
        if not self.is_empty():
            return self.items[-1]
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

class ValidParenthesesScene(MovingCameraScene):
    def construct(self):
        input_str = os.environ.get("INPUT_STR", "([{}])")
        # Create a VGroup of Text objects for each character
        char_mobs = VGroup(*[Text(c, font_size=48) for c in input_str])
        char_mobs.arrange(RIGHT, buff=0.2)
        char_mobs.to_edge(UP)
        self.add(char_mobs)

        # Create a pointer (triangle) under the first character
        pointer = Triangle(color=YELLOW, fill_opacity=1).scale(0.2)
        pointer.next_to(char_mobs[0], DOWN, buff=0.1)
        self.add(pointer)

        # Show empty stack for context
        stack = Stack()
        self.play(Create(stack.visual_stack), Create(stack.pointer_group), stack.get_pointer_animation())
        self.wait(0.5)

        pairs = {'(': ')', '[': ']', '{': '}'}
        error_found = False

        for i, c in enumerate(input_str):
            # Move pointer to current character
            self.play(pointer.animate.next_to(char_mobs[i], DOWN, buff=0.1), run_time=0.4)
            self.wait(0.2)
            if c in pairs:
                # Push to stack
                anims = stack.push(c)
                self.play(*anims)
                self.play(stack.get_pointer_animation(), run_time=0.3)
            else:
                # Closing bracket
                if stack.is_empty():
                    char_mobs[i].set_color(RED)
                    error_found = True
                    break
                top = stack.top()
                if pairs.get(top, None) != c:
                    char_mobs[i].set_color(RED)
                    error_found = True
                    break
                # Pop and mark as green
                char_mobs[i].set_color(PURE_GREEN)
                anims = stack.pop()
                self.play(*anims)
                self.play(stack.get_pointer_animation(), run_time=0.3)
            self.wait(0.3)

        # If error not found, check if stack is empty at the end
        if not error_found:
            if not stack.is_empty():
                # Highlight last unmatched opening
                for j in range(len(input_str)-1, -1, -1):
                    if char_mobs[j].color != PURE_GREEN:
                        char_mobs[j].set_color(RED)
                        break
            else:
                # Optionally, highlight all as green if valid
                pass
        self.wait(1) 