locals {
  terraform_queues = {
    register_service_task_queue = {
      name = "register-service-task-queue"
      message_retention = "86600s"
    }
    delete_service_task_queue = {
      name = "delete-service-task-queue"
      message_retention = "86600s"
    }
    monitor_task_queue = {
      name = "monitor-task-queue"
      message_retention = "86600s"
    }
    send_notification_event_queue = {
      name = "send-notification-event-queue"
      message_retention = "86600s"
    }
  }

  queues = { for k, v in local.terraform_queues :
    k => merge(v, {
      topic = google_pubsub_topic.pubsub[k].id
    })
  }
}
