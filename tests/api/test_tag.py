#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Standard
from unittest.mock import Mock

# Third-party
import pytest

# InOrbit
from sick_tag_loc_connector.api import Tag, RestClient, ENDPOINT_TAGS
from sick_tag_loc_connector.api.rest import FeedTypes


class TestTag:

    @staticmethod
    def validate_tag_data(tag, rest_client, tag_data):
        assert tag.rest_client is rest_client
        assert tag._id == tag_data["id"]
        assert tag._type == tag_data["type"]
        assert tag.alias == tag_data["alias"]
        assert tag.private == tag_data["private"]
        assert tag.description == tag_data["description"]
        assert tag.feed == tag_data["feed"]
        assert tag.version == tag_data["version"]
        assert tag.website == tag_data["website"]
        assert tag.tags == tag_data["tags"]
        assert tag.title == tag_data["title"]
        assert tag.updated == tag_data["updated"]
        assert tag.created == tag_data["created"]
        assert tag.creator == tag_data["creator"]
        assert id(tag) is not tag._id
        assert type(tag) is not tag._type

    @pytest.fixture
    def mock_rest_client(self):
        return Mock(spec=RestClient)

    @pytest.fixture
    def tag_data(self):
        return {
            "id": "12",
            "alias": "pizza tracker",
            "title": "0x2404638707AA",
            "private": "0",
            "description": "",
            "feed": "1.0.0",
            "updated": "2024-06-10 15:05:31.425717",
            "created": "2023-12-18 21:37:53.746653",
            "creator": "admin",
            "version": "1.0.0",
            "website": "https://pizza.com",
            "type": "tag",
            "tags": ["#yolo"],
        }

    @pytest.fixture
    def mock_tag(self, mock_rest_client, tag_data):
        tag = Tag(mock_rest_client, **tag_data)
        tag.rest_client.get.return_value = tag_data
        tag.rest_client.post.return_value = tag_data
        modified_data = tag_data.copy()
        modified_data["updated"] = "updated-now"
        tag.rest_client.put.return_value = modified_data
        tag.rest_client.delete = Mock()
        return tag

    def test_init_with_defaults(self, mock_rest_client):
        tag = Tag(mock_rest_client)
        assert tag.rest_client is mock_rest_client
        assert tag.endpoint is ENDPOINT_TAGS
        assert tag.alias is None
        assert tag.private == "0"
        assert tag.description is None
        assert tag.feed is None
        assert tag.version is None
        assert tag.website is None
        assert tag.tags == []
        assert tag._id is None
        assert tag._type is FeedTypes.TAG.value
        assert tag.title is None
        assert tag.updated is None
        assert tag.created is None
        assert tag.creator is None
        assert id(tag) is not tag._id

    def test_init_with_all_parameters_set(self, mock_rest_client, tag_data):
        tag = Tag(mock_rest_client, **tag_data)
        self.validate_tag_data(tag, mock_rest_client, tag_data)

    def test_class_method_get(self, mock_rest_client, mock_tag, tag_data):
        tag = Tag.get(mock_rest_client, "12")
        mock_rest_client.get.assert_called_once_with(f"/{ENDPOINT_TAGS}/12")
        self.validate_tag_data(tag, mock_rest_client, tag_data)

    def test_class_method_get_invalid__id(self, mock_rest_client):
        with pytest.raises(Exception):
            Tag.get(mock_rest_client, "invalid__id")
        mock_rest_client.get.assert_called_once_with(f"/{ENDPOINT_TAGS}/invalid__id")

    def test_class_method_create(self, mock_rest_client, mock_tag, tag_data):
        tag = Tag.create(mock_rest_client, tag_data)
        mock_rest_client.post.assert_called_once_with(f"/{ENDPOINT_TAGS}", tag_data)
        self.validate_tag_data(tag, mock_rest_client, tag_data)

    def test_update(self, mock_rest_client, mock_tag):
        original_data = mock_tag.get_attrs_dict()
        updated_data = {
            "alias": "update_alias",
            "private": "1",
            "description": "update_description",
            "feed": "update_feed",
            "version": "update_version",
            "website": "update_website",
            "tags": {"update_tagName"},
        }
        [setattr(mock_tag, key, value) for key, value in updated_data.items()]
        expected_data = mock_tag.get_attrs_dict()
        assert expected_data == {**original_data, **updated_data}

        mock_tag.update()
        # noinspection PyUnresolvedReferences
        mock_tag.rest_client.put.assert_called_once_with(
            f"/{ENDPOINT_TAGS}/12", expected_data
        )
        assert "updated-now" == mock_tag.updated
        assert mock_tag._id is expected_data["id"]
        assert id(mock_tag) is not mock_tag._id

    def test_save_with_existing_id(self, mock_rest_client, mock_tag):
        original_data = mock_tag.get_attrs_dict()
        updated_data = {
            "alias": "save_update_alias",
            "private": True,
            "description": "save_update_description",
            "feed": "save_update_feed",
            "version": "save_update_version",
            "website": "save_update_website",
            "tags": {"save_update_tagName"},
        }
        [setattr(mock_tag, key, value) for key, value in updated_data.items()]
        expected_data = mock_tag.get_attrs_dict()
        assert expected_data == {**original_data, **updated_data}

        mock_tag.save()
        # noinspection PyUnresolvedReferences
        mock_tag.rest_client.put.assert_called_once_with(
            f"/{ENDPOINT_TAGS}/12", expected_data
        )
        assert "updated-now" == mock_tag.updated
        assert mock_tag._id is expected_data["id"]
        assert id(mock_tag) is not mock_tag._id

    def test_save_with_no_id(self, mock_rest_client, mock_tag, tag_data):
        mock_tag.__setattr__("_id", None)
        original_data = mock_tag.get_attrs_dict()
        updated_data = {
            "alias": "save_create_alias",
            "private": True,
            "description": "save_create_description",
            "feed": "save_create_feed",
            "version": "save_create_version",
            "website": "save_create_website",
            "tags": {"save_create_tagName"},
        }
        [setattr(mock_tag, key, value) for key, value in updated_data.items()]
        expected_data = mock_tag.get_attrs_dict()
        assert expected_data == {**original_data, **updated_data}

        mock_tag.save()
        assert mock_tag._id is tag_data["id"]
        assert id(mock_tag) is not mock_tag._id
        # noinspection PyUnresolvedReferences
        mock_tag.rest_client.post.assert_called_once_with(
            f"/{ENDPOINT_TAGS}", expected_data
        )

    def test_delete(self, mock_tag):
        assert mock_tag._id == "12"
        mock_tag.delete()
        # noinspection PyUnresolvedReferences
        mock_tag.rest_client.delete.assert_called_once_with(f"/{ENDPOINT_TAGS}/12")
        assert mock_tag._id is None

    def test_get_attrs_dict(self, mock_tag, tag_data):
        assert mock_tag._id == tag_data["id"]
        assert "rest_client" not in mock_tag.get_attrs_dict()
        assert "endpoint" not in mock_tag.get_attrs_dict()
        assert mock_tag.get_attrs_dict() == tag_data

    def test_get_attrs_dict_without_id(self, mock_tag, tag_data):
        del mock_tag._id
        expected_data = tag_data.copy()
        del expected_data["id"]
        assert "rest_client" not in mock_tag.get_attrs_dict()
        assert "endpoint" not in mock_tag.get_attrs_dict()
        assert mock_tag.get_attrs_dict() == expected_data

    def test_get_all(self, tag_data):
        tag_data_2 = tag_data.copy()
        for key, value in tag_data_2.items():
            if isinstance(value, list):
                tag_data_2[key] = [item + "_test" for item in tag_data_2[key]]
            elif isinstance(value, str):
                tag_data_2[key] = value + "_test"

        rest_client = Mock(spec=RestClient)
        rest_client.get.return_value = {"results": [tag_data, tag_data_2]}

        feeds = Tag.get_all(rest_client)
        assert len(feeds) == 2

        for feed in feeds:
            if feed._id.endswith("_test"):
                self.validate_tag_data(feed, rest_client, tag_data_2)
            else:
                self.validate_tag_data(feed, rest_client, tag_data)
