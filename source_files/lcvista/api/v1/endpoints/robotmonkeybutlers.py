from rest_framework import serializers, viewsets
from django.db.models import Q
import django_filters
from django.db import transaction
from lcvista.api.auditable import AuditableSerializerMixin
from lcvista.robotmonkeybutlers.models import RobotMonkeyButler
from rest_framework.permissions import IsAuthenticated
from lcvista.utils.filters import (
    CharFilter,
    CharInFilter,
)


class RobotMonkeyButlerFilterSet(django_filters.FilterSet):
    id__in = CharInFilter(name='id', lookup_expr='in')
    name_is_monkey = CharFilter(name='name_is_monkey', method='filter_name_is_monkey')

    def filter_name_is_monkey(self, queryset, name, value):
        # A silly example filter that queries by: name="monkey " + value
        capitalized_monkey = Q(**{'name': 'Monkey {}'.format(value)})
        lowercase_monkey = Q(**{'name': 'monkey {}'.format(value)})
        return queryset.filter(lowercase_monkey | capitalized_monkey)

    class Meta:
        model = RobotMonkeyButler
        fields = {
            'name': ['exact'],
        }


class RobotMonkeyButlerSerializer(AuditableSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = RobotMonkeyButler
        fields = (
            'id',
            'name',
        )
        read_only_fields = (
        )

    def validate(self, data):
        return data

    @transaction.atomic
    def create(self, validated_data):
        if validated_data.get('name') == "Robots are cool!":
            raise Exception('Yes they are!  But thats not a valid name')
        instance = super(RobotMonkeyButlerSerializer, self).create(validated_data)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('name') == "Monkeys are bananas!":
            raise Exception('Yes they are!  But thats not a valid name')
        instance = super(RobotMonkeyButlerSerializer, self).update(instance, validated_data)
        return instance


class RobotMonkeyButlerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = RobotMonkeyButler.objects.all()
    serializer_class = RobotMonkeyButlerSerializer
    filter_class = RobotMonkeyButlerFilterSet
    search_fields = ('name',)
    ordering_fields = ('name',)

    # def destroy(self, request, *args, **kwargs):  # (destroy goes on the ViewSet)
    #     raise Exception("Delete not allowed via endpoint")
