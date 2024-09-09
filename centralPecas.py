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
            tickvals=np.arange(0, 1.05, 0.05),  # Define os ticks em 0.05
            ticktext=[f'{i:.2f}' for i in np.arange(0, 1.05, 0.05)]  # Mostra os ticks como texto formatado
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

st.set_page_config(page_title='Sistema de Controle de Peças', layout='wide')

# Definição das variáveis linguísticas
m = ctrl.Antecedent(np.arange(0, 1.2, 0.001), 'tempo_medio_espera')
m['mp'] = fuzz.trapmf(m.universe, [0, 0, 0.1, 0.3])
m['p'] = fuzz.trimf(m.universe, [0.1, 0.3, 0.5])
m['m'] = fuzz.trapmf(m.universe, [0.4, 0.6, 0.7, 0.7])

p = ctrl.Antecedent(np.arange(0, 1.2, 0.001), 'fator_utilizacao')
p['b'] = fuzz.trapmf(p.universe, [0, 0, 0.2, 0.4])
p['m'] = fuzz.trimf(p.universe, [0.3, 0.5, 0.7])
p['a'] = fuzz.trapmf(p.universe, [0.6, 0.8, 1, 1])

s = ctrl.Antecedent(np.arange(0, 1.2, 0.001), 'num_funcionarios')
s['p'] = fuzz.trapmf(s.universe, [0, 0, 0.4, 0.6])
s['m'] = fuzz.trimf(s.universe, [0.4, 0.6, 0.8])
s['g'] = fuzz.trapmf(s.universe, [0.6, 0.8, 1, 1])

n = ctrl.Consequent(np.arange(0, 1.2, 0.001), 'num_pecas_extras')
n['mp'] = fuzz.trapmf(n.universe, [0, 0, 0.1, 0.3])
n['p'] = fuzz.trimf(n.universe, [0, 0.2, 0.4])
n['pp'] = fuzz.trimf(n.universe, [0.25, 0.35, 0.45])
n['m'] = fuzz.trimf(n.universe, [0.3, 0.5, 0.7])
n['pg'] = fuzz.trimf(n.universe, [0.55, 0.65, 0.75])
n['g'] = fuzz.trimf(n.universe, [0.6, 0.8, 1])
n['mg'] = fuzz.trapmf(n.universe, [0.7, 0.9, 1, 1])

rule1 = ctrl.Rule(m['mp'] & s['p'], n['mg'])
rule2 = ctrl.Rule(m['p'] & s['g'], n['p'])
rule3 = ctrl.Rule(p['b'], n['p'])
rule4 = ctrl.Rule(p['a'], n['g'])

system = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
sim = ctrl.ControlSystemSimulation(system)

st.title('Sistema de Controle de Peças')

# Campos de entrada para os dados
tempo_medio_espera = st.number_input('Tempo de Espera (0.0 a 1.0)', 0.0, 1.0, 0.3, step=0.01)
fator_utilizacao = st.number_input('Fator de Utilização (0.0 a 1.0)', 0.0, 1.0, 0.3, step=0.01)
num_funcionarios = st.number_input('Número de Funcionários (0.0 a 1.0)', 0.0, 1.0, 0.3, step=0.01)

# Botão para calcular
if st.button("Calcular"):
    sim.input['tempo_medio_espera'] = tempo_medio_espera
    sim.input['fator_utilizacao'] = fator_utilizacao
    sim.input['num_funcionarios'] = num_funcionarios

    if safe_compute(sim):
        st.write(f"Número de peças extras: {sim.output['num_pecas_extras']:.2f}")

        # Exibindo gráficos das funções de pertinência e marcando os pontos
        st.subheader('Funções de Pertinência')
        st.plotly_chart(plot_fuzzy_var(m, 'Tempo de Espera', input_value=tempo_medio_espera, medians=[0.1, 0.3, 0.6]))
        st.plotly_chart(plot_fuzzy_var(p, 'Fator de Utilização', input_value=fator_utilizacao, medians=[0.2, 0.5, 0.8]))
        st.plotly_chart(plot_fuzzy_var(s, 'Número de Funcionários', input_value=num_funcionarios, medians=[0.4, 0.6, 0.8]))
        st.plotly_chart(plot_fuzzy_var(n, 'Número de Peças Extras', output_value=sim.output['num_pecas_extras'], medians=[0.1, 0.2, 0.35, 0.5, 0.65, 0.8, 0.9]))
    else:
        st.error("Erro ao calcular o número de peças extras.")
