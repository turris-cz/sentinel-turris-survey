from turris_survey.survey import (
    get_pkglists,
    get_os_version,
    collect_data,
    get_installed_pkgs,
)

_EXPECTED_DATA = {
    "os_version": "5.3.0",
    "enabled_pkglists": [
        {"name": "datacollect", "options": ["survey", "dynfw", "fwlogs", "minipot"]},
        {"name": "hardening", "options": ["common_passwords"]},
        {"name": "net_monitoring", "options": ["netmetr"]},
        {"name": "netdata", "options": []},
    ],
    "installed_packages": [],
}


def test_helper_functions(mock_pkglist, mock_status):
    assert get_pkglists() == _EXPECTED_DATA["enabled_pkglists"]
    assert get_installed_pkgs() == []


def test_get_version(mock_os):
    assert get_os_version() == "5.3.0"


def test_collect_data(mock_os, mock_pkglist, mock_status):
    data = collect_data()
    assert data == _EXPECTED_DATA
