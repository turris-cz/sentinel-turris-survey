import pytest

from zmq import PULL

from zmq.tests import BaseZMQTestCase


@pytest.mark.usefixtures("mock_os", "mock_pkglist", "mock_status")
class TestSend(BaseZMQTestCase):
    def test_send(self):

        from turris_survey.survey import send, collect_data

        ctx = self.Context()
        sock = ctx.socket(PULL)
        sock.bind(pytest._DEFAULT_ARGS["socket"])

        self.assertEqual(
            send(
                pytest._DEFAULT_ARGS["socket"],
                pytest._DEFAULT_ARGS["topic"],
                [
                    collect_data(),
                ],
            ),
            0,
        )
        sock.close()
