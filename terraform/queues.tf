locals {
  queues = {
    register_service_task_queue = {
      topic = "register-service-task-queue"
      message_retention = "86600s"
    }
  }
}
