import random
from time import sleep
import os 
import config
from LSL import LSL
from tests.TestGUI import TestGUI
from tests.TestThread import TestThread


class BlinkTest(TestThread):
    """
    The Blink test that extends the TestThread class.

    Audio only
    """

    def __init__(self, name):
        super().__init__(name)
        test_path = os.path.join(config.SAVED_DATA_PATH, TestGUI.participant_ID, TestGUI.session_ID, self.name)
        self.current_path = os.path.join(str(test_path), f"trial_{str(self.trial_number).zfill(2)}")
        os.makedirs(self.current_path, exist_ok=True)
    def run_test(self):
        """
        Main loop that runs and schedules the next iteration of the test
        """
        if self.iteration == config.ITERATIONS_PER_TEST:
            self.running = False

        if self.running:
            # Blink & setup next interval
            LSL.start_label(self.name)
            self.playsound()
            self.iteration += 1

            interval = random.randint(config.BLINK_MIN_INTERVAL * 1000, config.BLINK_MAX_INTERVAL * 1000)
            sleep(config.PAUSE_AFTER_TEST)  # Wait extra after blinking
            LSL.stop_label()

            self.test_job_id = TestGUI.display_window.after(interval, self.run_test)
        else:
            # Stop test thread
            self.running = False

            LSL.stop_label()
            self.stop()
