import tkinter as tk
import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread
import time

class SpeechTest(TestThread):
   

    def __init__(
        self,
        name,
        word_path_1,
        word_path_2,
        word_path_3,
        word_path_4,
        word_path_5,
        word_path_6,
        word_path_7,
        word_path_8,
        word_path_9,
        word_path_10,
        word_path_11,
        word_path_12,
        word_path_13,
        word_path_14,
        word_path_15,
        word_path_16,
        word_path_17,
        muscle_file,

    ):
        """
        Initializes and creates the transition labels in the display window.

        :param name: The name of the test. Should be "<state 1> to <state 2>" for correct labeling.
        :param word_path_1: The path to the word of state 1
        :param word_path_2: The path to the word of state 2
        """
        super().__init__(name)

        self.word_1 = tk.PhotoImage(file=word_path_1)
        self.word_2 = tk.PhotoImage(file=word_path_2)
        self.word_3 = tk.PhotoImage(file=word_path_3)
        self.word_4 = tk.PhotoImage(file=word_path_4)
        self.word_5 = tk.PhotoImage(file=word_path_5)
        self.word_6 = tk.PhotoImage(file=word_path_6)
        self.word_1 = tk.PhotoImage(file=word_path_7)
        self.word_2 = tk.PhotoImage(file=word_path_8)
        self.word_3 = tk.PhotoImage(file=word_path_9)
        self.word_4 = tk.PhotoImage(file=word_path_10)
        self.word_5 = tk.PhotoImage(file=word_path_11)
        self.word_6 = tk.PhotoImage(file=word_path_12)
        self.word_1 = tk.PhotoImage(file=word_path_13)
        self.word_2 = tk.PhotoImage(file=word_path_14)
        self.word_3 = tk.PhotoImage(file=word_path_15)
        self.word_4 = tk.PhotoImage(file=word_path_16)
        self.word_5 = tk.PhotoImage(file=word_path_17)

        # Derive labels from each half of the test name
        self.label_1 = "blank"
        self.label_2 = "left arm"
        self.label_3 = "right arm"
        self.label_4 = "left leg"
        self.label_5 = "right leg"
        self.label_6 = "torso"
        self.label_7 = "blank"
        self.label_8 = "left arm"
        self.label_9 = "right arm"
        self.label_10 = "left leg"
        self.label_11 = "right leg"
        self.label_12 = "torso"
        self.label_13 = "blank"
        self.label_14 = "left arm"
        self.label_15 = "right arm"
        self.label_16 = "left leg"
        self.label_17 = "right leg"

        self.firstWord = True
        self.current_word = None

        self.muscle_file = muscle_file

    def run_test(self):
        with open(self.muscle_file) as input:
            token = next(input)
            if token != None:
                if token == "blank":
                    LSL.start_label(self.label_1)
                    self.current_word = TestGUI.place_image(self.word_1)
                elif token == "left arm":
                    LSL.start_label(self.label_2)
                    self.current_word = TestGUI.place_image(self.word_2)
                elif token == "right arm":
                    LSL.start_label(self.label_3)
                    self.current_word = TestGUI.place_image(self.word_3)
                elif token == "left leg":
                    LSL.start_label(self.label_4)
                    self.current_word = TestGUI.place_image(self.word_4)
                elif token == "right leg":
                    LSL.start_label(self.label_5)
                    self.current_word = TestGUI.place_image(self.word_5)
                elif token == "torso":
                    LSL.start_label(self.label_6)
                    self.current_word = TestGUI.place_image(self.word_6)
                if token == "blank":
                    LSL.start_label(self.label_1)
                    self.current_word = TestGUI.place_image(self.word_7)
                elif token == "left arm":
                    LSL.start_label(self.label_2)
                    self.current_word = TestGUI.place_image(self.word_8)
                elif token == "right arm":
                    LSL.start_label(self.label_3)
                    self.current_word = TestGUI.place_image(self.word_9)
                elif token == "left leg":
                    LSL.start_label(self.label_4)
                    self.current_word = TestGUI.place_image(self.word_10)
                elif token == "right leg":
                    LSL.start_label(self.label_5)
                    self.current_word = TestGUI.place_image(self.word_11)
                elif token == "torso":
                    LSL.start_label(self.label_6)
                    self.current_word = TestGUI.place_image(self.word_12)
                if token == "blank":
                    LSL.start_label(self.label_1)
                    self.current_word = TestGUI.place_image(self.word_13)
                elif token == "left arm":
                    LSL.start_label(self.label_2)
                    self.current_word = TestGUI.place_image(self.word_14)
                elif token == "right arm":
                    LSL.start_label(self.label_3)
                    self.current_word = TestGUI.place_image(self.word_15)
                elif token == "left leg":
                    LSL.start_label(self.label_4)
                    self.current_word = TestGUI.place_image(self.word_16)
                elif token == "right leg":
                    LSL.start_label(self.label_5)
                    self.current_word = TestGUI.place_image(self.word_17)

                time.sleep(5)

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
   