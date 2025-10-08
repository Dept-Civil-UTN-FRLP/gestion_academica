import pytest
from django.contrib.auth.models import User
from apps.usuarios.models import UserProfile
from apps.core.models import Departamento


@pytest.mark.django_db
def test_creacion_perfil_usuario():
    user = User.objects.create_user(username="jorge", password="1234")
    perfil = UserProfile.objects.create(user=user, telefono="123456789")
    assert perfil.user.username == "jorge"
    assert perfil.telefono == "123456789"
    assert str(perfil) == "Perfil de jorge"


@pytest.mark.django_db
def test_acceso_departamento_por_asignacion():
    user = User.objects.create_user(username="maria", password="abcd")
    perfil = UserProfile.objects.create(user=user)
    departamento = Departamento.objects.create(nombre="Ingeniería Civil")
    perfil.departamentos.add(departamento)

    assert perfil.tiene_acceso_departamento(departamento) is True


@pytest.mark.django_db
def test_acceso_departamento_denegado():
    user = User.objects.create_user(username="carlos", password="xyz")
    perfil = UserProfile.objects.create(user=user)
    otro_dep = Departamento.objects.create(nombre="Electrónica")

    assert perfil.tiene_acceso_departamento(otro_dep) is False


@pytest.mark.django_db
def test_superadmin_tiene_acceso_a_todo():
    user = User.objects.create_user(username="admin", password="admin")
    perfil = UserProfile.objects.create(user=user, es_superadmin=True)
    dep = Departamento.objects.create(nombre="Civil")

    # Aunque no tenga asignado el departamento, debe tener acceso
    assert perfil.tiene_acceso_departamento(dep) is True
