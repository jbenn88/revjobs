import sys
from selenium.common import WebDriverException
from src.driver_setup import setup_driver, teardown_driver
from src.auth import login
from src.data_retrieval import apply_filters, collect_job_data
from src.notification import send_notification
from src.output import update_job_data_files, save_prev_week_job_data, erase_file, first_run_of_week
from src.plots import update_scatter_plot
from config.config import get_config

config = get_config()


def main():
    try:
        driver = setup_driver()
    except WebDriverException:
        print("selenium.common.exceptions.WebDriverException: "
              "Message: Process unexpectedly closed with status 2.")
        print("This typically happens when logged in with another macOS user account. "
              "Program exiting.")
        sys.exit(1)

    try:

        # Save last week's job data, max jobs plot, and reset weekly job data txt file
        if first_run_of_week():
            save_prev_week_job_data()
            erase_file(config['weekly_data_filepath'])

        login(driver)
        apply_filters(driver)
        data = collect_job_data(driver)
        update_job_data_files(data)
        update_scatter_plot()
        send_notification(
            "Available Job Information",
            f"NVNR jobs: {data['number_of_non_verbatim_or_rush_jobs']} | "
            f"Line jobs: {data['number_of_line_jobs']} \n"
            f"0 unclaims: {data['zero_unclaim_count']} | "
            f"0-2 unclaims: {data['number_of_jobs_with_less_than_two_unclaims']} \n"
            f"10 minutes or less: {data['under_ten_count']} | "
            f"5 minutes or less: {data['under_five_count']} \n"
        )

    finally:
        teardown_driver(driver)


if __name__ == "__main__":
    main()
