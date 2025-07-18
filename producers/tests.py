import pytest
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from producers.models import Producer, Farm, Harvest, Crop
from producers.serializers import FarmSerializer

pytestmark = pytest.mark.django_db

client = APIClient()

### MODELS ###

def test_create_valid_producer():
    # cria e espera o mesmo valor que foi passado
    producer = Producer.objects.create(name="João", cpf_cnpj="123.456.789-09")
    assert producer.name == "João"
    assert producer.cpf_cnpj == "123.456.789-09"

def test_invalid_cpf_cnpj():
    with pytest.raises(ValidationError):
        Producer(name="Ana", cpf_cnpj="123").full_clean()

def test_create_farm_valid_area():
    producer = Producer.objects.create(name="Maria", cpf_cnpj="123.456.789-09")
    farm = Farm.objects.create(
        producer=producer,
        name="Fazenda Verde",
        city="Fortaleza",
        state="CE",
        total_area=100,
        farming_area=50,
        vegetation_area=50,
    )
    assert farm.name == "Fazenda Verde"

def test_farm_invalid_area_sum():
    producer = Producer.objects.create(name="Lucas", cpf_cnpj="987.654.321-00")
    farm = Farm(
        producer=producer,
        name="Fazenda Azul",
        city="Sobral",
        state="CE",
        total_area=100,
        farming_area=60,
        vegetation_area=50,
    )
    with pytest.raises(ValidationError):
        farm.full_clean()

def test_unique_harvest_year():
    Harvest.objects.create(year="2024")
    with pytest.raises(ValidationError):
        h = Harvest(year="2024")
        h.full_clean()

### SERIALIZERS ###

def test_farm_serializer_valid():
    producer = Producer.objects.create(name="João", cpf_cnpj="111.222.333-44")
    data = {
        "producer": producer.id,
        "name": "Fazenda Nova",
        "city": "Quixadá",
        "state": "CE",
        "total_area": 200,
        "farming_area": 100,
        "vegetation_area": 50,
    }
    serializer = FarmSerializer(data=data)
    assert serializer.is_valid()

def test_farm_serializer_invalid_area():
    producer = Producer.objects.create(name="Carlos", cpf_cnpj="999.888.777-66")
    data = {
        "producer": producer.id,
        "name": "Fazenda Teste",
        "city": "Limoeiro",
        "state": "CE",
        "total_area": 100,
        "farming_area": 80,
        "vegetation_area": 30,
    }
    serializer = FarmSerializer(data=data)
    assert not serializer.is_valid()
    # aqui verificamos se a mensagem de erro do serializer aparece
    assert "Área agricultável + vegetação" in str(serializer.errors)

### API / VIEWS ###

def _len_response_list(resp):
    """
    Helper para lidar com APIs paginadas (retornam {'results': [...]})
    ou APIs que retornam uma list diretamente.
    """
    data = resp.data
    if isinstance(data, dict) and "results" in data:
        return len(data["results"])
    if isinstance(data, list):
        return len(data)
    # fallback: tentar converter para json e contar
    try:
        return len(resp.json().get("results", resp.json()))
    except Exception:
        return 0

def test_api_create_producer():
    payload = {
        "name": "Joana",
        "cpf_cnpj": "123.456.789-00",
    }
    response = client.post("/api/producers/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Joana"

def test_api_list_farms():
    producer = Producer.objects.create(name="Fernanda", cpf_cnpj="111.111.111-11")
    Farm.objects.create(
        producer=producer,
        name="Fazenda X",
        city="Caucaia",
        state="CE",
        total_area=100,
        farming_area=40,
        vegetation_area=40,
    )
    response = client.get("/api/farms/")
    assert response.status_code == status.HTTP_200_OK
    assert _len_response_list(response) == 1

def test_api_invalid_crop_duplicate():
    producer = Producer.objects.create(name="Zé", cpf_cnpj="123.123.123-12")
    farm = Farm.objects.create(
        producer=producer,
        name="Fazenda Y",
        city="Maracanaú",
        state="CE",
        total_area=150,
        farming_area=70,
        vegetation_area=60,
    )
    harvest = Harvest.objects.create(year="2025")
    Crop.objects.create(farm=farm, harvest=harvest, name="Milho")

    with pytest.raises(ValidationError):
        duplicate_crop = Crop(farm=farm, harvest=harvest, name="Milho")
        duplicate_crop.full_clean()
