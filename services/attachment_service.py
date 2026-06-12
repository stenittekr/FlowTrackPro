from database.transaction_manager import TransactionManager

from repositories.attachment_repository import (
    create_attachment,
    get_attachments
)


def add_attachment(
    task_id,
    file_name,
    file_path,
    uploaded_by
):
    with TransactionManager() as conn:
        attachment_id = create_attachment(
            conn,
            task_id,
            file_name,
            file_path,
            uploaded_by
        )

        return {
            "attachment_id": attachment_id,
            "message": "Attachment uploaded"
        }


def list_attachments(task_id):
    with TransactionManager() as conn:
        attachments = get_attachments(
            conn,
            task_id
        )

        return [
            dict(attachment)
            for attachment in attachments
        ]