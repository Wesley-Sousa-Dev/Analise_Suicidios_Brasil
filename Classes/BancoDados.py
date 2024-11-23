import psycopg2 as psy

class BancoDados:
    def __init__(self, dbname, user, password, host, port):
        try:
            self.db_connect = psy.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Conexão bem-sucedida!")
        except Exception as e:
            print(f"Erro ao conectar: {e}")

    def criacao_tabelas(self):
        cursor = self.db_connect.cursor()

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
                                NEW.descricao := 'Homem';
                            ELSIF NEW.tipo = 'F' THEN
                                NEW.descricao := 'Mulher';
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

        tableList = [tablePeriodo, tableGenero, tableRegiao, tableRel_GeneroPeriodo, tableRel_RegiaoPeriodo]

        for table in tableList:
            cursor.execute(table)
        self.db_connect.commit()
        print("Tabelas criadas com sucesso!")
        cursor.close()
        self.db_connect.close()


        def insercao_dados(self, csv):
            cursor = self.db_connect.cursor()
            print("Método não feito ainda chefia")
            cursor.close()