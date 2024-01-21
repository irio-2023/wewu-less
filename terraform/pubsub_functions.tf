locals {
  pubsub_functions = {
    wewu_api_copy_and_paste_inator = {
      source = "wewu_less/handlers/entry.py"
      handler = "wewu_api_copy_and_paste_inator"

      memory = "256Mi"
      timeout_seconds = 60

      trigger_topic = local.queues.register_service_task_queue.topic
      retry_policy = true
      environment = {
        WEWU_DELETE_TASK_QUEUE_TOPIC = local.queues.delete_service_task_queue.topic
        WEWU_REGISTER_TASK_QUEUE_TOPIC = local.queues.register_service_task_queue.topic
      }
    }
    wewu_api_delete_and_paste_inator = {
      source = "wewu_less/handlers/entry.py"
      handler = "wewu_api_delete_and_paste_inator"

      memory = "256Mi"
      timeout_seconds = 60

      trigger_topic = local.queues.delete_service_task_queue.topic
      retry_policy = true
      environment = {
        WEWU_REGISTER_TASK_QUEUE_TOPIC = local.queues.register_service_task_queue.topic
        WEWU_DELETE_TASK_QUEUE_TOPIC = local.queues.delete_service_task_queue.topic
      }
    }
    wewu_notifier = {
      source = "wewu_less/handlers/notifier.py"
      handler = "wewu_notifier"

      memory = "256M"
      timeout_seconds = 60

      trigger_topic = local.queues.send_notification_event_queue.topic
      retry_policy = true
      environment = {
        WEWU_CLOUD_TASKS_QUEUE_NAME = google_cloud_tasks_queue.notifier_cloud_tasks_queue.name
        WEWU_CLOUD_TASKS_QUEUE_REGION = google_cloud_tasks_queue.notifier_cloud_tasks_queue.location
        WEWU_CLOUD_TASKS_QUEUE_PROJECT = google_cloud_tasks_queue.notifier_cloud_tasks_queue.project
        WEWU_SEND_NOTIFICATION_EVENT_QUEUE_TOPIC = local.queues.send_notification_event_queue.topic
        NOTIFICATION_URL = google_cloudfunctions2_function.http_cf_template["wewu_acker"].url
        SERVICE_MAIL = "wewu.alert.inator@gmail.com"
        MAIL_API_KEY = var.MAIL_API_KEY
        MAIL_API_SECRET = var.MAIL_API_SECRET_KEY
        WEWU_PUBSUB_HTTP_KEY = var.WEWU_PUBSUB_HTTP_KEY
        WEWU_SERVICE_ACCOUNT_EMAIL = var.WEWU_SERVICE_ACCOUNT_EMAIL
        TWILIO_ACCOUNT_SID = "ACabafe1af5723c567643198fe7e416097"
        TWILIO_AUTH_TOKEN = var.TWILIO_AUTH_TOKEN
      }
    }
  }
}
