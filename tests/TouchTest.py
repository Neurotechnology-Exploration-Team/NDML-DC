import tkinter as tk
import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread
import time


class TouchTest(TestThread):
   

    def __init__(
        self,
        name,
        touch_path_1,
        touch_path_2,
        touch_path_3,
        touch_path_4,
        touch_path_5,
        touch_path_6,
        muscle_file

        

    ):
        """
        Initializes and creates the transition labels in the display window.

        :param name: The name of the test. Should be "<state 1> to <state 2>" for correct labeling.
        :param word_path_1: The path to the word of state 1
        :param word_path_2: The path to the word of state 2
        """
        super().__init__(name)

        self.touch_1 = tk.PhotoImage(file=touch_path_1)
        self.touch_2 = tk.PhotoImage(file=touch_path_2)
        self.touch_3 = tk.PhotoImage(file=touch_path_3)
        self.touch_4 = tk.PhotoImage(file=touch_path_4)
        self.touch_5 = tk.PhotoImage(file=touch_path_5)
        self.touch_6 = tk.PhotoImage(file=touch_path_6)
        # Derive labels from each half of the test name
        self.label_1 = "sand paper"
        self.label_2 = "artificial fur"
        self.label_3 = "cloth"
        self.label_4 = "smooth plastic"
        self.label_5 = "bumpy plastic"
        self.label_6 = "cardboard"

        self.firstWord = True
        self.current_word = None

        self.muscle_file = muscle_file

    def run_test(self):
        with open(self.muscle_file) as input:
            token = next(input)
            if token != None:
                if token == "sand paper":
                    LSL.start_label(self.label_1)
                    self.current_word = TestGUI.place_image(self.touch_1)
                elif token == "artificial fur":
                    LSL.start_label(self.label_2)
                    self.current_word = TestGUI.place_image(self.touch_2)
                elif token == "cloth":
                    LSL.start_label(self.label_3)
                    self.current_word = TestGUI.place_image(self.touch_3)
                elif token == "smooth plastic":
                    LSL.start_label(self.label_4)
                    self.current_word = TestGUI.place_image(self.touch_4)
                elif token == "bumpy plastic":
                    LSL.start_label(self.label_5)
                    self.current_word = TestGUI.place_image(self.touch_5)
                elif token == "cardboard":
                    LSL.start_label(self.label_6)
                    self.current_word = TestGUI.place_image(self.touch_6)

                time.sleep(5)
                if self.paused:
                    time.sleep(.1)
                # """
                # Main loop that runs and schedules the next iteration of the test
                # """
                # if self.iteration == config.ITERATIONS_PER_TEST:
                #     self.running = False

                # if self.running:
                #     # Display current word and start labeling based on flag
                #     if self.firstWord:
                #         LSL.start_label(self.label_1)
                #         self.current_word = TestGUI.place_image(self.word_1)
                #     else:
                #         LSL.start_label(self.label_2)
                #         self.current_word = TestGUI.place_image(self.word_2)

                #     self.playsound()  # Auditory stimulus

                #     def swap():
                #         """
                #         Function to swap the images for transition states.
                #         """
                #         self.firstWord = not self.firstWord
                #         self.run_test()

                #     self.test_job_id = TestGUI.display_window.after(config.TRANSITION_DURATION * 1000, swap)

                #     self.iteration += 1
                # else:
            # Stop test thread
            self.running = False
            TestGUI.destroy_current_element()

            LSL.stop_label()
            self.stop()
   