from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Doctor, Patient, SpokenLanguage
from django.contrib.auth.hashers import check_password


class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=Doctor.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    spoken_languages = SpokenLanguageSerializer(many=True,read_only=True)
    class Meta:
        model = Doctor
        exclude = ("username",)

        extra_kwargs = {
            "username": {"required": False},
        }
        

    def validate(self, attrs):
        request_method = self.context["request"].method
        if request_method == "POST":
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError(
                    {"password": "Password fields didn't match."}
                )
        return attrs

    def create(self, validated_data):
        context_data = self.context['request'].data
        
        password = validated_data.pop('password')
        validated_data.pop('password2')
        validated_data["username"] = validated_data["email"]
        doctor = Doctor.objects.create(
            **validated_data
        )
        doctor.set_password(password)
        doctor.save()

        # adding languages to doctor by id

        if context_data.get("spoken_languages"):
            doctor.spoken_languages.set(context_data["spoken_languages"])
        return doctor

    def update(self, instance, validated_data):
        context_data = self.context['request'].data

        email = validated_data.get("email")
        if email:
            validated_data.pop("email")
        password = validated_data.get("password")
        new_password = validated_data.get("password2")

        if password and new_password:
            validated_data.pop("password2")
            validated_data.pop("password")
            match_check = check_password(password, instance.password)
            if match_check:
                instance.set_password(new_password)
            else:
                raise serializers.ValidationError({"password": "Password not match!"})

        if context_data.get("spoken_languages"):
            instance.spoken_languages.set(context_data["spoken_languages"])

        return super().update(instance, validated_data)

    

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


