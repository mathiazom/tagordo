import os
import datetime
from croniter import croniter
import typer
import logging

logging.basicConfig(level=logging.INFO)

app = typer.Typer()


@app.command()
def main(cron_expression: str, checkpoints_dir: str):
    """
    Check if checkpoints in CHECKPOINTS_DIR are up-to-date with a given CRON_EXPRESSION schedule.
    """
    if not croniter.is_valid(cron_expression):
        raise ValueError(f"Invalid cron expression '{cron_expression}'")
    should_have_run_date = croniter(cron_expression).get_prev(datetime.datetime).date()
    logging.info(f"Should have run at {should_have_run_date}")
    if not os.path.isdir(checkpoints_dir):
        logging.warning(f"The given directory '{checkpoints_dir}' does not exist, assuming no checkpoints exist")
        raise typer.Exit(code=1)
    latest_checkpoint_date = None
    for filename in os.listdir(checkpoints_dir):
        try:
            checkpoint = datetime.date.fromisoformat(filename)
            if latest_checkpoint_date is None or checkpoint >= latest_checkpoint_date:
                latest_checkpoint_date = checkpoint
        except ValueError:
            logging.warning(f"The file '{filename}' is not a valid checkpoint")
    if latest_checkpoint_date is None:
        logging.warning(f"No checkpoints found in directory '{checkpoints_dir}'")
        raise typer.Exit(code=1)
    logging.info(f"Latest checkpoint was at {latest_checkpoint_date}")
    if latest_checkpoint_date >= should_have_run_date:
        logging.info("Looking good!")
        raise typer.Exit(code=0)
    logging.info("Looks like you're behind schedule...")
    raise typer.Exit(code=1)
