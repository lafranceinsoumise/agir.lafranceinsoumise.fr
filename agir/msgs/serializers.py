from rest_framework import serializers

from agir.events.serializers import EventSerializer
from agir.lib.serializers import FlexibleFieldsMixin
from agir.people.serializers import PersonSerializer


class BaseMessageSerializer(FlexibleFieldsMixin, serializers.Serializer):
    author = PersonSerializer("id", "fullName")
    content = serializers.CharField()
    image = serializers.ImageField()


class MessageCommentSerializer(BaseMessageSerializer):
    pass


class MessageSerializer(BaseMessageSerializer):
    linked_event = EventSerializer(
        fields=EventSerializer.EVENT_CARD_FIELDS, read_only=True,
    )
    comments = MessageCommentSerializer(many=True)
