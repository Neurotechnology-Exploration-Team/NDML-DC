import tkinter as tk
import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread
import time

class SmellTest(TestThread):
   

    def __init__(
        self,
        name,
        smell_path_1,
        smell_path_2,
        smell_path_3,
        smell_path_4,
        smell_path_5,
        smell_path_6,
        smell_path_7,
        smell_path_8,
        smell_path_9,
        smell_path_10,
        smell_path_11,
        smell_file,

    ):
        """
        Initializes and creates the transition labels in the display window.

        :param name: The name of the test. Should be "<state 1> to <state 2>" for correct labeling.
        :param smell_path_1: The path to the smell of state 1
        :param smell_path_2: The path to the smell of state 2
        """
        super().__init__(name)

        self.smell_1 = tk.PhotoImage(file=smell_path_1)
        self.smell_2 = tk.PhotoImage(file=smell_path_2)
        self.smell_3 = tk.PhotoImage(file=smell_path_3)
        self.smell_4 = tk.PhotoImage(file=smell_path_4)
        self.smell_5 = tk.PhotoImage(file=smell_path_5)
        self.smell_6 = tk.PhotoImage(file=smell_path_6)
        self.smell_7 = tk.PhotoImage(file=smell_path_7)
        self.smell_8 = tk.PhotoImage(file=smell_path_8)
        self.smell_9 = tk.PhotoImage(file=smell_path_9)
        self.smell_10 = tk.PhotoImage(file=smell_path_10)
        self.smell_11 = tk.PhotoImage(file=smell_path_11)
        
        # Derive labels from each half of the test name
        self.label_1 = "blank"
        self.label_2 = "lemon"
        self.label_3 = "clove"
        self.label_4 = "rose"
        self.label_5 = "coffee"
        self.label_6 = "eucalyptus"
        self.label_7 = "cinnamon"
        self.label_8 = "strawberry"
        self.label_9 = "peppermint"
        self.label_10 = "banana"
        self.label_11 = "leather"

        self.firstsmell = True
        self.current_smell = None

        self.smell_file = smell_file

    def run_test(self):
        with open(self.smell_file) as input:
            token = next(input)
            if token != None:
                if token == "blank":
                    LSL.start_label(self.label_1)
                    self.current_label = TestGUI.place_image(self.smell_1)
                elif token == "lemon":
                    LSL.start_label(self.label_2)
                    self.current_label = TestGUI.place_image(self.smell_2)
                elif token == "clove":
                    LSL.start_label(self.label_3)
                    self.current_label = TestGUI.place_image(self.smell_3)
                elif token == "rose":
                    LSL.start_label(self.label_4)
                    self.current_label = TestGUI.place_image(self.smell_4)
                elif token == "coffee":
                    LSL.start_label(self.label_5)
                    self.current_label = TestGUI.place_image(self.smell_5)
                elif token == "eucalyptus":
                    LSL.start_label(self.label_6)
                    self.current_label = TestGUI.place_image(self.smell_6)
                if token == "cinnamon":
                    LSL.start_label(self.label_1)
                    self.current_label = TestGUI.place_image(self.smell_7)
                elif token == "strawberry":
                    LSL.start_label(self.label_2)
                    self.current_label = TestGUI.place_image(self.smell_8)
                elif token == "peppermint":
                    LSL.start_label(self.label_3)
                    self.current_label = TestGUI.place_image(self.smell_9)
                elif token == "banana":
                    LSL.start_label(self.label_4)
                    self.current_label = TestGUI.place_image(self.smell_10)
                elif token == "leather":
                    LSL.start_label(self.label_5)
                    self.current_label = TestGUI.place_image(self.smell_11)

                time.sleep(5)
                if self.paused:
                    time.sleep(.1)

            # Stop test thread
            self.running = False
            TestGUI.destroy_current_element()

            LSL.stop_label()
            self.stop()
   