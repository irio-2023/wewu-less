from wewu_less.handlers.scheduler import wewu_scheduler


def test_should_schedule_expired_jobs():
    wewu_scheduler(None)
