from scheduling import MyScheduler
import schedule
import time

run_all_time = True # False to run every tuesday at 9:00 AM

# instance of the scheduler
scheduler = MyScheduler(run_all_time)

while True:
    # Run the scheduled jobs
    schedule.run_pending()
    time.sleep(1)
