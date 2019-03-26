import logging

from base_project.common.utils.json import Json

logger = logging.getLogger(__name__)


class HeartBeatHealthCheck(Json):
    def get(self, request):
        logger.info('Common Health: OK')
        return dict(
            result='CommonOK'
        )
