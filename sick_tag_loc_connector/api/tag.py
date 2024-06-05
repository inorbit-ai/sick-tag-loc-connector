#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from typing import Type, TypeVar, Set, Any

# InOrbit
from sick_tag_loc_connector.api import RestClient

# The endpoint name for tags
ENDPOINT: str = "tags"

T = TypeVar("T", bound="Tag")


class Tag:
    """A class representing a SICK Tag-LOC tag.

    A Tag is a feed used to store datastreams with information on location.

    Attributes:
        rest_client (RestClient): The client used to communicate with the REST API
        alias (str | None): User defined alias for feed (i.e., tag/anchor)
        private (bool): If the Tag should be private or public (defaults to False)
        description (str | None): User defined description for the Tag
        feed (str | None): This parameter can be set to any value
        status (str | None): User can set to any value, e.g. live or frozen
        version (str | None): Can be set to any value
        website (str | None): Can be set to any value
        tags (Set[str]): Feeds can be filtered by the value of this meta-tag
        tag_id (str | None): Auto generated unique ID which identifies tags
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
        # Fields that can be manually set
        self.rest_client = rest_client
        self.alias = alias
        self.private = private
        self.description = description
        self.feed = feed
        self.status = status
        self.version = version
        self.website = website
        self.tags = tags if tags else []

        # Fields that are set automatically by the server
        self.tag_id: str | None = kwargs.get("id", None)
        self.title: str | None = kwargs.get("title", None)
        self.updated: str | None = kwargs.get("updated", None)
        self.created: str | None = kwargs.get("created", None)
        self.creator: str | None = kwargs.get("creator", None)

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

    def update(self) -> None:
        """Updates the data for this Tag.

        This method will update the data for this Tag using the REST API. It assumes
        attributes have been set on this object.
        """
        updated_data = self.get_attrs_dict()
        data = self.rest_client.put(f"/{ENDPOINT}/{self.tag_id}", updated_data)
        # Update the Tag with the latest data from the server
        [self.__setattr__("tag_id" if k == "id" else k, v) for k, v in data.items()]

    def save(self) -> None:
        """Saves the current Tag.

        If the object has a `tag_id`, it will call the `update()` method on the object.
        Otherwise, it will call the `create()` method on the object using the REST
        client and the object's dictionary. It assumes  attributes have been set on this
        object.
        """
        if self.tag_id:
            self.update()
        else:
            data = Tag.create(self.rest_client, self.get_attrs_dict()).get_attrs_dict()
            # Update the Tag with the latest data from the server
            [self.__setattr__("tag_id" if k == "id" else k, v) for k, v in data.items()]

    def delete(self) -> None:
        """Deletes the current tag from the system.

        This will use the DELETE HTTP method and reset this tag to have no ID.
        """
        self.rest_client.delete(f"/{ENDPOINT}/{self.tag_id}")
        self.tag_id = None

    def get_attrs_dict(self):
        """Get the attribute dictionary of the object.

        This method retrieves the attributes of the Tag and returns them as a dict.
        It excludes the rest_client attribute from the dictionary.
        If the object has a "tag_id" attribute, it is renamed to "id" in the result.

        Returns:
            dict: The dictionary containing the attributes of the object.
        """
        # We don't serialize the client
        class_attrs = {k: v for k, v in self.__dict__.items() if k != "rest_client"}

        # tag_id is serialized as id since we don't overwrite the builtin python 'id'
        if "tag_id" in class_attrs:
            class_attrs["id"] = class_attrs.pop("tag_id")

        return class_attrs