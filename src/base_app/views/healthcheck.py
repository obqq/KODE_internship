import logging

from base_app.utils.json import Json

logger = logging.getLogger(__name__)


class HeartBeatHealthCheck(Json):
    def get(self, request):
        logger.info('Common Health: OK')
        return dict(
            result='CommonOK'
        )
