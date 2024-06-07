#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from typing import Type, TypeVar, Set, Any, List, Callable, Union

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

    @classmethod
    def get_all(cls: Type[T], rest_client: RestClient) -> List[T]:
        """Get all the Tags from the system

        This class method will attempt to load all the tags from the SICK
        Tag-LOC system via the REST API.

        Args:
            rest_client (RestClient): The client to communicate with the REST API

        Returns:
            An instance of the Tag class, representing the retrieved tag
        """
        data = rest_client.get(f"/{ENDPOINT}")
        tag_list = [cls(rest_client, **tag) for tag in data["results"]]
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
    def __init__(self, url: str, api_key: str, on_message_callback: Callable, tag: Tag):
        super().__init__(url, api_key, on_message_callback)
        self.tag = tag

    def suscribe_to_tag_updates(self) -> None:
        # TODO(elvio.aruta): parametrize "method" and "resource" (possible values should be part of this class)
        sub_message = f'{{"headers":{{"X-ApiKey":"{self.api_key}"}}, "method":"subscribe", "resource":"/feeds/{self.tag._id}"}}'
        super().send(sub_message)
