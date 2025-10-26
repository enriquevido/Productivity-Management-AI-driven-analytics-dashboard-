import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import numpy as np
from nav import top_nav
top_nav(active="Benchmark")

# Configuración de la página
st.set_page_config(
    page_title="Global Efficiency Dashboard",
    page_icon="🌍",
    layout="wide",
)

st.markdown("""
<style>
/* Ocultar sidebar completamente */
section[data-testid="stSidebar"] {display: none;}
/* Ajustar el ancho del contenido para ocupar toda la pantalla */
div.block-container {padding-left: 3rem; padding-right: 3rem;}
</style>
""", unsafe_allow_html=True)

# Estilos personalizados
st.markdown(f"<style>{(Path(__file__).resolve().parents[1] / 'assets' / 'theme.css').read_text()}</style>", unsafe_allow_html=True)


# Datos de ejemplo
@st.cache_data
def load_data():
    sites_data = {
        'FRA': {'country': 'France', 'region': 'Europe', 'efficiency': 0.94, 'accuracy': 0.38},
        'JFK': {'country': 'United States', 'region': 'North America', 'efficiency': 0.93, 'accuracy': 0.27},
        'CDG': {'country': 'France', 'region': 'Europe', 'efficiency': 0.82, 'accuracy': 0.14},
        'ORD': {'country': 'United States', 'region': 'North America', 'efficiency': 0.90, 'accuracy': 0.06},
        'LHR': {'country': 'United Kingdom', 'region': 'Europe', 'efficiency': 0.88, 'accuracy': 0.22},
        'NRT': {'country': 'Japan', 'region': 'Asia', 'efficiency': 0.91, 'accuracy': 0.19},
        'SYD': {'country': 'Australia', 'region': 'Oceania', 'efficiency': 0.85, 'accuracy': 0.15},
        'DXB': {'country': 'United Arab Emirates', 'region': 'Middle East', 'efficiency': 0.89, 'accuracy': 0.25},
    }
    
    df_sites = pd.DataFrame(sites_data).T
    df_sites['site'] = df_sites.index
    return df_sites

df_sites = load_data()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="big-title">Benchmark & Global Comparison</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f"<div style='text-align: right; color: #666;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)


# <CHANGE> Crear visualización de eficiencia por región usando gráfico de barras
col_chart, col_table = st.columns([2, 1])

with col_chart:
    st.subheader("Efficiency Score by Region")
    
    # Crear gráfico de barras horizontal
    df_sorted = df_sites.sort_values('efficiency', ascending=True)
    
    fig_bars = go.Figure(data=[
        go.Bar(
            y=df_sorted['site'],
            x=df_sorted['efficiency'],
            orientation='h',
            marker=dict(
                color=df_sorted['efficiency'],
                colorscale='Blues',
                showscale=True,
                colorbar=dict(
                    title="Efficiency<br>Score",
                    thickness=15,
                    len=0.7
                ),
                line=dict(color='white', width=2)
            ),
            text=df_sorted['efficiency'].apply(lambda x: f'{x:.2%}'),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Efficiency: %{x:.2%}<extra></extra>'
        )
    ])
    
    fig_bars.update_layout(
        height=400,
        margin=dict(l=50, r=50, t=30, b=50),
        xaxis_title="Efficiency Score",
        yaxis_title="Site",
        showlegend=False,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_bars, use_container_width=True)

with col_table:
    st.subheader("Site Performance")
    
    df_display = df_sites[['site', 'country', 'accuracy', 'efficiency']].copy()
    df_display['accuracy'] = df_display['accuracy'].apply(lambda x: f"{x:.0%}")
    df_display['efficiency'] = df_display['efficiency'].apply(lambda x: f"{x:.2f}")
    df_display.columns = ['Site', 'Country', 'Accuracy', 'Efficiency']
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=400
    )

st.divider()

# Sección de métricas globales
st.subheader("Global Trendline")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Average Efficiency",
        value=f"{df_sites['efficiency'].mean():.2%}",
        delta=f"+{(df_sites['efficiency'].mean() - 0.85):.1%}"
    )

with col2:
    st.metric(
        label="Best Performing Site",
        value=df_sites.loc[df_sites['efficiency'].idxmax(), 'site'],
        delta=f"{df_sites['efficiency'].max():.2%}"
    )

with col3:
    st.metric(
        label="Global Accuracy",
        value=f"{df_sites['accuracy'].mean():.0%}",
        delta=f"+{(df_sites['accuracy'].mean() - 0.15):.0%}"
    )

st.divider()

# Gráfico de tendencia
st.subheader("Efficiency Trend Analysis")

dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
trend_data = pd.DataFrame({
    'Date': dates,
    'FRA': np.random.normal(0.94, 0.02, 30),
    'JFK': np.random.normal(0.93, 0.02, 30),
    'CDG': np.random.normal(0.82, 0.03, 30),
    'ORD': np.random.normal(0.90, 0.02, 30),
})

fig_trend = px.line(
    trend_data,
    x='Date',
    y=['FRA', 'JFK', 'CDG', 'ORD'],
    title='Efficiency Trend Over Time',
    labels={'value': 'Efficiency Score', 'variable': 'Site'},
    color_discrete_map={
        'FRA': '#001f3f',
        'JFK': '#0051ba',
        'CDG': '#4a90e2',
        'ORD': '#7cb9e8'
    }
)

fig_trend.update_layout(
    hovermode='x unified',
    height=400,
    margin=dict(l=0, r=0, t=50, b=0)
)

st.plotly_chart(fig_trend, use_container_width=True)

# Gráfico de eficiencia por región
st.subheader("Efficiency by Region")

region_efficiency = df_sites.groupby('region')['efficiency'].mean().sort_values(ascending=False)

fig_region = px.bar(
    x=region_efficiency.values,
    y=region_efficiency.index,
    orientation='h',
    title='Average Efficiency by Region',
    labels={'x': 'Average Efficiency', 'y': 'Region'},
    color=region_efficiency.values,
    color_continuous_scale='Blues'
)

fig_region.update_layout(
    height=300,
    margin=dict(l=0, r=0, t=50, b=0),
    showlegend=False
)

st.plotly_chart(fig_region, use_container_width=True)

# Sidebar con filtros
st.sidebar.title("Filters & Settings")

selected_sites = st.sidebar.multiselect(
    "Select Sites to Display",
    options=df_sites['site'].tolist(),
    default=df_sites['site'].tolist()
)

efficiency_range = st.sidebar.slider(
    "Efficiency Range",
    min_value=0.0,
    max_value=1.0,
    value=(0.8, 1.0),
    step=0.05
)

st.sidebar.divider()
st.sidebar.info(
    "📊 This dashboard displays global efficiency metrics across multiple sites. "
    "Use the filters to customize your view and analyze performance trends."
)