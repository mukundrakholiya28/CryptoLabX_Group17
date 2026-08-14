from datetime import datetime


def write_log(option):

    with open("outputs/execution.log", "a") as log:

        now = datetime.now()

        log.write(
            f"{now.strftime('%Y-%m-%d %H:%M:%S')} -> {option}\n"
        )