from enum import Enum


class PingResult(Enum):
    Success = "SUC"
    Failure = "FAIL"
    ErrorTimeout = "ERR_TO"
    ErrorDNS = "ERR_DN"
    ErrorNoResponse = "ERR_NR"

    def __str__(self):
        return self.value
