locals {
  functions = {
    wewu_scheduler = {
      source = "wewu_less/handlers/scheduler.py"
      handler = "wewu_scheduler"
      memory = "256M"
      environment = {
        GOOGLE_WORKER_QUEUE_TOPIC = "monitor-task-topic"
      }
    }
  }
}
