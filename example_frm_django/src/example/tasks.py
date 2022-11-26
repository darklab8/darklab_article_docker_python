from celery import shared_task

@shared_task
def loop_task() -> bool:
    print(f"task={'loop_task'.upper()} is done")
    return True