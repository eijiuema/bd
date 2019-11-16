from faker import Faker
import datetime
import random
import io

OUTPUT = "populate.sql"

N_PESSOAS = range(1000)
N_MEDICOS = range(0, 100)
N_PACIENTES = range(90, 800)
N_ENFERMEIROS = range(780, 1000)
N_QUARTOS = 50

CHANCE_MULTIPLOS_CORENS = 5 # %
CHANCE_CONTATO_EMERGENCIA = 95 # %

MIN_VISITAS_ENFERMEIRO = 5 # vezes
MAX_VISITAS_ENFERMEIRO = 30 # vezes
MIN_TEMPO_VISITA = 15 # minutos
MAX_TEMPO_VISITA = 60 # minutos

CHANCE_INTERNACAO = 15 # %
MIN_TEMPO_INTERNACAO = 5 # dias
MAX_TEMPO_INTERNACAO = 185 # dias

CHANCE_MULTIPLOS_ATENDIMENTOS = 25 # %

fake = Faker('pt_BR')

tabelas = {
    'pessoa': [],
    'medico': [],
    'paciente': [],
    'enfermeiro': [],
    'quarto': [],
    'coren': [],
    'contato_emergencia': [],
    'atendimento': [],
    'visita': [],
    'interna': [],
}

especialidades = [
    'Pediatra',
    'Clínica Médica',
    'Cirurgião Geral',
    'Cardiologista',
    'Psiquiatra',
    'Ortopedista',
    'Ginecologista',
    'Infectologista',
    'Oncologista'
]

tipo_sanguineo = ['A-', 'A+', 'B-', 'B+', 'AB-', 'AB+', 'O-', 'O+']

setores = ['Clínico', 'Cirúrgico', 'Obstétrico', 'Pediátrico']

rgs = set()

while (len(rgs) < 1000):
    rgs.add(fake.rg())

for i in N_PESSOAS:
    tabelas['pessoa'].append({
        'rg': rgs.pop(),
        'nome': fake.name(),
        'telefone_1': fake.phone_number(),
        'telefone_2': fake.phone_number(),
    })

for i in N_MEDICOS:
    tabelas['medico'].append({
        'rg': tabelas['pessoa'][i]['rg'],
        'especialidade': random.choice(especialidades),
        'crm': random.randint(1000, 999999)
    })

for i in N_PACIENTES:
    tabelas['paciente'].append({
        'rg': tabelas['pessoa'][i]['rg'],
        'tipo_sanguineo': random.choice(tipo_sanguineo),
        'data_nascimento': fake.date_of_birth(),
        'endereco': fake.address().replace("'", "''")
    })

for i in N_ENFERMEIROS:
    tabelas['enfermeiro'].append({
        'rg': tabelas['pessoa'][i]['rg'],
        'setor': random.choice(setores)
    })

for i in range(N_QUARTOS):
    tabelas['quarto'].append({
        'numero': i,
        'numero_de_leitos': random.randint(1, 5)
    })

for enfermeiro in tabelas['enfermeiro']:

    tabelas['coren'].append({
        'rg_enfermeiro': enfermeiro['rg'],
        'coren': random.randint(1000, 999999)
    })

    while(random.randint(1, 100) <= CHANCE_MULTIPLOS_CORENS):
        tabelas['coren'].append({
            'rg_enfermeiro': enfermeiro['rg'],
            'coren': random.randint(1000, 999999)
        })

    for i in range(MIN_VISITAS_ENFERMEIRO, MAX_VISITAS_ENFERMEIRO):
        data = fake.past_datetime()
        hora_saida = data + datetime.timedelta(minutes=random.randint(MIN_TEMPO_VISITA, MAX_TEMPO_VISITA))
        tabelas['visita'].append({
            'rg_enfermeiro': enfermeiro['rg'],
            'data': data.date(),
            'hora_entrada': data.time(),
            'hora_saida': hora_saida,
            'numero_quarto': random.choice(tabelas['quarto'])['numero']
        })

for paciente in tabelas['paciente']:

    if random.randint(1, 100) <= CHANCE_CONTATO_EMERGENCIA:
        tabelas['contato_emergencia'].append({
            'rg_paciente': paciente['rg'],
            'nome': fake.name(),
            'telefone': fake.phone_number()
        })

    if random.randint(1, 100) <= CHANCE_INTERNACAO:
        data = fake.past_datetime()
        data_saida = data + datetime.timedelta(days=random.randint(MIN_TEMPO_INTERNACAO, MAX_TEMPO_INTERNACAO))
        tabelas['interna'].append({
            'rg_paciente': paciente['rg'],
            'numero_quarto': random.choice(tabelas['quarto'])['numero'],
            'data_entrada': data.date(),
            'data_saida': data_saida.date()
        })

    medico = random.choice(tabelas['medico'])
    while medico['rg'] == paciente['rg']:
        medico = random.choice(tabelas['medico'])

    tabelas['atendimento'].append({
        'rg_medico': medico['rg'],
        'rg_paciente': paciente['rg'],
        'data': fake.past_date()
    })

    while random.randint(1, 100) <= CHANCE_MULTIPLOS_ATENDIMENTOS:
        medico = random.choice(tabelas['medico'])
        while medico['rg'] == paciente['rg']:
            random.choice(tabelas['medico'])

        tabelas['atendimento'].append({
            'rg_medico': medico['rg'],
            'rg_paciente': paciente['rg'],
            'data': fake.past_date()
        })

with io.open(OUTPUT, 'w', encoding="utf8") as output:
    for tabela in tabelas:
        for linha in tabelas[tabela]:
            output.write("INSERT INTO " + tabela + " VALUES ('" +
                         '\',\''.join(map(str, linha.values())) + "');\n")
