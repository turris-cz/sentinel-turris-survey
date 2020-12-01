"""Collects information about the system and sends it to the proxy.
"""
import argparse


from . import collect_data, send


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
    send(options.socket_path, options.topic, [collect_data(), ])


if __name__ == "__main__":
    main()
