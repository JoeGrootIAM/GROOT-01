"""GROOT-01 resource and safety policy."""

import psutil



def available_ram_mb() -> float:
    """Return currently available RAM in MiB."""
    return psutil.virtual_memory().available / (1024 * 1024)



def check_ram(min_free_ram_mb: int) -> tuple[bool, str]:
    """Check whether available RAM is above the safety floor."""
    available = available_ram_mb()

    if available < min_free_ram_mb:
        return (
            False,
            f"REFUSED: {available:.0f} MiB available; "
            f"minimum is {min_free_ram_mb} MiB.",
        )

    return (
        True,
        f"SAFE: {available:.0f} MiB available; "
        f"minimum is {min_free_ram_mb} MiB.",
    )

def check_vm_limit(running_vms: int, max_running_vms: int) -> tuple[bool, str]:
    """Check whether starting another VM would exceed the policy."""
    if running_vms >= max_running_vms:
        return (
            False,
            f"REFUSED: {running_vms} VM(s) already running; "
            f"maximum is {max_running_vms}.",
        )

    return (
        True,
        f"SAFE: {running_vms} VM(s) running; "
        f"maximum is {max_running_vms}.",
    )
