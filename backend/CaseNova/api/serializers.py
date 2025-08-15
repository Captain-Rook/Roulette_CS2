import base64

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cases.models import Case, Skin, SkinTransaction
from authentication.models import User
from django.core.files.base import ContentFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'balance', 'username', 'avatar', 'steam_profile_url', 'steam_id', 'trade_url')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class SkinReadSerializer(serializers.ModelSerializer):
    skin_image = serializers.SerializerMethodField()

    class Meta:
        model = Skin
        fields = ('id', 'weapon', 'price', 'fullname', 'skin_image', 'rare')

    def get_skin_image(self, skin_object):
        if skin_object.skin_image:
            return skin_object.skin_image.url
        return None


class SkinWriteSerializer(serializers.ModelSerializer):
    skin_image = Base64ImageField()

    class Meta:
        model = Skin
        fields = ('id', 'weapon', 'price', 'fullname', 'skin_image', 'rare')

    def to_representation(self, skin_object):
        return SkinReadSerializer(skin_object).data


class CaseWriteSerializer(serializers.ModelSerializer):
    skins = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skin.objects.all()
    )
    image = Base64ImageField()

    class Meta:
        model = Case
        fields = ('id', 'name', 'price', 'created_at', 'skins', 'image')

    def create(self, validated_data):
        skins = validated_data.pop('skins')
        case_object = Case.objects.create(**validated_data)
        case_object.skins.set(skins)
        return case_object

    def to_representation(self, case_object):
        return CaseReadSerializer(case_object, context=self.context).data


class CaseReadSerializer(serializers.ModelSerializer):
    skins = SkinReadSerializer(
        many=True,
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ('id', 'name', 'price', 'created_at', 'skins', 'image')
        read_only_fields = fields

    def get_image(self, case_object):
        if case_object.image:
            return case_object.image.url
        return None


class SkinTransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    skin = SkinReadSerializer()

    class Meta:
        model = SkinTransaction
        fields = ('id', 'user', 'details', 'skin', 'source',
                  'action', 'get_at', 'used_at')


class OpenCaseSerializer(serializers.Serializer):
    case_id = serializers.IntegerField()


class UpgradeSerializer(serializers.Serializer):
    used_skins = serializers.PrimaryKeyRelatedField(
        many=True, queryset=SkinTransaction.objects.all())
    expected_skin = serializers.PrimaryKeyRelatedField(queryset=Skin.objects.all())
    used_balance = serializers.IntegerField()

    class Meta:
        fields = ('used_skins', 'used_balance', 'expected_skin')

    def validate(self, data):
        user = self.context['request'].user
        user_balance = data['used_balance']
        expected_skin = data['expected_skin']
        used_skins = data['used_skins']
        user_skins = SkinTransaction.objects.filter(user=user).values_list('skin_id', flat=True)
        for skin in used_skins:
            if skin.id not in user_skins:
                raise ValidationError(f'У пользователя отсутствует скин с id {skin.id}')
        
        deposit_summ = sum([skin.price for skin in used_skins]) + user_balance
        if deposit_summ >= expected_skin.price:
            raise ValidationError(
                'Цена результирующего скина должна быть больше суммы цен используемых скинов'
            )
        return data
