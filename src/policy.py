"""GROOT-01 observable resource policy."""

from .logger import log_action
from .resources import check_ram, check_vm_limit



def check_ram_policy(logger, min_free_ram_mb: int) -> bool:
    """Check RAM and log the decision."""
    allowed, message = check_ram(min_free_ram_mb)

    result = "SAFE" if allowed else "REFUSED"
    log_action(logger, "RESOURCE_CHECK | RAM", result, message)

    return allowed



def check_vm_policy(logger, running_vms: int, max_running_vms: int) -> bool:
    """Check VM limit and log the decision."""
    allowed, message = check_vm_limit(running_vms, max_running_vms)

    result = "SAFE" if allowed else "REFUSED"
    log_action(logger, "RESOURCE_CHECK | VM", result, message)

    return allowed
