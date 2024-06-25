#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from typing import Type, TypeVar, Set, Any

# InOrbit
from sick_tag_loc_connector.api import RestClient, ENDPOINT_TAGS
from sick_tag_loc_connector.api.feed import Feed
from sick_tag_loc_connector.api.rest import FeedTypes

# Type hint definition
T: TypeVar = TypeVar("T", bound="Tag")


class Tag(Feed):
    """A class representing a SICK Tag-LOC tag.

    A Tag is a feed used to store datastreams with information on location.

    Attributes:
        rest_client (RestClient): The client used to communicate with the REST API
        endpoint (str): The endpoint name
        alias (str | None): User defined alias for feed (i.e., tag/anchor)
        private (str): If the feed should be private or public (default is "0");
                       If feed is private then it can only be looked up by request with
                       X-ApiKey which belongs to user that created that feed;
                       Public feed can be looked up by any X-ApiKey
        description (str | None): User defined description for the Tag
        feed (str | None): This parameter can be set to any value
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
        private: str = "0",
        description: str | None = None,
        feed: str | None = None,
        version: str | None = None,
        website: str | None = None,
        tags: Set[str] = None,
        # TODO(russell): datastreams (array of datastreams)
        # TODO(russell): location (location datatype in SICK)
        # TODO(russell): zones (array)
        # TODO(russell): creator_id (ID as string)
        # TODO(russell): uuid (string)
        **kwargs: Any,
    ) -> None:
        """Initialize a new Tag instance with the given parameters.

        Note that typically you will want to use the Tag.get() class method to get an
        existing tag or Tag.create() class method to create a new tag.

        Args:
            rest_client (RestClient): The client used to communicate with the REST API
            alias (str | None): User defined alias for feed (i.e., tag/anchor)
            private (str): If the feed should be private or public (default is "0");
                           If feed is private then it can only be looked up by request
                           with X-ApiKey which belongs to user that created that feed;
                           Public feed can be looked up by any X-ApiKey
            description (str | None): User defined description for the Tag
            feed (str | None): This parameter can be set to any value
            version (str | None): Can be set to any value
            website (str | None): Can be set to any value
            tags (Set[str]): Feeds can be filtered by the value of this meta-tag
            **kwargs (Any): Additional keyword args that are typically set by the server
        """
        super().__init__(
            rest_client=rest_client,
            endpoint=ENDPOINT_TAGS,
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
        self._type = FeedTypes.TAG.value if not self._type else self._type

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
        data = rest_client.get(f"/{ENDPOINT_TAGS}/{tag_id}")
        return cls(rest_client, **data)

    @staticmethod
    def get_all(rest_client: RestClient) -> Set[T]:
        """Get all the Tags from the system

        This static method will attempt to load all the tags from the SICK
        Tag-LOC system via the REST API.

        Args:
            rest_client (RestClient): The client to communicate with the REST API

        Returns:
            A set of Tag instances, representing the retrieved tags
        """
        # TODO(elvio.aruta): add pagination to this get call
        data = rest_client.get(f"/{ENDPOINT_TAGS}")
        tag_set = {Tag(rest_client, **tag) for tag in data["results"]}
        return tag_set

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
        data = rest_client.post(f"/{ENDPOINT_TAGS}", tag_data)
        return cls(rest_client, **data)
