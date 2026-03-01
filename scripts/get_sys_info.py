import platform
from typing import Any, Dict

import colorama
import psutil
from colorama import Fore, Style


# Initialize colorama
colorama.init(autoreset=True)


def get_system_info() -> Dict[str, Any]:
    """Gathers comprehensive details about the system including OS, CPU, and RAM.

    Returns:
        Dict[str, Any]: A dictionary containing various pieces of system information.
    """
    system_info = {
        "Platform": platform.system(),
        "Platform Release": platform.release(),
        "Platform Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": platform.node(),
        "Processor": platform.processor(),
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "RAM Total": psutil.virtual_memory().total / (1024**3),  # Convert to GB
        "RAM Available": psutil.virtual_memory().available / (1024**3),  # Convert to GB
        "Swap Total": psutil.swap_memory().total / (1024**3),  # Convert to GB
        "Swap Free": psutil.swap_memory().free / (1024**3),  # Convert to GB
    }

    return system_info


if __name__ == "__main__":
    info = get_system_info()

    # Calculate the maximum key length for alignment
    max_key_length = max(len(key) for key in info.keys())

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}System{Style.RESET_ALL}")

    # Print formatted and colored output
    for key, value in info.items():
        key_colored = f"{Fore.BLUE}{key:<{max_key_length}}{Style.RESET_ALL}"
        value_colored = f"{Fore.GREEN}{value}{Style.RESET_ALL}"
        print(key_colored + " : " + value_colored)
