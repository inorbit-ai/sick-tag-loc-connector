#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from typing import Type, TypeVar, Set, Any

# InOrbit
from sick_tag_loc_connector.api import RestClient

# The endpoint name for feeds
ENDPOINT: str = "/feeds"

T = TypeVar("T", bound="Feed")


class Feed:
    """A class representing a SICK Tag-LOC feed.

     Feed is a general term for anchor/tag/building or any other user specified object.

    Attributes:
        rest_client (RestClient): The client used to communicate with the REST API
        endpoint (str): The endpoint name (defaults to "feeds")
        alias (str | None): User defined alias for feed (i.e., tag/anchor)
        title (str | None): Title is user defined name for feed
        private (str): If the feed should be private or public (default is "0");
                       If feed is private then it can only be looked up by request with
                       X-ApiKey which belongs to user that created that feed;
                       Public feed can be looked up by any X-ApiKey
        description (str | None): User defined description
        feed (str | None): This parameter can be set to any value
        tags (Set[str]): Feeds can be filtered by the value of this meta-tag
        version (str | None): Can be set to any value
        website (str | None): Can be set to any value

        _id (str | None): Auto generated unique ID which identifies feeds
        _type (str | None): Type of feed (tag, anchor, or building)
        updated (str | None): Auto set to the time when the feed was last updated
        created (str | None): Auto set to the time when the feed was created
        creator (str | None): Auto set to the user whose X-ApiKey was used for creation
    """

    def __init__(
        self,
        rest_client: RestClient,
        endpoint: str = ENDPOINT,
        alias: str | None = None,
        title: str | None = None,
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
        """Initialize a new Feed instance with the given parameters.

        Note that typically you will want to use the Feed.get() class method to get an
        existing feed or Feed.create() class method to create a new feed.

        Args:
            rest_client (RestClient): The client used to communicate with the REST API
            endpoint (str, optional): The endpoint name (defaults to "feeds")
            alias (str | None): User defined alias for feed (i.e., tag/anchor)
            title (str | None): Title is user defined name for feed
            private (str): If the feed should be private or public (default is "0");
                           If feed is private then it can only be looked up by request
                           with X-ApiKey which belongs to user that created that feed;
                           Public feed can be looked up by any X-ApiKey
            description (str | None): User defined description
            feed (str | None): This parameter can be set to any value
            tags (Set[str]): Feeds can be filtered by the value of this meta-tag
            version (str | None): Can be set to any value
            website (str | None): Can be set to any value
            **kwargs (Any): Additional keyword args that are typically set by the server
        """

        # Client-only fields
        self.rest_client = rest_client
        self.endpoint = endpoint

        # Fields that can be manually set
        self.alias = alias
        self.title = title
        self.private = private
        self.description = description
        self.feed = feed
        self.version = version
        self.website = website
        self.tags = tags if tags else []

        # Fields that are set automatically by the server (or subclasses)
        self._id: str | None = kwargs.get("id", None)
        self._type: str | None = kwargs.get("type", None)
        self.updated: str | None = kwargs.get("updated", None)
        self.created: str | None = kwargs.get("created", None)
        self.creator: str | None = kwargs.get("creator", None)

    @classmethod
    def get(cls: Type[T], rest_client: RestClient, feed_id: str) -> T:
        """Get a Feed from the system by ID.

        This class method will attempt to load the feed with the given ID from the SICK
        Tag-LOC system via the REST API.

        Args:
            rest_client (RestClient): The client to communicate with the REST API
            feed_id (str): The ID of the feed to retrieve

        Returns:
            An instance of the Feed class, representing the retrieved feed
        """
        data = rest_client.get(f"{ENDPOINT}/{feed_id}")
        return cls(rest_client, **data)

    @staticmethod
    def get_all(rest_client: RestClient) -> Set[T]:
        """Get all the feeds from the system.

        This static method will attempt to load all the feeds from the SICK
        Tag-LOC system via the REST API.

        Args:
            rest_client (RestClient): The client to communicate with the REST API

        Returns:
            A set of Feed instances, representing the retrieved feeds
        """
        # TODO(elvio.aruta): add pagination to this get call
        data = rest_client.get(ENDPOINT)
        feed_set = {Feed(rest_client, **feed) for feed in data["results"]}
        return feed_set

    @classmethod
    def create(cls: Type[T], rest_client: RestClient, data: dict) -> T:
        """Create a new Feed.

        This class method will use the REST API to create a new Feed with the provided
        data. It will return an instance of the Feed class representing the newly
        created feed.

        Args:
            rest_client (RestClient): The client to communicate with the REST API
            data (dict): A dictionary containing the data for creating a new Feed

        Returns:
            An instance of the Feed class, representing the created feed
        """
        data = rest_client.post(ENDPOINT, data)
        return cls(rest_client, **data)

    def update(self) -> None:
        """Updates the data for this Feed.

        This method will update the data for this Feed using the REST API. It assumes
        attributes have been set on this object.
        """
        attrs = self.get_attrs_dict()
        data = self.rest_client.put(f"{self.endpoint}/{self._id}", attrs)
        # Update the Feed with the latest data from the server
        [
            self.__setattr__("_id" if k == "id" else "_type" if k == "type" else k, v)
            for k, v in data.items()
        ]

    def save(self) -> None:
        """Saves the current Feed.

        If the object has a `feed_id`, it will call the `update()` method on the object.
        Otherwise, it will call the `create()` method on the object using the REST
        client and the object's dictionary. It assumes attributes have been set on this
        object.
        """
        if self._id:
            self.update()
        else:
            instance = type(self).create(self.rest_client, self.get_attrs_dict())
            data = instance.get_attrs_dict()
            # Update the Feed with the latest data from the server
            for k, v in data.items():
                if k == "id":
                    self.__setattr__("_id", v)
                elif k == "type":
                    self.__setattr__("_type", v)
                else:
                    self.__setattr__(k, v)

    def delete(self) -> None:
        """Deletes the current feed from the system.

        This will use the DELETE HTTP method and reset this feed to have no ID.
        """
        self.rest_client.delete(f"{self.endpoint}/{self._id}")
        self._id = None

    def get_attrs_dict(self) -> dict:
        """Get the attribute dictionary of the object.

        This method retrieves the attributes of the Feed and returns them as a dict.
        It excludes the rest_client attribute from the dictionary.

        If the object has "_id" or "_type" attribute, they will be changed to "id" and
        "type" respectively in the result.

        Returns:
            dict: The dictionary containing the attributes of the object.
        """
        # We don't serialize the client or endpoint
        class_attrs = {k: v for k, v in self.__dict__.items()}
        class_attrs.pop("rest_client")
        class_attrs.pop("endpoint")

        # We use _id to not overwrite the builtin python "id"
        if "_id" in class_attrs:
            class_attrs["id"] = class_attrs.pop("_id")
        # We use _type to not overwrite the builtin python "type"
        if "_type" in class_attrs:
            class_attrs["type"] = class_attrs.pop("_type")

        return class_attrs
