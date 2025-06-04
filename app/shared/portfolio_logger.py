from datetime import datetime


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_log(message, type="INFO"):
    message = f"[{datetime.now().strftime('%B %d at %-I:%M:%S %p %Z')}] {message}"
    match type:
        case "INFO":
            print(bcolors.OKBLUE + message + bcolors.ENDC)
        case "SUCCESS":
            print(bcolors.OKGREEN + message + bcolors.ENDC)
        case "WARNING":
            print(bcolors.WARNING + message + bcolors.ENDC)
        case "ERROR":
            print(bcolors.FAIL + message + bcolors.ENDC)
