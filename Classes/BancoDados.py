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

    def insercao_dados(self, dataframe, chosenTable):
        cursor = self.db_connect.cursor()

        tables = {
            'periodo': ['ano', 'quantidade_total'],
            'genero': ['tipo', 'descricao'],
            'regiao': ['nome', 'descricao'],
            'gen_periodo': ['per_cod', 'gen_cod', 'quantidade'],
            'reg_periodo': ['per_cod', 'reg_cod', 'quantidade']
        }

        if chosenTable not in tables:
            print(f"Tabela {chosenTable} não encontrada. Verifique o nome.")
            return       
        
        table_columns = tables[chosenTable]

        placeholders = ', '.join(['%s'] * len(table_columns))
        columns = ', '.join(table_columns)
        insert_query = f"INSERT INTO {chosenTable} ({columns}) VALUES ({placeholders})"

        #Homens arma de fogo

        #Mulheres arma de fogo

        #Mulheres e homens suicídio

        #Suicidío região

        try:
            #Inserindo cada linha do DataFrame
            for _, row in dataframe.iterrows():
                values = tuple(row[col] for col in table_columns)
                cursor.execute(insert_query, values)

            self.db_connect.commit()
            print(f"Dados inseridos com sucesso na tabela {chosenTable}!")

        except Exception as e:
            self.db_connect.rollback()
            print(f"Erro ao inserir dados: {e}")

        finally:
            cursor.close()
            self.db_connect.close()
            return



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
