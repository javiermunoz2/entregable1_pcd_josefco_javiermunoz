import pytest
from entregable1 import Universidad, NotFound, Repeated, Departamento


@pytest.fixture
def university():
    return Universidad('UPCT', 30203, 'CT')

def test_add_asig(university):
    university.add_asig('mates', 6)
    assert len(university._lista_asig) == 1

def test_add_prof_asoc(university):
    university.add_prof_asoc('Ana', '123456789', 'ygfadgu', 'F', Departamento.DIIC)
    assert len(university._lista_prof_asoc) == 1

def test_asignar_asig_prof(university):
    university.add_asig('mates', 6)
    university.add_prof_asoc('Ana', '123456789', 'ygfadgu', 'F', Departamento.DIIC)
    university.asignar_asig_prof('Ana', 'mates')
    assert university._lista_prof_asoc[0].listaAsig[0].nombre == 'mates'

def test_add_estudiante(university):
    university.add_estudiante('Mar', '571867890', 'fsgsh', 'F')
    assert len(university._lista_est) == 1

def test_asignar_asig_est(university):
    university.add_estudiante('Mar', '571867890', 'fsgsh', 'F')
    university.add_asig('mates', 6)
    university.asignar_asig_est('Mar', 'mates')
    assert university._lista_est[0].listaAsig[0].nombre == 'mates'

def test_del_asig_est(university):
    university.add_estudiante('Mar', '571867890', 'fsgsh', 'F')
    university.add_asig('mates', 6)
    university.asignar_asig_est('Mar', 'mates')
    university.del_asig_est('Mar', 'mates')
    assert len(university._lista_est[0].listaAsig) == 0

def test_cambiar_dep(university):
    university.add_prof_titular('rosa', '896754145', 'bvsj', 'F', 'hhs', Departamento.DIS)
    university.cambiar_dep('rosa', Departamento.DITEC)
    assert university._lista_prof_tit[0].miembro.departamento == Departamento.DITEC

def test_asignar_asig_prof_repeated(university):
    university.add_asig('mates', 6)
    university.add_prof_asoc('Ana', '123456789', 'ygfadgu', 'F', Departamento.DIIC)
    university.asignar_asig_prof('Ana', 'mates')
    with pytest.raises(Repeated):
        university.asignar_asig_prof('Ana', 'mates')

def test_asignar_asig_prof_invalid_prof(university):
    university.add_asig('mates', 6)
    with pytest.raises(NotFound):
        university.asignar_asig_prof('Ana', 'mates')

def test_asignar_asig_prof_invalid_asig(university):
    university.add_prof_asoc('Ana', '123456789', 'ygfadgu', 'F', Departamento.DIIC)
    with pytest.raises(NotFound):
        university.asignar_asig_prof('Ana', 'mates')
