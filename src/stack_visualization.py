from manim import *
from dsa.stack import *

class StackScene(MovingCameraScene):
    def construct(self):
        stack = Stack()
        
        # Initial state
        self.play(
            Create(stack.visual_stack),
            Create(stack.pointer_group),
            stack.get_pointer_animation()
        )
        self.wait(1)

        # Push operations
        for i in range(1, 4):
            animation = stack.push(i)
            self.play(*animation)
            self.play(stack.get_pointer_animation(), run_time=0.5)
            self.wait(1)

        # Pop operations
        for _ in range(2):
            animation = stack.pop()
            # Play the first part of the animation (fade out and center)
            self.play(*animation)
            # Play the second part (move the pointer)
            self.play(stack.get_pointer_animation(), run_time=0.5)
            self.wait(1)
        
        # Push again
        animation = stack.push(4)
        self.play(*animation)
        self.play(stack.get_pointer_animation(), run_time=0.5)
        self.wait(1) 