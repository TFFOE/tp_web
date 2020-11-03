from app.views import tags
import logging

logger = logging.getLogger(__name__)


def top_tags(request):
    return {'top_tags': tags}