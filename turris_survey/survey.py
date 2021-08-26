import zmq
import msgpack
import distro


from svupdater.lists import pkglists
from svupdater.packages import Status


def get_os_version():
    """Returns current os version as string."""
    return distro.version()


def get_installed_pkgs():
    """Returns list of names (strings) of installed packages."""
    return list(name for name, pkg in Status().items() if pkg.is_installed())


def get_pkglists():
    """Returns list of dictionaries where each dict represents enabled package
    list. The dict has two keys: pkg_list and enabled_options. pkg_list is name of
    the package list and enabled_options is list of strings enumerating enabled
    options of the package list."""

    def _options(options):
        return [oname for oname, option in options.items() if option["enabled"]]

    ret = []
    for pkglist, data in pkglists().items():
        if data["enabled"]:
            ret.append({"name": pkglist, "options": _options(data["options"])})
    return ret


def collect_data():
    """Collects various system data and returns them as a dictionary."""
    return {
        "os_version": get_os_version(),
        "enabled_pkglists": get_pkglists(),
        "installed_packages": get_installed_pkgs(),
    }


def send(socket, topic, message):
    """Sends message with given topic to given socket. It returns 0 if message
    was sent succesfully, otherwise appropriate error code is returned."""
    try:
        with zmq.Context() as ctx, ctx.socket(zmq.PUSH) as zmq_sock:
            # Size (in bytes) below which messages should always be copied even if
            # in send() copy=False. The initial default value is 65536 (64kB).
            # To disable copying and allow tracking we need to turn it off.
            zmq_sock.copy_threshold = 0
            # Maximum time in ms before a send operation returns with EAGAIN.
            # = send supposed to be blocking for max 5s
            zmq_sock.setsockopt(zmq.SNDTIMEO, 5000)
            # The linger value of 0 specifies no linger period. Pending messages
            # shall be discarded immediately after close.
            # This must be set up to allow closing the socket if sending/waiting
            # for send failed, otherwise close waits untill pending messages are sent.
            zmq_sock.setsockopt(zmq.LINGER, 0)
            zmq_sock.connect(socket)
            tracker = zmq_sock.send_multipart(
                [topic.encode(), msgpack.packb(message, use_bin_type=True)],
                copy=False,
                track=True,
            )
            tracker.wait(5)
        return 0
    except (zmq.ZMQError, zmq.NotDone):
        # Send did not succeed
        return 1
