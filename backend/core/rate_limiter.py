from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address
)

#This file creates a rate-limiting instance that controls how many requests a client can make.
# get_remote_address: Uses the client's IP address as the unique identifier to count a the number of requests made by the client.