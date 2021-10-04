from unittest.mock import patch

from turris_survey.__main__ import main as _main


_DEFAULT_ARGS = (
    "ipc:///tmp/sentinel_pull.sock",
    "sentinel/collect/survey",
    [
        {
            "os_version": "5.3.0",
            "enabled_pkglists": [
                {
                    "name": "datacollect",
                    "options": ["survey", "dynfw", "fwlogs", "minipot"],
                },
                {"name": "hardening", "options": ["common_passwords"]},
                {"name": "net_monitoring", "options": ["netmetr"]},
                {"name": "netdata", "options": []},
            ],
            "installed_packages": [],
        }
    ],
)


def test_main(mock_os, mock_pkglist, mock_status):
    with patch("turris_survey.__main__.send") as m:
        _main()
        m.assert_called_with(*_DEFAULT_ARGS)
