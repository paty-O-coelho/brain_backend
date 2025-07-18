from rest_framework import serializers
from .models import Producer, Farm, Harvest, Crop

"""
Serializa os dados do modelo Crop (cultura agrícola).
É usado em leitura e escrita simples.
"""


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = "__all__"


"""
Serializa o modelo Harvest (safra), que possui apenas o campo "year".
"""


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = "__all__"


"""
Serializa o modelo Farm (fazenda), incluindo as culturas (crops) relacionadas.
Realiza validação customizada para garantir que a soma das áreas de cultivo e vegetação
não ultrapasse a área total da fazenda.
"""


class FarmSerializer(serializers.ModelSerializer):
    crops = CropSerializer(
        many=True, read_only=True
    )  # Relação reversa: uma fazenda pode ter várias culturas

    class Meta:
        model = Farm
        fields = "__all__"

    def validate(self, data):
        if data["farming_area"] + data["vegetation_area"] > data["total_area"]:
            raise serializers.ValidationError(
                "Área agricultável + vegetação não pode exceder a área total."
            )
        return data

"""
Serializa o modelo Producer (produtor rural), incluindo suas fazendas.
A relação com as fazendas é apenas leitura (read_only).
"""
class ProducerSerializer(serializers.ModelSerializer):
    farms = FarmSerializer(
        many=True, read_only=True
    )  # Um produtor pode ter várias fazendas

    class Meta:
        model = Producer
        fields = "__all__"
