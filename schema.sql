DROP TABLE IF EXISTS interna;
DROP TABLE IF EXISTS visita;
DROP TABLE IF EXISTS atendimento;
DROP TABLE IF EXISTS contato_emergencia;
DROP TABLE IF EXISTS coren;
DROP TABLE IF EXISTS quarto;
DROP TABLE IF EXISTS medico;
DROP TABLE IF EXISTS paciente;
DROP TABLE IF EXISTS enfermeiro;
DROP TABLE IF EXISTS pessoa;

CREATE TABLE pessoa(
    rg          varchar PRIMARY KEY,
    nome        varchar NOT NULL,
    telefone_1  varchar,
    telefone_2  varchar
);

CREATE TABLE paciente(
    rg              varchar PRIMARY KEY,
    tipo_sanguineo  char(3) NOT NULL,
    data_nascimento date NOT NULL,
    endereco        varchar NOT NULL,

    CONSTRAINT chk_tipo_sanguineo CHECK (tipo_sanguineo IN ('A-', 'A+', 'B-', 'B+', 'AB-', 'AB+', 'O-', 'O+')),
    FOREIGN KEY (rg) REFERENCES pessoa(rg)
);

CREATE TABLE medico(
    rg              varchar PRIMARY KEY,
    especialidade   varchar NOT NULL,
    crm             varchar NOT NULL,

    CONSTRAINT chk_especialidade CHECK (especialidade IN ('Pediatra', 'Clínica Médica', 'Cirurgião Geral', 'Cardiologista', 'Psiquiatra', 'Ortopedista', 'Ginecologista', 'Infectologista', 'Oncologista')),
    FOREIGN KEY (rg) REFERENCES pessoa(rg)
);

CREATE TABLE quarto(
    numero integer PRIMARY KEY,
    numero_de_leitos smallint NOT NULL,

    CONSTRAINT chk_numero_de_leitos CHECK (numero_de_leitos > 0)
);

CREATE TABLE enfermeiro(
    rg      varchar PRIMARY KEY,
    setor   varchar NOT NULL,
    
    CONSTRAINT chk_setor CHECK (setor IN ('Clínico', 'Cirúrgico', 'Obstétrico', 'Pediátrico')),
    FOREIGN KEY (rg) REFERENCES pessoa(rg)
);

CREATE TABLE coren(
    rg_enfermeiro varchar,
    coren varchar,

    PRIMARY KEY (rg_enfermeiro, coren),
    FOREIGN KEY (rg_enfermeiro) REFERENCES enfermeiro(rg) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE contato_emergencia(
    rg_paciente VARCHAR,
    nome varchar,
    telefone varchar NOT NULL,

    PRIMARY KEY (rg_paciente, nome),
    FOREIGN KEY (rg_paciente) REFERENCES paciente(rg) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE atendimento(
    rg_medico varchar,
    rg_paciente varchar,
    data date,

    PRIMARY KEY (rg_medico, rg_paciente, data),
    FOREIGN KEY (rg_medico) REFERENCES medico(rg),
    FOREIGN KEY (rg_paciente) REFERENCES paciente(rg)
);

CREATE TABLE visita(
    rg_enfermeiro varchar,
    data date,
    hora_entrada time,
    hora_saida time,
    numero_quarto smallint,

    PRIMARY KEY (rg_enfermeiro, data, hora_entrada, numero_quarto),
    FOREIGN KEY (rg_enfermeiro) REFERENCES enfermeiro(rg),
    FOREIGN KEY (numero_quarto) REFERENCES quarto(numero)
);

CREATE TABLE interna(
    rg_paciente varchar,
    numero_quarto smallint,
    data_entrada date,
    data_saida date,
    
    PRIMARY KEY (rg_paciente, numero_quarto, data_entrada),
    FOREIGN KEY (rg_paciente) REFERENCES paciente(rg),
    FOREIGN KEY (numero_quarto) REFERENCES quarto(numero)
);