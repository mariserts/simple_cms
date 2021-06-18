from rest_framework import serializers

from . import models


class BaseTenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Tenant
        fields = '__all__'


class BaseThingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ThingType
        fields = '__all__'


class BaseTranslatableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Translatable
        fields = '__all__'


class BaseThingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Thing
        fields = '__all__'


class TenantSerializer(BaseTenantSerializer):

    class Meta:
        model = BaseTenantSerializer.Meta.model
        exclude = [
            'created_at',
            'updated_at',
        ]


class ThingTypeSerializer(BaseThingTypeSerializer):

    class Meta:
        model = BaseThingTypeSerializer.Meta.model
        exclude = [
            'created_at',
            'updated_at',
        ]


class TranslatableSerializer(BaseTranslatableSerializer):

    class Meta:
        model = BaseTranslatableSerializer.Meta.model
        exclude = [
            'thing',
        ]


class ThingSerializer(BaseThingSerializer):

    tenant = TenantSerializer(many=False)
    thing_type = ThingTypeSerializer(many=False)
    translatables = TranslatableSerializer(many=True)
