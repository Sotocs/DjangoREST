from urllib.parse import urlparse

from rest_framework import serializers


def validate_youtube_url(value):
    parsed_url = urlparse(value)

    allowed_hosts = {
        "youtube.com",
        "www.youtube.com",
        "youtu.be",
    }

    if parsed_url.scheme not in ("http", "https"):
        raise serializers.ValidationError(
            "Ссылка должна начинаться с http:// или https://."
        )

    if parsed_url.netloc.lower() not in allowed_hosts:
        raise serializers.ValidationError(
            "Можно использовать только ссылки на YouTube."
        )

    return value