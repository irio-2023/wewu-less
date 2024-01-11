locals {
  http_functions = {
    wewu_scheduler = {
      source = "wewu_less/handlers/scheduler.py"
      handler = "wewu_scheduler"
      memory = "256M"
      timeout_seconds = 60
      environment = {
        GOOGLE_WORKER_QUEUE_TOPIC = "monitor-task-topic"
      }
    }
    wewu_api_register_service = {
      source = "wewu_less/handlers/entry.py"
      handler = "wewu_api_register_service"
      memory = "256M"
      timeout_seconds = 3
      environment = {
        WEWU_REGISTER_TASK_QUEUE_TOPIC = local.queues.register_service_task_queue.topic
      }
    }

  }
}
