import tkinter as tk

import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class WarmUpTest(TestThread):
   

    def __init__(self, name, image_path_1, image_path_2,image_path_3,image_path_4,image_path_5):
        """
        Initializes and creates the transition labels in the display window.

        :param name: The name of the test. Should be "<state 1> to <state 2>" for correct labeling.
        :param image_path_1: The path to the image of state 1
        :param image_path_2: The path to the image of state 2
        """
        super().__init__(name)

        self.image_1 = tk.PhotoImage(file=image_path_1)
        self.image_2 = tk.PhotoImage(file=image_path_2)
        self.image_3 = tk.PhotoImage(file=image_path_3)
        self.image_4 = tk.PhotoImage(file=image_path_4)
        self.image_5 = tk.PhotoImage(file=image_path_5)

        # Derive labels from each half of the test name
        self.label_1 = "center"
        self.label_2 = "up arrow"
        self.label_3 = "down arrow"
        self.label_4 = "left arrow"
        self.label_5 = "right arrow"

        self.firstImage = True
        self.current_image = None

    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_TEST:
            self.running = False

        if self.running:
            # Display current image and start labeling based on flag
            if self.firstImage:
                LSL.start_label(self.label_1)
                self.current_image = TestGUI.place_image(self.image_1)
            else:
                LSL.start_label(self.label_2)
                self.current_image = TestGUI.place_image(self.image_2)

            self.playsound()  # Auditory stimulus

            def swap():
                """
                Function to swap the images for transition states.
                """
                self.firstImage = not self.firstImage
                self.run_test()

            self.test_job_id = TestGUI.display_window.after(config.TRANSITION_DURATION * 1000, swap)

            self.iteration += 1
        else:
            # Stop test thread
            self.running = False
            TestGUI.destroy_current_element()

            LSL.stop_label()
            self.stop()
