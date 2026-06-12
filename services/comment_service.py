from database.transaction_manager import TransactionManager

from repositories.comment_repository import (
    add_comment,
    get_comments
)


def create_comment(
    task_id,
    user_id,
    comment
):

    with TransactionManager() as conn:

        comment_id = add_comment(
            conn,
            task_id,
            user_id,
            comment
        )

        return {
            "comment_id": comment_id,
            "message": "Comment added"
        }


def list_comments(task_id):

    with TransactionManager() as conn:

        comments = get_comments(
            conn,
            task_id
        )

        return [
            dict(comment)
            for comment in comments
        ]