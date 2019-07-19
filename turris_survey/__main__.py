"""Collects information about the system and sends it to the proxy.
"""
import argparse
import zmq
import msgpack
from turris_survey import packages
from turris_survey import osinfo


def send(socket,topic,message):
    """ Sends message with given topic to given socket.
    """
    with zmq.Context() as context, context.socket(zmq.PUSH) as zmq_sock:
        #Maximum time before a send operation returns with EAGAIN
        #-1 = it will block until the message is sent
        zmq_sock.setsockopt(zmq.SNDTIMEO, -1)
        #The linger period determines how long pending messages which have yet to be sent to a peer shall linger in memory after a socket is closed
        #-1 = an infinite linger period. Pending messages shall not be discarded after close.
        # It shall block until all pending messages have been sent to a peer.
        zmq_sock.setsockopt(zmq.LINGER, -1)
        zmq_sock.connect(socket)
        tracker = zmq_sock.send_multipart([topic.encode(), msgpack.packb(message, use_bin_type=True)],0,False,True)
        #wait for frames release
        tracker.wait()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--socket", dest='socket_path',
        default='ipc:///tmp/sentinel_pull.sock',
        type=str, help='set the socket path'
    )
    parser.add_argument(
        "-T", "--topic", dest='topic', default='sentinel/collect/survey',
        type=str, help='topic'
    )

    options = parser.parse_args()
    topic = options.topic
    socket_path = options.socket_path

    data = {}
    data["os_info"] = osinfo.os_info()
    data["updater_enabled"] = packages.updater()
    data["pkglist"] = packages.pkglist()
    data["langs"] = packages.languages()
    data["installed_packages"] = packages.installed_packages()
    send(socket_path, topic, [data,])


if __name__ == "__main__":
    main()
