from celery import shared_task

@shared_task
def loop_task() -> bool:
    print(f"task={'update_players'.upper()} is done")
    return True