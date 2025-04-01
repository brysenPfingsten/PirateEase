import time

def slow_print(s: str, delay: float = 0.02) -> None:
    """
    Prints the given string like how an AI would.
    :param s: The string to print.
    :param delay: Delay in seconds between each character being printed
    :return: None
    """
    for c in s:
        print(c, end='', flush=True)
        time.sleep(delay)
    print()