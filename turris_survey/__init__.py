import zmq
import msgpack
import distro


from svupdater.lists import pkglists
from svupdater.packages import Status


def get_os_version():
    """ Returns current os version as string. """
    return distro.version()


def get_installed_pkgs():
    """ Returns list of names (strings) of installed packages. """
    return list(name for name, pkg in Status().items() if pkg.is_installed())


def get_pkglists():
    """ Returns list of dictionaries where each dict represents enabled package
    list. The dict has two keys: pkg_list and enabled_options. pkg_list is name of
    the package list and enabled_options is list of strings enumerating enabled
    options of the package list. """
    def _options(options):
        return [oname for oname, option in options.items() if option["enabled"]]

    ret = []
    for pkglist, data in pkglists().items():
        if data["enabled"]:
            ret.append({"name": pkglist,
                        "options": _options(data["options"])})
    return ret


def collect_data():
    """ Collects various system data and returns them as a dictionary. """
    return {
        "os_version": get_os_version(),
        "enabled_pkglists": get_pkglists(),
        "installed_packages": get_installed_pkgs(),
    }


def send(socket, topic, message):
    """ Sends message with given topic to given socket. """
    with zmq.Context() as context, context.socket(zmq.PUSH) as zmq_sock:
        # Maximum time before a send operation returns with EAGAIN
        # -1 = it will block until the message is sent
        zmq_sock.setsockopt(zmq.SNDTIMEO, -1)
        # The linger period determines how long pending messages which have
        # yet to be sent to a peer shall linger in memory after a socket
        # is closed
        # -1 = an infinite linger period. Pending messages shall not be
        # discarded after close.
        # It shall block until all pending messages have been sent to a peer.
        zmq_sock.setsockopt(zmq.LINGER, -1)
        zmq_sock.connect(socket)
        tracker = zmq_sock.send_multipart(
            [topic.encode(), msgpack.packb(message, use_bin_type=True)],
            0, False, True)
        # Wait for frames release
        tracker.wait()
