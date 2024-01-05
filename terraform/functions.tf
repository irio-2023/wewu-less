locals {
  functions = {
    wewu_test_lambda_one = {
      source      = "wewu_less/echoer.py"
      handler     = "test_handler"
      memory      = "256M"
      environment = {}
    }
    wewu_test_lambda_two = {
      source = "wewu_less/echoer.py"
      handler = "second_test_handler"
      memory      = "256M"
      environment = {}
    }
  }
}