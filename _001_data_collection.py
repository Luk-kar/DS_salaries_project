from config.get_config import get_args

args = get_args()


def get_jobs(
        job_title=args["jobs_titles"]["default"],
        url=args["url"], jobs_number=args["jobs_number"],
        driver_path=args["driver_path"],
        debug_mode=args["debug_mode"]
):

    print(job_title, url, jobs_number, driver_path, debug_mode)


get_jobs()
