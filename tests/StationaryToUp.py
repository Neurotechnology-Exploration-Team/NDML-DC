import tkinter as tk
from LSL import LSL
import os

from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class StationaryToUp(TestThread):
    """
    The Stationary Float To Float Up test that extends the TestThread class.

    Explain to the subject they will be imagining themselves floating still and then floating up, alternating based on audiovisual stimulus directing the correct action.
    They will be switching between still and floating up state when a cue is presented.
    TODO The subject will know when to switch states by looking for two audiovisual cues denoting each action.
    TODO Label for entire transition state?
    """

    def __init__(self):
        """
        Initializes and creates the transition labels in the display window.
        """
        super().__init__(transition=True)
        action_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'Up.png')
        stop_image_directory = os.path.join(os.path.dirname(__file__), '..', 'assets', 'stop white.png')

        self.action_image = tk.PhotoImage(file=action_image_directory)
        self.stop_image = tk.PhotoImage(file=stop_image_directory)

        self.firstImage = True
        self.current_label = None

    def start_iteration(self):
        """
        Creates and displays a new label for each iteration.
        """
        super().start_iteration()

        if self.firstImage:
            LSL.start_label("Stop")
            self.current_label = tk.Label(TestGUI.display_window, image=self.stop_image, borderwidth=0)
        else:
            LSL.start_label("Up")
            self.current_label = tk.Label(TestGUI.display_window, image=self.action_image, borderwidth=0)

        self.firstImage = not self.firstImage
        self.current_label.place(relx=0.5, rely=0.5, anchor='center')

    def stop_iteration(self):
        """
        Destroys the label after each iteration.
        """
        super().stop_iteration()

        self.current_label.destroy()
