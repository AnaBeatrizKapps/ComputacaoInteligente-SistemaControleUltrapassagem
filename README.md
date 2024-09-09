## Trabalho Computação Inteligente - Exercício Central de Peças e Trabalho de ultrapassagem de um veículo

### Controle de ultrapassagem de um veículo:

#### variáveis de inferência

```
1. distância_adequada(da) - distância adequada para ultrapassagem
2. permissao_ultrapassagem(pu) - se o trecho da estrada permite ultrapassagem
3. pista_livre(pl) - se a pista contrária está livre
4. velocidade_veiculo_frente(vvf) - se a velocidade do veículo a frente é adequada
5. visibilidade(v) - se o trecho da estrada tem boas condições de visibilidade
```

#### variáveis de entrada:
```
da,pl,vvf,v
```

#### variável de saída:
```
pu
```

### variáveis linguísticas:

Tabela 1 - variável distância adequada para ultrapassagem (da)

| Termo | Representação   | Intervalo numérico |
| -------------- | ----------- | ----------- |
| Boa | B | [3,...,6]|
| Média| M | [6,...,9] |
| Ruim | R | [9,...,12] |

Tabela 2 - variável permissão para ultrapassagem (pu)

| Termo | Representação |
| -------------- | ----------- |
| Negada | N |
| Permitida| P |

Tabela 3 - variável verificação pista livre (pl)

| Termo | Representação |
| -------------- | ----------- |
| Livre | L |
| Obstruída| O |

Tabela  4 - variável velocidade do  veículo a frente (vvf)

| Termo | Representação   | Intervalo numérico |
| -------------- | ----------- | ----------- |
| Rápida | R | [90,...,200]|
| Adequada| A | [60,...,90] |
| Lenta | L | [0,..,60] |

Tabela 5 - variável visibilidade (v)

| Termo | Representação |
| -------------- | ----------- |
| Ruim | R |
| Boa| B |

### Regras de inferência

```
1. IF (da is B) AND (pl is L) AND (v is B) AND (vvf is A) THEN (pu is P)
2. IF (da is M) AND (pl is L) AND (v is B) AND (vvf is A) THEN (pu is P)
3. IF (da is R) AND (pl is O) AND (v is R) AND (vvf is L) THEN (pu is N)
4. IF (da is B) AND (pl is L) AND (v is B) AND (vvf is R) THEN (pu is N)
```

### Execução

Para executar o programa, abra o terminal e navegue até a pasta raíz do projeto e em seguida, execute o seguinte comando:

```
python -m venv venv
source venv/bin/activate  # Para Linux/MacOS
venv\Scripts\activate  # Para Windows
```

Após isso, instale as dependências usando o seguinte comando: 

```
pip install -r requirements.txt
```

Para executar os experimentos execute para:

Exercício Central de Peças

```
streamlit run centralPecas.py
```

Trabalho de ultrapassagem de um veículo:

```
streamlit run passagemVeiculo.py
```
