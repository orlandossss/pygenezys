import pytest
import requests
import responses
from pygenezys.exceptions import GenezysAPIError, GenezysAuthError, GenezysConnectionError


@responses.activate
def test_auth_error_on_401(client):
    responses.add(responses.GET, "https://example.com/test", status=401)
    with pytest.raises(GenezysAuthError):
        client._request("GET", "https://example.com/test")


@responses.activate
def test_api_error_on_bad_status(client):
    responses.add(responses.GET, "https://example.com/test", status=500)
    with pytest.raises(GenezysAPIError):
        client._request("GET", "https://example.com/test")


@responses.activate
def test_api_error_on_invalid_json(client):
    responses.add(responses.GET, "https://example.com/test", body="not json", status=200)
    with pytest.raises(GenezysAPIError):
        client._request("GET", "https://example.com/test")


@responses.activate
def test_connection_error_wrapped(client):
    responses.add(responses.GET, "https://example.com/test", body=requests.exceptions.ConnectionError("boom"))
    with pytest.raises(GenezysConnectionError):
        client._request("GET", "https://example.com/test")


def test_set_token_updates_header(client):
    client.set_token("new-token")
    assert client.session.headers["Authorization"] == "new-token"
