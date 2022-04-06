from rest_framework import serializers

from watchlist_app.models import Movie


# field level validators
def check_name(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is Too Short !")
    else:
        return value

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=80, validators=[check_name,])
    description = serializers.CharField(max_length=300)
    active = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    # # field level validation
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is Too Short!!")
    #     else:
    #         return value
    
    # object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Description can not be Same.")
        else:
            return data