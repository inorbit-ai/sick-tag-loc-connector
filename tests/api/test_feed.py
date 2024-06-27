#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from unittest.mock import Mock, MagicMock

# Third-party
import pytest

# InOrbit
from sick_tag_loc_connector.api import Feed, RestClient, ENDPOINT_FEEDS
from sick_tag_loc_connector.api.feed import SICK_RTLS_ID_PREFIX


class TestFeed:

    @staticmethod
    def validate_feed_data(feed, rest_client, feed_data):
        assert feed.rest_client is rest_client
        assert feed._id == feed_data["id"]
        assert feed.alias == feed_data["alias"]
        assert feed.private == feed_data["private"]
        assert feed.description == feed_data["description"]
        assert feed.feed == feed_data["feed"]
        assert feed._type == feed_data["type"]
        assert feed.version == feed_data["version"]
        assert feed.updated == feed_data["updated"]
        assert feed.created == feed_data["created"]
        assert feed.creator == feed_data["creator"]
        assert feed.website == feed_data["website"]
        assert feed.tags == feed_data["tags"]
        assert feed.title == feed_data["title"]
        assert id(feed) is not feed._id
        assert type(feed) is not feed._type

    @pytest.fixture
    def mock_rest_client(self):
        return Mock(spec=RestClient)

    @pytest.fixture
    def feed_data(self):
        return {
            "id": "1",
            "alias": "A6",
            "title": "0xE8EB1B3C0FE5",
            "private": "0",
            "description": "pizza-bot",
            "feed": "1.0.0",
            "updated": "2023-12-19 00:12:00.197192",
            "created": "2023-12-18 20:58:35.722557",
            "creator": "admin",
            "version": "1.0.0",
            "website": "https://pizza.com",
            "type": "anchor",
            "tags": ["#robots"],
        }

    @pytest.fixture
    def mock_feed(self, mock_rest_client, feed_data):
        feed = Feed(mock_rest_client, **feed_data)
        feed.rest_client.get.return_value = feed_data
        feed.rest_client.post.return_value = feed_data
        modified_data = feed_data.copy()
        modified_data["updated"] = "updated-now"
        feed.rest_client.put.return_value = modified_data
        feed.rest_client.delete = Mock()
        return feed

    def test_init_with_defaults(self, mock_rest_client):
        feed = Feed(mock_rest_client)
        assert feed.rest_client is mock_rest_client
        assert feed.endpoint == ENDPOINT_FEEDS
        assert feed.alias is None
        assert feed.private == "0"
        assert feed.description is None
        assert feed.feed is None
        assert feed.tags == []
        assert feed.version is None
        assert feed.website is None
        assert feed._id is None
        assert feed._type is None
        assert feed.updated is None
        assert feed.created is None
        assert feed.creator is None
        assert feed.title is None
        assert id(feed) is not feed._id
        assert type(feed) is not feed._type

    def test_init_with_all_parameters_set(self, mock_rest_client, feed_data):
        feed = Feed(mock_rest_client, **feed_data)
        self.validate_feed_data(feed, mock_rest_client, feed_data)

    def test_class_method_get(self, mock_rest_client, mock_feed, feed_data):
        feed = Feed.get(mock_rest_client, "1")
        mock_rest_client.get.assert_called_once_with(f"/{ENDPOINT_FEEDS}/1")
        self.validate_feed_data(feed, mock_rest_client, feed_data)

    def test_class_method_get_invalid__id(self, mock_rest_client):
        with pytest.raises(Exception):
            Feed.get(mock_rest_client, "invalid__id")
        mock_rest_client.get.assert_called_once_with(f"/{ENDPOINT_FEEDS}/invalid__id")

    def test_class_method_create(self, mock_rest_client, mock_feed, feed_data):
        feed = Feed.create(mock_rest_client, feed_data)
        mock_rest_client.post.assert_called_once_with(f"/{ENDPOINT_FEEDS}", feed_data)
        self.validate_feed_data(feed, mock_rest_client, feed_data)

    def test_update(self, mock_rest_client, mock_feed):
        original_data = mock_feed.get_attrs_dict()
        updated_data = {
            "alias": "update_feed_alias",
            "private": "1",
            "description": "update_feed_description",
            "feed": "update_feed_feed",
            "version": "update_feed_version",
            "website": "update_feed_website",
            "tags": {"update_feed_tagName"},
        }
        [setattr(mock_feed, key, value) for key, value in updated_data.items()]
        expected_data = mock_feed.get_attrs_dict()
        assert expected_data == {**original_data, **updated_data}

        mock_feed.update()
        assert "updated-now" == mock_feed.updated
        assert mock_feed._id is expected_data["id"]
        assert mock_feed._type is expected_data["type"]
        assert id(mock_feed) is not mock_feed._id
        assert type(mock_feed) is not mock_feed._type
        # noinspection PyUnresolvedReferences
        mock_feed.rest_client.put.assert_called_once_with(
            f"/{ENDPOINT_FEEDS}/1", expected_data
        )

    def test_save_with_existing_id(self, mock_rest_client, mock_feed):
        original_data = mock_feed.get_attrs_dict()
        updated_data = {
            "alias": "save_update_feed_alias",
            "private": True,
            "description": "save_update_feed_description",
            "feed": "save_update_feed_feed",
            "version": "save_update_feed_version",
            "website": "save_update_feed_website",
            "tags": {"save_update_feed_tagName"},
        }
        [setattr(mock_feed, key, value) for key, value in updated_data.items()]
        expected_data = mock_feed.get_attrs_dict()
        assert expected_data == {**original_data, **updated_data}

        mock_feed.save()
        assert "updated-now" == mock_feed.updated
        assert id(mock_feed) is not mock_feed._id
        assert type(mock_feed) is not mock_feed._type
        assert mock_feed._id is expected_data["id"]
        assert mock_feed._type is expected_data["type"]
        # noinspection PyUnresolvedReferences
        mock_feed.rest_client.put.assert_called_once_with(
            f"/{ENDPOINT_FEEDS}/1", expected_data
        )

    def test_save_with_no_id(self, mock_rest_client, mock_feed, feed_data):
        mock_feed.__setattr__("_id", None)
        original_data = mock_feed.get_attrs_dict()
        updated_data = {
            "alias": "save_create_feed_alias",
            "private": True,
            "description": "save_create_feed_description",
            "feed": "save_create_feed_feed",
            "version": "save_create_feed_version",
            "website": "save_create_feed_website",
            "tags": {"save_create_feed_tagName"},
        }
        [setattr(mock_feed, key, value) for key, value in updated_data.items()]
        expected_data = mock_feed.get_attrs_dict()
        assert expected_data == {**original_data, **updated_data}

        mock_feed.save()
        assert mock_feed._id is feed_data["id"]
        assert mock_feed._type is expected_data["type"]
        assert id(mock_feed) is not mock_feed._id
        assert type(mock_feed) is not mock_feed._type
        # noinspection PyUnresolvedReferences
        mock_feed.rest_client.post.assert_called_once_with(
            f"/{ENDPOINT_FEEDS}", expected_data
        )

    def test_delete(self, mock_feed):
        assert mock_feed._id == "1"
        mock_feed.delete()
        # noinspection PyUnresolvedReferences
        mock_feed.rest_client.delete.assert_called_once_with(f"/{ENDPOINT_FEEDS}/1")
        assert mock_feed._id is None

    def test_get_attrs_dict(self, mock_feed, feed_data):
        assert mock_feed._id == feed_data["id"]
        assert mock_feed._type == feed_data["type"]
        assert "rest_client" not in mock_feed.get_attrs_dict()
        assert "endpoint" not in mock_feed.get_attrs_dict()
        assert mock_feed.get_attrs_dict() == feed_data

    def test_get_attrs_dict_without_id(self, mock_feed, feed_data):
        del mock_feed._id
        expected_data = feed_data.copy()
        del expected_data["id"]
        assert "rest_client" not in mock_feed.get_attrs_dict()
        assert "endpoint" not in mock_feed.get_attrs_dict()
        assert mock_feed.get_attrs_dict() == expected_data

    def test_get_all(self, feed_data):
        feed_data_2 = feed_data.copy()
        for key, value in feed_data_2.items():
            if isinstance(value, str):
                feed_data_2[key] = value + "_test"
            elif isinstance(value, list):
                feed_data_2[key] = [item + "_test" for item in feed_data_2[key]]

        rest_client = Mock(spec=RestClient)
        rest_client.get.return_value = {"results": [feed_data, feed_data_2]}

        feeds = Feed.get_all(rest_client)
        assert len(feeds) == 2

        for feed in feeds:
            if feed._id.endswith("_test"):
                self.validate_feed_data(feed, rest_client, feed_data_2)
            else:
                self.validate_feed_data(feed, rest_client, feed_data)

    def test_get_id(self, mock_feed):
        assert mock_feed.get_id() == mock_feed._id

    def test_get_inorbit_id(self, mock_feed):
        expected = (
            f"{SICK_RTLS_ID_PREFIX}-{mock_feed._type}_{mock_feed._id}_{mock_feed.title}"
        )
        assert mock_feed.get_inorbit_id() == expected

    def test_get_websocket_client(self):
        rest_client = RestClient("http://localhost:8080/api", "my_api_key")

        feed = Feed(rest_client, id="my_feed_id")
        callback = MagicMock()
        client = feed.get_websocket_client(9999, callback)

        assert client.url == "ws://localhost:9999"
        assert client.headers == {"X-ApiKey": "my_api_key"}
        assert client.feed_id == "my_feed_id"
        assert client._on_message_cb == callback
