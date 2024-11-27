import psycopg2 as psy
import pandas as pd
from BancoDados import BancoDados

class BancoDDL(BancoDados):
    def __init__(self, dbname, user, password, host, port):
        super().__init__(dbname, user, password, host, port)
        
    def criacao_tabelas(self):
        cursor = self.db_connect.cursor()

        #REALIZANDO CRIAÇÃO DAS TABLES
        tablePeriodo = """
                        CREATE TABLE IF NOT EXISTS periodo (
                            per_cod SERIAL PRIMARY KEY,
                            ano SMALLINT NOT NULL,
                            quantidade_total INTEGER NOT NULL
                        );
                       """

        tableGenero = """
                        CREATE TABLE IF NOT EXISTS genero (
                            gen_cod SERIAL PRIMARY KEY,
                            tipo CHAR(1) NOT NULL CHECK (tipo IN ('M', 'F')),
                            descricao VARCHAR(10) NOT NULL
                        );

                        CREATE OR REPLACE FUNCTION set_genero_descricao()
                        RETURNS TRIGGER AS $$
                        BEGIN
                            IF NEW.tipo = 'M' THEN
                                NEW.descricao := 'Masculino';
                            ELSIF NEW.tipo = 'F' THEN
                                NEW.descricao := 'Feminino';
                            END IF;
                            RETURN NEW;
                        END;
                        $$ LANGUAGE plpgsql;

                        CREATE TRIGGER genero_descricao_trigger
                        BEFORE INSERT OR UPDATE ON genero
                        FOR EACH ROW
                        EXECUTE FUNCTION set_genero_descricao();
                      """

        tableRegiao = """
                        CREATE TABLE IF NOT EXISTS regiao (
                            reg_cod SERIAL PRIMARY KEY,
                            nome VARCHAR(3) NOT NULL CHECK (nome IN ('CO', 'SE', 'N', 'S', 'NE')),
                            descricao VARCHAR(15) NOT NULL
                        );

                        CREATE OR REPLACE FUNCTION set_regiao_descricao()
                        RETURNS TRIGGER AS $$
                        BEGIN
                            IF NEW.nome = 'CO' THEN
                                NEW.descricao := 'Centro-Oeste';
                            ELSIF NEW.nome = 'N' THEN
                                NEW.descricao := 'Norte';
                            ELSIF NEW.nome = 'NE' THEN
                                NEW.descricao := 'Nordeste';
                            ELSIF NEW.nome = 'S' THEN
                                NEW.descricao := 'Sul';
                            ELSIF NEW.nome = 'SE' THEN
                                NEW.descricao := 'Sudeste';
                            END IF;
                            RETURN NEW;
                        END;
                        $$ LANGUAGE plpgsql;

                        CREATE TRIGGER regiao_descricao_trigger
                        BEFORE INSERT OR UPDATE ON regiao
                        FOR EACH ROW
                        EXECUTE FUNCTION set_regiao_descricao();
                      """
        
        tableArmaFogo = """
                        CREATE TABLE IF NOT EXISTS arma_fogo (
                            arm_cod SERIAL,
                            per_cod SMALLINT NOT NULL REFERENCES periodo(per_cod),
                            quantidade_total INTEGER NOT NULL,
                            PRIMARY KEY (arm_cod, per_cod)
                        );
                        """

        tableRel_GeneroPeriodo = """
                                CREATE TABLE IF NOT EXISTS gen_periodo (
                                    per_cod SMALLINT NOT NULL REFERENCES periodo(per_cod),
                                    gen_cod SMALLINT NOT NULL REFERENCES genero(gen_cod),
                                    quantidade INTEGER NOT NULL,
                                    PRIMARY KEY (per_cod, gen_cod)
                                );
                                 """

        tableRel_RegiaoPeriodo = """
                                CREATE TABLE IF NOT EXISTS reg_periodo (
                                    per_cod SMALLINT NOT NULL REFERENCES periodo(per_cod),
                                    reg_cod SMALLINT NOT NULL REFERENCES regiao(reg_cod),
                                    quantidade INTEGER NOT NULL,
                                    PRIMARY KEY (per_cod, reg_cod)
                                );
                                 """

        tableList = [tablePeriodo, tableGenero, tableRegiao, tableArmaFogo, tableRel_GeneroPeriodo, tableRel_RegiaoPeriodo]

        for table in tableList:
            cursor.execute(table)


        #REALIZANDO INSERÇÕES INICIAIS
        insertGenero = """
                    INSERT INTO genero (tipo) 
                    VALUES ('F'), ('M')
                    ON CONFLICT DO NOTHING;
                    """

        insertRegiao = """
                    INSERT INTO regiao (nome) 
                    VALUES ('CO'), ('N'), ('NE'), ('S'), ('SE')
                    ON CONFLICT DO NOTHING;
                    """
        
        insertList = [insertGenero, insertRegiao]

        for insert in insertList:
            cursor.execute(insert)

        self.db_connect.commit()
        print("Tabelas criadas com sucesso!")
        cursor.close()