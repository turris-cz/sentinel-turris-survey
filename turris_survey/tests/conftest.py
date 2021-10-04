import pytest

import json

from unittest.mock import patch, Mock, MagicMock

pytest._DEFAULT_ARGS = {  # defaults as defined in CLI app
    "topic": "sentinel/collect/survey",
    "socket": "ipc:///tmp/sentinel_pull.sock",
}


def _load_data(module):
    with open(f"turris_survey/tests/test_data/{module}.json") as file:
        return json.load(file)


@pytest.fixture
def mock_os():
    with patch("turris_survey.survey.distro.version", return_value="5.3.0") as o:
        yield o


@pytest.fixture
def mock_pkglist():
    with patch(
        "turris_survey.survey.pkglists", return_value=_load_data("pkglist")
    ) as p:
        yield p


@pytest.fixture
def mock_status():
    item_mock = Mock()
    item_mock.is_installed.return_value = True

    patched_status = MagicMock()
    patched_status.__getitem__.return_value = item_mock

    with patch("turris_survey.survey.Status", return_value=patched_status) as m:
        yield m
