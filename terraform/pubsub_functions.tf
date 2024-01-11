locals {
  pubsub_functions = {
    wewu_api_copy_and_paste_inator = {
      source = "wewu_less/handlers/entry.py"
      handler = "wewu_api_copy_and_paste_inator"

      memory = "256M"
      timeout_seconds = 60

      trigger_topic = local.queues.register_service_task_queue.topic
      retry_policy = true
      environment = {
        WEWU_REGISTER_TASK_QUEUE_TOPIC = local.queues.register_service_task_queue.topic
      }
    }
  }
}
