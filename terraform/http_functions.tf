locals {
  http_functions = {
    wewu_scheduler = {
      source = "wewu_less/handlers/scheduler.py"
      handler = "wewu_scheduler"
      memory = "256Mi"
      timeout_seconds = 60
      environment = {
        WEWU_WORKER_QUEUE_TOPIC = "projects/wewu-410223/topics/monitor-task-topic"
      }
    }
    wewu_api_register_service = {
      source = "wewu_less/handlers/entry.py"
      handler = "wewu_api_register_service"
      memory = "256Mi"
      timeout_seconds = 3
      environment = {
        WEWU_REGISTER_TASK_QUEUE_TOPIC = local.queues.register_service_task_queue.topic
        WEWU_DELETE_TASK_QUEUE_TOPIC = local.queues.delete_service_task_queue.topic
      }
    }
    wewu_api_delete_service = {
      source = "wewu_less/handlers/entry.py"
      handler = "wewu_api_delete_service"
      memory = "256Mi"
      timeout_seconds = 3
      environment = {
        WEWU_REGISTER_TASK_QUEUE_TOPIC = local.queues.register_service_task_queue.topic
        WEWU_DELETE_TASK_QUEUE_TOPIC = local.queues.delete_service_task_queue.topic
      }
    }
    wewu_buzzator = {
      source = "wewu_less/handlers/buzzator.py"
      handler = "wewu_buzzator"
      memory = "512Mi"
      timeout_seconds = 120
      environment = {
        WEWU_SEND_NOTIFICATION_EVENT_QUEUE_TOPIC = local.queues.send_notification_event_queue.topic
      }
    }
    wewu_tester = {
      source = "wewu_less/handlers/tester.py"
      handler = "wewu_tester"
      memory = "256Mi"
      timeout_seconds = 15
      environment = {}
    }
  }
}
