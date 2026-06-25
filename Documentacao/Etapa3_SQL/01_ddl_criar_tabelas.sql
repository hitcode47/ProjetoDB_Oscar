-- =============================================================
-- Oscar AMPAS — Winner Demographics — DDL
-- Disciplina: Banco de Dados — DCC/UFMG
-- =============================================================

-- Remove tabelas na ordem correta (dependentes primeiro)
DROP TABLE IF EXISTS premio         CASCADE;
DROP TABLE IF EXISTS filme          CASCADE;
DROP TABLE IF EXISTS categoria      CASCADE;
DROP TABLE IF EXISTS pais           CASCADE;
DROP TABLE IF EXISTS etnia          CASCADE;
DROP TABLE IF EXISTS religiao       CASCADE;
DROP TABLE IF EXISTS orient_sexual  CASCADE;
DROP TABLE IF EXISTS vencedor       CASCADE;
DROP TABLE IF EXISTS edicao         CASCADE;

-- -------------------------------------------------------------
-- Tabelas de domínio (sem FKs)
-- -------------------------------------------------------------

CREATE TABLE edicao (
    id_edicao SERIAL PRIMARY KEY,
    ano       INTEGER NOT NULL,
    CONSTRAINT uq_edicao_ano UNIQUE (ano),
    CONSTRAINT ck_edicao_ano CHECK (ano >= 1927)
);

CREATE TABLE categoria (
    id_categoria SERIAL PRIMARY KEY,
    nome         VARCHAR(100) NOT NULL,
    CONSTRAINT uq_categoria_nome UNIQUE (nome)
);

CREATE TABLE filme (
    id_filme SERIAL PRIMARY KEY,
    titulo   VARCHAR(255) NOT NULL,
    CONSTRAINT uq_filme_titulo UNIQUE (titulo)
);

CREATE TABLE pais (
    nome_pais VARCHAR(255) PRIMARY KEY
);

CREATE TABLE etnia (
    nome_etnia VARCHAR(50) PRIMARY KEY
);

CREATE TABLE religiao (
    nome_religiao VARCHAR(100) PRIMARY KEY
);

CREATE TABLE orient_sexual (
    nome_orient_sexual VARCHAR(50) PRIMARY KEY
);

CREATE TABLE vencedor (
    id_vencedor      SERIAL PRIMARY KEY,
    nome             VARCHAR(150) NOT NULL,
    ano_nascimento   INTEGER,
    pais_nascimento  VARCHAR(200) NOT NULL REFERENCES pais(nome_pais),
    nome_etnia            VARCHAR(50)  NOT NULL REFERENCES etnia(nome_etnia),
    nome_religiao         VARCHAR(100) REFERENCES religiao(nome_religiao),
    nome_orient_sexual    VARCHAR(50) REFERENCES orient_sexual(nome_orient_sexual),
    CONSTRAINT uq_vencedor_nome UNIQUE (nome)
    CONSTRAINT chk_mesmo_ano CHECK (ano_nascimento = EXTRACT(YEAR FROM data_nascimento))
);

-- -------------------------------------------------------------
-- Tabela central
-- -------------------------------------------------------------

CREATE TABLE premio (
    id_premio    SERIAL PRIMARY KEY,
    id_vencedor  INTEGER NOT NULL REFERENCES vencedor(id_vencedor),
    id_filme     INTEGER NOT NULL REFERENCES filme(id_filme),
    id_categoria INTEGER NOT NULL REFERENCES categoria(id_categoria),
    id_edicao    INTEGER NOT NULL REFERENCES edicao(id_edicao),

    -- Uma pessoa não ganha a mesma categoria duas vezes na mesma edição
    CONSTRAINT uq_premio UNIQUE (id_vencedor, id_categoria, id_edicao)
);

-- -------------------------------------------------------------
-- Índices para acelerar as consultas mais comuns
-- -------------------------------------------------------------

CREATE INDEX idx_premio_vencedor  ON premio(id_vencedor);
CREATE INDEX idx_premio_filme     ON premio(id_filme);
CREATE INDEX idx_premio_categoria ON premio(id_categoria);
CREATE INDEX idx_premio_edicao    ON premio(id_edicao);
