import sys
import os
import datetime

from croniter import croniter


def main():
    if len(sys.argv) < 2:
        raise ValueError("No cron expression was provided")
    if len(sys.argv) < 3:
        raise ValueError("No checkpoints directory provided")
    cron_expression = sys.argv[1]
    if not croniter.is_valid(cron_expression):
        raise ValueError(f"Invalid cron expression '{cron_expression}'")
    # Find last date it should have run
    should_have_run_date = croniter(cron_expression).get_prev(datetime.datetime).date()
    print(f"Should have run at {should_have_run_date}")
    # Check if the schedule has been kept by comparing expected date with latest checkpoint date
    #   (could have just looked for any checkpoint at or after expected date,
    #    but going through everything for logging purposes)
    latest_checkpoint_date = find_latest_checkpoint_date(directory=sys.argv[2])
    if latest_checkpoint_date is not None and latest_checkpoint_date >= should_have_run_date:
        print("Looking good!")
        sys.exit(1)
        return
    print("Looks like you're behind schedule...")
    # Check if optional script was provided
    if len(sys.argv) > 3:
        # Treat rest of cli args for this script as python cli args
        script = " ".join(sys.argv[3:])
        print(f"Running '{script}'")
        os.system(f"python {script}")
        return
    sys.exit(0)


# Look through checkpoint files and find the date of the latest checkpoint
def find_latest_checkpoint_date(directory):
    if not os.path.isdir(directory):
        print(f"Warning: the given directory '{directory}' does not exist, assuming no checkpoints exist")
        return None
    latest_checkpoint = None
    for filename in os.listdir(directory):
        try:
            checkpoint = datetime.date.fromisoformat(filename)
            if latest_checkpoint is None or checkpoint >= latest_checkpoint:
                latest_checkpoint = checkpoint
        except ValueError:
            print(f"Warning: the file '{filename}' is not a valid checkpoint")
    if latest_checkpoint is None:
        print(f"No checkpoints found in directory '{directory}'")
        return None
    print(f"Latest checkpoint was at {latest_checkpoint}")
    return latest_checkpoint


if __name__ == '__main__':
    main()
