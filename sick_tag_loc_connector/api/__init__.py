#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.


# Constants
ENDPOINT_FEEDS: str = "feeds"
ENDPOINT_TAGS: str = "tags"
HEADER_API_KEY: str = "X-ApiKey"
REST_ENDPOINT = "/sensmapserver/api"

# Clients
from .rest import RestClient, FeedTypes  # noqa: F401, E402
from .websocket import WebSocketClient  # noqa: F401, E402

# Models
from .feed import Feed  # noqa: F401, E402
from .tag import Tag  # noqa: F401, E402
