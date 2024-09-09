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
| Boa | B | [30,...,60]|
| Média| M | [60,...,90] |
| Ruim | R | [90,...,120] |

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
