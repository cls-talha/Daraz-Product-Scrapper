import schedule
import time

from bot import bot


class MyScheduler:
    def __init__(self, run_all_time=False):
        if run_all_time:
            # Run the function immediately
            self.scheduled_function()

        if not run_all_time:
            # Schedule the job to run every Tuesday at 9:00 AM
            schedule.every().tuesday.at("09:00").do(self.scheduled_function)

    def scheduled_function(self):
        print("[INFO] Running the scheduled function!")
        bot()

    def unscheduled_function(self):
        print("[INFO] Running the unscheduled function!")
        bot()


