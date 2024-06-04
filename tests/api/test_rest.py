#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT License
# Copyright 2024 InOrbit, Inc.

# Third-party
import pytest
import requests
import requests_mock

# InOrbit
from sick_tag_loc_connector.api import RestClient


class TestRestClient:
    @pytest.fixture
    def client(self):
        return RestClient("https://fakeurl.com/", "fake_api_key")

    @pytest.fixture
    def m(self):
        with requests_mock.Mocker() as m:
            yield m

    def test_get(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        expected = {"status": "ok"}
        m.get(url, json=expected)

        response = client.get(endpoint)

        assert response == expected

    def test_post(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        expected = {"status": "ok"}
        data = {"test_key": "test_data"}
        m.post(url, json=expected)

        response = client.post(endpoint, data)

        assert response == expected

    def test_put(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        expected = {"status": "ok"}
        data = {"test_key": "test_data"}
        m.put(url, json=expected)

        response = client.put(endpoint, data)

        assert response == expected

    def test_delete(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        expected = {"status": "ok"}
        m.delete(url, json=expected)

        response = client.delete(endpoint)

        assert response == expected

    def test_get_exception(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        m.get(url, status_code=500)

        with pytest.raises(requests.exceptions.HTTPError):
            client.get(endpoint)

    def test_post_exception(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        data = {"test_key": "test_data"}
        m.post(url, status_code=500)

        with pytest.raises(requests.exceptions.HTTPError):
            client.post(endpoint, data)

    def test_put_exception(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        data = {"test_key": "test_data"}
        m.put(url, status_code=500)

        with pytest.raises(requests.exceptions.HTTPError):
            client.put(endpoint, data)

    def test_delete_exception(self, m, client):
        endpoint = "test-endpoint"
        url = f"https://fakeurl.com/{endpoint}"
        m.delete(url, status_code=500)

        with pytest.raises(requests.exceptions.HTTPError):
            client.delete(endpoint)
