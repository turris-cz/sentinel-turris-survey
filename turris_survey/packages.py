"""Collect all installed packages and information related to that.
"""
import subprocess
import svupdater.lists
import svupdater.l10n
import svupdater.autorun


def installed_packages():
    """Returns dictionary with installed packages and their versions.
    """
    result = {}
    packages = subprocess.check_output(
        ["opkg", "-V0", "list-installed"]).decode().splitlines()
    for package in packages:
        (key, val) = package.split(" - ", 1)
        result[key] = val
    return result


def updater():
    """Returns if updater is enabled.
    """
    return svupdater.autorun.enabled()


def pkglist():
    """Returns dictionary of pkglists' states.
    """
    return {pkglist: info["enabled"] for pkglist, info in
            svupdater.lists.pkglists().items()}


def languages():
    """Returns dictionary of states of languages' packages.
    """
    return svupdater.l10n.languages()
