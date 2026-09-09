from typing import Any

from frontend.core.polling import ACTIVE_STATUSES, SUCCESS_STATUSES, FAILED_STATUSES


def display_inngest_run_status(T: dict[str, str], status: str, status_placeholder: Any):

    if status == "ConnectionError":
        status_placeholder.warning(T["status_retry"])

    elif status in ACTIVE_STATUSES:
        status_placeholder.info(f"⏳ {T['status']}: **{status}**")

    elif status in SUCCESS_STATUSES:
        status_placeholder.success(T["operation_completed"])

    elif status in FAILED_STATUSES:
        status_placeholder.error(
            f"❌ {T['operation_failed']}: "
            f"**{status}**"
        )

    else:
        status_placeholder.warning(
            f"{T['operation_status']}: "
            f"**{status}**"
        )