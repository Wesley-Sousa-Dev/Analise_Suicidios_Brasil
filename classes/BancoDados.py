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
                            tipo CHAR(1) NOT NULL CHECK (tipo IN ('M', 'F'))
                        );

                        CREATE OR REPLACE VIEW genero_view AS
                        SELECT 
                            gen_cod, 
                            tipo, 
                            CASE 
                                WHEN tipo = 'M' THEN 'Homem'
                                WHEN tipo = 'F' THEN 'Mulher'
                            END AS descricao
                        FROM genero;
                      """

        tableRegiao = """
                        CREATE TABLE IF NOT EXISTS regiao (
                            reg_cod SERIAL PRIMARY KEY,
                            nome VARCHAR(3) NOT NULL CHECK (nome IN ('CO', 'SE', 'N', 'S', 'NE'))
                        );

                        CREATE OR REPLACE VIEW regiao_view AS
                        SELECT 
                            reg_cod, 
                            nome, 
                            CASE
                                WHEN nome = 'CO' THEN 'Centro-Oeste'
                                WHEN nome = 'N' THEN 'Norte'
                                WHEN nome = 'NE' THEN 'Nordeste'
                                WHEN nome = 'S' THEN 'Sul'
                                WHEN nome = 'SE' THEN 'Sudeste'
                            END AS descricao
                        FROM regiao;
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
