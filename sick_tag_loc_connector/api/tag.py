#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from typing import Type, TypeVar, Set, Any, List, Callable

# InOrbit
from sick_tag_loc_connector.api import RestClient
from sick_tag_loc_connector.api.feed import Feed
from sick_tag_loc_connector.api.rest import FeedTypes
from sick_tag_loc_connector.api.websocket import WebSocketClient

# The endpoint name for tags
ENDPOINT: str = "tags"

T = TypeVar("T", bound="Tag")


class Tag(Feed):
    """A class representing a SICK Tag-LOC tag.

    A Tag is a feed used to store datastreams with information on location.

    Attributes:
        rest_client (RestClient): The client used to communicate with the REST API
        endpoint (str): The endpoint name
        alias (str | None): User defined alias for feed (i.e., tag/anchor)
        private (bool): If the Tag should be private or public (defaults to False)
        description (str | None): User defined description for the Tag
        feed (str | None): This parameter can be set to any value
        status (str | None): User can set to any value, e.g. live or frozen
        version (str | None): Can be set to any value
        website (str | None): Can be set to any value
        tags (Set[str]): Feeds can be filtered by the value of this meta-tag
        _id (str | None): Auto generated unique ID which identifies tags
        _type (str | None): Type of feed (tag, anchor, or building)
        title (str | None): Tags have autogenerated title which is their mac address’
        updated (str | None): Set to the time when the tag was last updated
        created (str | None): Set to the time when the feed was created
        creator (str | None): Set to the user whose X-ApiKey was used for creation
    """

    def __init__(
        self,
        rest_client: RestClient,
        alias: str | None = None,
        private: bool = False,
        description: str | None = None,
        feed: str | None = None,
        status: str | None = None,
        version: str | None = None,
        website: str | None = None,
        tags: Set[str] = None,
        # TODO(russell): datastreams (array of datastreams)
        # TODO(russell): location (location datatype in SICK),
        **kwargs: Any,
    ) -> None:
        """Initialize a new Tag instance with the given parameters.

        Note that typically you will want to use the Tag.get() class method to get an
        existing tag or Tag.create() class method to create a new tag.

        Args:
            rest_client (RestClient): The client used to communicate with the REST API
            alias (str | None): User defined alias for feed (i.e., tag/anchor)
            private (bool): If the Tag should be private or public (defaults to False)
            description (str | None): User defined description for the Tag
            feed (str | None): This parameter can be set to any value
            status (str | None): User can set to any value, e.g. live or frozen
            version (str | None): Can be set to any value
            website (str | None): Can be set to any value
            tags (Set[str]): Feeds can be filtered by the value of this meta-tag
            **kwargs (Any): Additional keyword args that are typically set by the server
        """
        super().__init__(
            rest_client=rest_client,
            endpoint=ENDPOINT,
            type=FeedTypes.TAG.value,
            alias=alias,
            private=private,
            description=description,
            feed=feed,
            version=version,
            website=website,
            tags=tags,
            **kwargs,
        )
        # Fields that can be manually set
        self.status = status

    @classmethod
    def get(cls: Type[T], rest_client: RestClient, tag_id: str) -> T:
        """Get a Tag from the system by ID.

        This class method will attempt to load the tag with the given ID from the SICK
        Tag-LOC system via the REST API.

        Args:
            rest_client (RestClient): The client to communicate with the REST API
            tag_id (str): The ID of the tag to retrieve

        Returns:
            An instance of the Tag class, representing the retrieved tag
        """
        data = rest_client.get(f"/{ENDPOINT}/{tag_id}")
        return cls(rest_client, **data)

    @staticmethod
    def get_all(rest_client: RestClient) -> List["Tag"]:
        """Get all the Tags from the system

        This static method will attempt to load all the tags from the SICK
        Tag-LOC system via the REST API.

        Args:
            rest_client (RestClient): The client to communicate with the REST API

        Returns:
            An instance of the Tag class, representing the retrieved tag
        """
        # TODO(elvio.aruta): add pagination to this get call
        data = rest_client.get(f"/{ENDPOINT}")
        tag_list = [Tag(rest_client, **tag) for tag in data["results"]]
        return tag_list

    @classmethod
    def create(cls: Type[T], rest_client: RestClient, tag_data: dict) -> T:
        """Create a new Tag.

        This class method will use the REST API to create a new Tag with the provided
        data. It will return an instance of the Tag class representing the newly created
        tag.

        Args:
            rest_client (RestClient): The client to communicate with the REST API
            tag_data (dict): A dictionary containing the data for creating a new Tag

        Returns:
            An instance of the Tag class, representing the created tag
        """
        data = rest_client.post(f"/{ENDPOINT}", tag_data)
        return cls(rest_client, **data)


class TagStreamWebSocketClient(WebSocketClient):
    """
    A WebSocket client specifically for subscribing to tag updates.

    Inherits from WebSocketClient and adds functionality to handle tag-specific subscriptions.
    """

    def __init__(self, url: str, api_key: str, on_message_callback: Callable, tag: Tag):
        """
        Initialize the TagStreamWebSocketClient.

        Args:
            url (str): The URL for the WebSocket connection.
            api_key (str): The API key for authentication.
            on_message_callback (Callable): The callback function to handle incoming messages.
            tag (Tag): The Tag instance to subscribe to updates for.

        NOTE(elvio.aruta):
            If the API key is the same for both REST and WebSocket clients, consider reading the key
            directly from the tag instance.
            If that's the case, refactor the Tag class to add subscribe(callback) method and make it
            return a TagStreamWebSocketClient() already subscribed to the updates.
        """
        super().__init__(url, api_key, on_message_callback)
        self.tag = tag

    def subscribe_to_tag_updates(self) -> None:
        """
        Subscribe to updates for the specific tag associated with this client.

        This method constructs a subscription message and sends it via the WebSocket connection.

        NOTE(elvio.aruta):
            The "method" and "resource" in the message should be parameterized. Possible values
            should be part of this class (add new Enums)
        """
        sub_message = (
            f'{{"headers":{{"X-ApiKey":"{self.api_key}"}}, "method":"subscribe", '
            f'"resource":"/feeds/{self.tag._id}"}}'
        )
        super().send(sub_message)
