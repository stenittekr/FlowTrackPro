from database.transaction_manager import TransactionManager

from repositories.approval_repository import (
    create_approval_request,
    get_pending_requests,
    approve_request
)


def submit_for_approval(
    task_id,
    user_id
):
    with TransactionManager() as conn:

        request_id = create_approval_request(
            conn,
            task_id,
            user_id
        )

        return {
            "request_id": request_id,
            "message": "Submitted for approval"
        }


def pending_approvals():

    with TransactionManager() as conn:

        requests = get_pending_requests(conn)

        return [
            dict(r)
            for r in requests
        ]


def approve(
    request_id,
    manager_id
):
    with TransactionManager() as conn:

        approve_request(
            conn,
            request_id,
            manager_id
        )

        return {
            "message": "Approved"
        }