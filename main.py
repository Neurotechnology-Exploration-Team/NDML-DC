import importlib
import os

import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class DataCollectorApp:
    """
    A collection of functions to initialize the GUI, tests, and setup test logic.
    """

    @staticmethod
    def run_test(current_test: str, test_type: str) -> TestThread:
        """
        Runs the specified test in a separate thread and collects data.
        :param current_test: Name of the test being run
        :param test_type: Type of the test being run: Blink, Constant, or Transition
        """
        # Dynamically import the test from tests package & construct it w/ no parameters
        class_name = f"{test_type}Test"
        test_class = getattr(importlib.import_module(f"tests.{class_name}"), class_name)
        # Possible optimization of test selection, try if seeing input delays
        if test_type == "Transition":
            assets = config.TESTS[test_type]
            test = test_class(
                current_test,
                os.path.join(".", "assets", assets[0]),
                os.path.join(".", "assets", assets[1]),
            )
        elif test_type == "Constant":
            test = test_class(current_test)
        elif test_type == "Blink":
            test = test_class(current_test)
        elif test_type == "WarmUp":
            assets = config.TESTS[test_type]
            test = test_class(
                current_test,
                os.path.join(".", "assets", assets["Center"] ),
                os.path.join(".", "assets", assets["Up"]),
                os.path.join(".", "assets", assets["Down"]),
                os.path.join(".", "assets", assets["Left"]),
                os.path.join(".", "assets", assets["Right"]),
                os.path.join(".", "tests", "random_order_files", assets["ArrowFile"]),
            )
        elif test_type == "Muscle":
            assets = config.TESTS[test_type]
            test = test_class(
                current_test,
                os.path.join(".", "assets", assets["Blank"]),
                os.path.join(".", "assets", assets["right arm"]),
                os.path.join(".", "assets", assets["left arm"]),
                os.path.join(".", "assets", assets["right leg"]),
                os.path.join(".", "assets", assets["left leg"]),
                os.path.join(".", "assets", assets["torso"]),
            )
        elif test_type == "Color":
            assets = config.TESTS[test_type]
            test = test_class(
                current_test,
                os.path.join(".", "assets", assets[0]),
                os.path.join(".", "assets", assets[1]),
                os.path.join(".", "assets", assets[2]),
                os.path.join(".", "assets", assets[3]),
                os.path.join(".", "assets", assets[4]),
            )
        elif test_type == "Hearing":
            assets = config.TESTS[test_type]
            test = test_class(current_test)
        elif test_type == "Touch":
            test = test_class(current_test)
        elif test_type == "Smell":
            test = test_class(current_test)
        elif test_type == "Speech":
            assets = config.TESTS[test_type]
            test = test_class(
                current_test,
                os.path.join(".", "assets", assets[0]),
            )
        else:
            # Invalid test type
            raise ValueError(f"Unknown test type: {test_type}")

        test.start()  # Start test thread
        return test

    @staticmethod
    def run():
        """
        Main function for adding buttons that run tests to the GUI and initializing the LSL streams & GUI.
        """
        # Initialize streams & GUI
        LSL.init_lsl_stream()
        TestGUI.init_gui()

        # Add each test button to the GUI that calls the run_test method above w/ the test name and type
        for test_type in config.TESTS.keys():
            # Add button to test
            TestGUI.add_test(
                test_type,
                lambda n=test_type, t=test_type: DataCollectorApp.run_test(n, t),
            )

        TestGUI.control_window.mainloop()


if __name__ == "__main__":
    DataCollectorApp.run()
