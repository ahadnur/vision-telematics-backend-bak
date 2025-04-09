from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import Company, Customer  


def get_subscriber_content_type(sub_type: str) -> ContentType:
    SUBSCRIBER_TYPE_MAP = {
        'company': Company,
        'customer': Customer,
    }
    try:
        model = SUBSCRIBER_TYPE_MAP[sub_type.lower()]
        return ContentType.objects.get_for_model(model)
    except KeyError:
        raise ValueError("Invalid subscriber type")
