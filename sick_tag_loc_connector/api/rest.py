#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
import json
from enum import Enum
from urllib.parse import urljoin

# Third-party
import requests

# The global endpoint name for streams
STREAMS_ENDPOINT: str = "/streams"


class FeedTypes(Enum):
    """Enum representing different types of feeds.

    These are all the currently supported feeds in the SICK Tag-LOC system.

    Attributes:
        ANCHOR (str): The feed type for anchor feeds.
        TAG (str): The feed type for tag feeds.
        BUILDING (str): The feed type for building feeds.
    """

    ANCHOR = "anchor"
    TAG = "tag"
    BUILDING = "building"


class RestClient:
    """RestClient

    A helper class for making API requests using the RestClient.

    Attributes:
        url (str): The base URL of the API
        headers (dict): The headers to be included in every request
    """

    def __init__(self, url: str, api_key: str) -> None:
        """RestClient Constructor

        Initializes a new instance of the class.

        Args:
            url (str): The URL to the API
            api_key (str): The API key for authentication
        """
        self.url = url
        self.headers = {"X-ApiKey": api_key, "Content-Type": "application/json"}

    def get(self, endpoint: str) -> dict:
        """Helper Method for GET

        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The endpoint to make the GET request to.

        Returns:
            dict: The response in JSON format.

        Raises:
            requests.HTTPError: If the GET request returns a non-success status code.
        """
        response = requests.get(urljoin(self.url, endpoint), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint: str, data: dict) -> dict:
        """Helper Method for POST

        Sends a POST request to the specified endpoint with the given data.

        Args:
            endpoint (str): The endpoint where the request will be sent
            data (dict): The data to be sent in the request body

        Returns:
            dict: The JSON response from the server

        Raises:
            requests.HTTPError: If the GET request returns a non-success status code
        """
        response = requests.post(
            urljoin(self.url, endpoint), headers=self.headers, data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()

    def put(self, endpoint: str, data: dict) -> dict:
        """Helper Method for PUT

        Sends a PUT request to the specified endpoint with the given data.

        Args:
            endpoint (str): The endpoint where the request will be sent
            data (dict): The data to be sent in the request body

        Returns:
            A dictionary representing the JSON response from the PUT request

        Raises:
            requests.HTTPError: If the GET request returns a non-success status code
        """
        response = requests.put(
            urljoin(self.url, endpoint), headers=self.headers, data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()

    def delete(self, endpoint: str) -> dict:
        """Helper Method for DELETE

        Deletes a resource by sending a DELETE request to the specified endpoint

        Args:
            endpoint (str): The endpoint to which the DELETE request will be sent

        Returns:
            dict: The response content in JSON format

        Raises:
            requests.HTTPError: If the GET request returns a non-success status code
        """
        response = requests.delete(urljoin(self.url, endpoint), headers=self.headers)
        response.raise_for_status()
        return response.json()
