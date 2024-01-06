locals {
  functions = {
    wewu_scheduler = {
      source = "wewu_less/handlers/scheduler.py"
      handler = "wewu_scheduler"
      memory = "256M"
      environment = {}
    }
  }
}
