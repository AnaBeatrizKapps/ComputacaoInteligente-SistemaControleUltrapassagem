import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import streamlit as st
import plotly.graph_objs as go
import plotly.express as px

# Função para tratamento de erros
def safe_compute(simulation):
    try:
        simulation.compute()
        return True
    except Exception as e:
        st.error(f"Erro ao calcular a saída: {e}")
        return False

# Função para plotar as funções de pertinência com Plotly e marcar os pontos
def plot_fuzzy_var(var, var_name, input_value=None, output_value=None, medians=[]):
    traces = []
    for label in var.terms:
        trace = go.Scatter(
            x=var.universe,
            y=var[label].mf,
            mode='lines',
            name=label
        )
        traces.append(trace)

    layout = go.Layout(
        title=f'Função de Pertinência - {var_name}',
        xaxis=dict(
            title=var_name,
            tickvals=np.arange(0, np.max(var.universe) + 10, 10),  # Define os ticks em 10
            ticktext=[f'{i:.2f}' for i in np.arange(0, np.max(var.universe) + 10, 10)]  # Mostra os ticks como texto formatado
        ),
        yaxis=dict(title='Pertinência'),
    )
    
    fig = go.Figure(data=traces, layout=layout)

    # Adicionando linhas medianas
    for median in medians:
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=median, y0=0,
                x1=median, y1=1,
                line=dict(color="LightGray", dash="dash"),
            )
        )

    # Adicionando labels
    for label, x in zip(var.terms, medians):
        fig.add_annotation(
            x=x,
            y=1.05,
            text=label,
            showarrow=False,
            xanchor="center",
            yanchor="bottom"
        )

    if input_value is not None:
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=input_value, y0=0,
                x1=input_value, y1=1,
                line=dict(color="Red", dash="dashdot"),
            )
        )

    if output_value is not None:
        fig.add_shape(
            go.layout.Shape(
                type="line",
                x0=output_value, y0=0,
                x1=output_value, y1=1,
                line=dict(color="Blue", dash="dashdot"),
            )
        )

    return fig

st.set_page_config(page_title='Sistema de Controle de Ultrapassagem', layout='wide')

# Definição das variáveis linguísticas
da = ctrl.Antecedent(np.arange(0, 121, 1), 'distancia_adequada')
da['boa'] = fuzz.trimf(da.universe, [3, 4.5, 6])
da['media'] = fuzz.trimf(da.universe, [6, 7.5, 9])
da['ruim'] = fuzz.trimf(da.universe, [9, 10.5, 12])

pl = ctrl.Antecedent(np.arange(0, 2, 1), 'pista_livre')
pl['livre'] = fuzz.trimf(pl.universe, [0, 0, 1])
pl['obstruida'] = fuzz.trimf(pl.universe, [0, 1, 1])

vvf = ctrl.Antecedent(np.arange(0, 201, 1), 'velocidade_veiculo_frente')
vvf['rapida'] = fuzz.trimf(vvf.universe, [90, 130, 200])
vvf['adequada'] = fuzz.trimf(vvf.universe, [60, 75, 90])
vvf['lenta'] = fuzz.trimf(vvf.universe, [0, 30, 60])

v = ctrl.Antecedent(np.arange(0, 2, 1), 'visibilidade')
v['ruim'] = fuzz.trimf(v.universe, [0, 0, 1])
v['boa'] = fuzz.trimf(v.universe, [0, 1, 1])

pu = ctrl.Consequent(np.arange(0, 2, 1), 'permissao_ultrapassagem')
pu['negada'] = fuzz.trimf(pu.universe, [0, 0, 1])
pu['permitida'] = fuzz.trimf(pu.universe, [0, 1, 1])

# Regras de inferência
rule1 = ctrl.Rule(da['boa'] & pl['livre'] & v['boa'] & vvf['adequada'], pu['permitida'])
rule2 = ctrl.Rule(da['media'] & pl['livre'] & v['boa'] & vvf['adequada'], pu['permitida'])
rule3 = ctrl.Rule(da['ruim'] | pl['obstruida'] | v['ruim'] | vvf['lenta'], pu['negada'])
rule4 = ctrl.Rule(da['boa'] & pl['livre'] & v['boa'] & vvf['rapida'], pu['negada'])

# Criando o sistema de controle
system = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
sim = ctrl.ControlSystemSimulation(system)

st.title('Sistema de Controle de Ultrapassagem')

# Campos de entrada para os dados
distancia_adequada = st.number_input('Distância Adequada (0 a 120)', 0, 120, 60, step=1)
pista_livre = st.selectbox('Pista Livre', ['Livre', 'Obstruída'])
velocidade_veiculo_frente = st.number_input('Velocidade do Veículo à Frente (0 a 200)', 0, 200, 90, step=1)
visibilidade = st.selectbox('Visibilidade', ['Boa', 'Ruim'])

# Botão para calcular
if st.button("Calcular"):
    sim.input['distancia_adequada'] = distancia_adequada
    sim.input['pista_livre'] = 0 if pista_livre == 'Livre' else 1
    sim.input['velocidade_veiculo_frente'] = velocidade_veiculo_frente
    sim.input['visibilidade'] = 0 if visibilidade == 'Ruim' else 1

    if safe_compute(sim):
        permissao_ultrapassagem = sim.output['permissao_ultrapassagem']
        st.write(f"Valor de saída para permissão de ultrapassagem: {permissao_ultrapassagem}")
        st.write(f"Permissão de ultrapassagem: {'Permitida' if permissao_ultrapassagem > 0.5 else 'Negada'}")

        # Exibindo gráficos das funções de pertinência e marcando os pontos
        st.subheader('Funções de Pertinência')
        st.plotly_chart(plot_fuzzy_var(da, 'Distância Adequada', input_value=distancia_adequada, medians=[30, 60, 90]))
        # st.plotly_chart(plot_fuzzy_var(pl, 'Pista Livre', input_value=None, medians=[]))
        st.plotly_chart(plot_fuzzy_var(vvf, 'Velocidade do Veículo à Frente', input_value=velocidade_veiculo_frente, medians=[60, 90, 200]))
        # st.plotly_chart(plot_fuzzy_var(v, 'Visibilidade', input_value=None, medians=[]))
        # st.plotly_chart(plot_fuzzy_var(pu, 'Permissão de Ultrapassagem', output_value=sim.output.get('permissao_ultrapassagem', 0), medians=[]))
    else:
        st.error("Erro ao calcular a permissão de ultrapassagem.")
