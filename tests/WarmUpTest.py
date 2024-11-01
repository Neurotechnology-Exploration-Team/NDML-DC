import tkinter as tk
import os 
import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread
import time


class WarmUpTest(TestThread):

    def __init__(
        self,
        name,
        image_path_1,
        image_path_2,
        image_path_3,
        image_path_4,
        image_path_5,
        arrow_file=None,
    ):
        """
        Initializes and creates the transition labels in the display window.

        :param name: The name of the test. Should be "<state 1> to <state 2>" for correct labeling.
        :param image_path_1: The path to the image of state 1
        :param image_path_2: The path to the image of state 2
        """
        super().__init__(name)
        test_path = os.path.join(config.SAVED_DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)

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

        self.arrow_file = arrow_file

    def run_test(self):
        with open(self.arrow_file) as input:
            while True:
                try:
                    token = next(input)
                    token = token.strip()
                    print(token)
                    print(type(token))
                    if token != None:
                        if token == "Center":
                            LSL.start_label(self.label_1)
                            self.current_image = TestGUI.place_image(self.image_1)
                        elif token == "Up":
                            LSL.start_label(self.label_2)
                            self.current_image = TestGUI.place_image(self.image_2)
                        elif token == "Down":
                            LSL.start_label(self.label_3)
                            self.current_image = TestGUI.place_image(self.image_3)
                        elif token == "Left":
                            LSL.start_label(self.label_4)
                            self.current_image = TestGUI.place_image(self.image_4)
                        elif token == "Right":
                            LSL.start_label(self.label_5)
                            self.current_image = TestGUI.place_image(self.image_5)
            
                        time.sleep(5)
                    else: 
                        break
                except StopIteration:
                    break
            self.running = False
            TestGUI.destroy_current_element()

            LSL.stop_label()
            self.stop()
