import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import requests
import io

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Audit Assurance",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS pour le style moderne
def inject_css():
    st.markdown("""
    <style>
    /* Style général */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Carte de titre dégradée moderne */
    .title-gradient-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #fda085 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: none;
        position: relative;
        overflow: hidden;
        width: 100%;
    }
    
    .title-gradient-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        pointer-events: none;
    }
    
    .title-gradient-content {
        position: relative;
        z-index: 1;
        text-align: center;
    }
    
    .title-gradient-text {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        letter-spacing: -0.02em;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .title-gradient-subtitle {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 0.5rem;
        font-weight: 400;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Responsive pour mobile */
    @media (max-width: 768px) {
        .title-gradient-card {
            padding: 2rem 1rem;
        }
        
        .title-gradient-text {
            font-size: 2.5rem;
        }
        
        .title-gradient-subtitle {
            font-size: 1rem;
        }
    }
    
    /* Cartes KPI */
    .kpi-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: transform 0.2s ease-in-out;
        height: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    .kpi-title {
        font-size: 0.875rem;
        color: #6b7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }
    
    .kpi-change {
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .kpi-change.positive {
        color: #10b981;
    }
    
    .kpi-change.negative {
        color: #ef4444;
    }
    
    /* Filtres */
    .filter-section {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    
    .filter-title {
        font-weight: 600;
        color: #475569;
        margin-bottom: 0.75rem;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Graphiques */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
    }
    
    .chart-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
    }
    
    /* Sidebar */
    .sidebar-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Cache le streamlit footer */
    .footer {
        visibility: hidden;
    }
    
    /* Style pour les sélecteurs */
    .stSelectbox > div > div > select {
        background-color: white;
        color: #1f2937;
        border: 1px solid #d1d5db;
        border-radius: 6px;
    }
    
    .stMultiSelect > div > div > div {
        background-color: white;
        border: 1px solid #d1d5db;
        border-radius: 6px;
    }
    
    .stDateInput > div > div > input {
        background-color: white;
        border: 1px solid #d1d5db;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Charger et prétraiter les données depuis le fichier Parquet"""
    try:

        # Maintenant Pandas peut lire le contenu réel du fichier
        df = pd.read_parquet("resultats_avril_2026_V5.parquet")
                
        # Conversion des dates avec gestion des erreurs
        def safe_date_conversion(series):
            """Convertir les dates en gérant les valeurs hors limites"""
            try:
                # Essayer la conversion standard
                return pd.to_datetime(series, errors='coerce')
            except:
                # Si erreur, utiliser une approche plus robuste
                dates = []
                for val in series:
                    try:
                        date = pd.to_datetime(val)
                        # Vérifier si la date est dans une plage raisonnable (1900-2100)
                        if 1900 <= date.year <= 2100:
                            dates.append(date)
                        else:
                            dates.append(pd.NaT)
                    except:
                        dates.append(pd.NaT)
                return pd.Series(dates)
        
        # Conversion sécurisée des dates
        df['date_effet_corrige'] = safe_date_conversion(df['date_effet_corrige'])
        
        # Filtrer les lignes avec des dates invalides
        initial_count = len(df)
        df = df.dropna(subset=['date_effet_corrige'])
        
        if len(df) < initial_count:
            st.warning(f"{initial_count - len(df)} enregistrements avec dates invalides ont été filtrés")
        
        # Nettoyage des données
        df['veh_marque'] = df['veh_marque'].fillna('Non spécifié')
        df['veh_modele'] = df['veh_modele'].fillna('Non spécifié')
        df['veh_immatriculation'] = df['veh_immatriculation'].fillna('Non spécifié')
        
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame()

def create_kpi_cards(df):
    """Créer les cartes KPI stylisées"""
    # Calcul des KPIs
    total_vehicules = df['veh_immatriculation'].nunique()
    total_compagnies = df['Compagnie'].nunique()
    total_records = len(df)
    total_anomalies = df[df['anomalie'] == 'oui'].shape[0]
    
    # Pourcentage d'anomalies
    pct_anomalies = (total_anomalies / total_records * 100) if total_records > 0 else 0
    
    kpis = [
        {
            "title": "Véhicules Uniques",
            "value": f"{total_vehicules:,}",
            "change": f"{total_vehicules}",
            "change_type": "positive"
        },
        {
            "title": "Compagnies",
            "value": f"{total_compagnies}",
            "change": f"{total_compagnies} assureurs",
            "change_type": "positive"
        },
        {
            "title": "Total Enregistrements",
            "value": f"{total_records:,}",
            "change": f"Période sélectionnée",
            "change_type": "positive"
        },
        {
            "title": "Véhicules en Anomalie",
            "value": f"{total_anomalies:,}",
            "change": f"{pct_anomalies:.1f}% du total",
            "change_type": "negative" if pct_anomalies > 20 else "positive"
        }
    ]
    
    return kpis

def create_comparison_charts(df):
    """Créer les graphiques de comparaison"""
    # Volume total de véhicules uniques par compagnie
    volume_total = df.groupby('Compagnie')['veh_immatriculation'].nunique().reset_index(name='total_vehicules')
    volume_total = volume_total.sort_values('total_vehicules', ascending=False)
    
    # Volume des véhicules uniques avec anomalies par compagnie
    anomalies_df = df[df['anomalie'] == 'oui']
    volume_anomalies = anomalies_df.groupby('Compagnie')['veh_immatriculation'].nunique().reset_index(name='vehicules_anomalies')
    
    # Fusion pour avoir toutes les compagnies
    volume_compare = pd.merge(volume_total, volume_anomalies, on='Compagnie', how='left')
    volume_compare['vehicules_anomalies'] = volume_compare['vehicules_anomalies'].fillna(0)
    
    # Graphique 1: Volume total de véhicules par compagnie
    fig1 = px.bar(
        volume_total.head(10),
        x='total_vehicules',
        y='Compagnie',
        orientation='h',
        title='Top 10 - Volume Total de Véhicules par Compagnie',
        color='total_vehicules',
        color_continuous_scale='Blues'
    )
    fig1.update_layout(
        height=400,
        xaxis_title="Nombre de véhicules uniques",
        yaxis_title="Compagnie",
        showlegend=False
    )
    
    # Graphique 2: Volume des véhicules avec anomalies par compagnie
    fig2 = px.bar(
        volume_compare[volume_compare['vehicules_anomalies'] > 0].head(10),
        x='vehicules_anomalies',
        y='Compagnie',
        orientation='h',
        title='Top 10 - Véhicules avec Anomalies par Compagnie',
        color='vehicules_anomalies',
        color_continuous_scale='Reds'
    )
    fig2.update_layout(
        height=400,
        xaxis_title="Nombre de véhicules avec anomalies",
        yaxis_title="Compagnie",
        showlegend=False
    )
    
    return fig1, fig2

def create_comparison_dual_chart(df):
    """Créer un graphique de comparaison avec deux barres par compagnie (largeur complète)"""
    # Volume total de véhicules uniques par compagnie
    volume_total = df.groupby('Compagnie')['veh_immatriculation'].nunique().reset_index(name='total_vehicules')
    
    # Volume des véhicules uniques avec anomalies par compagnie
    anomalies_df = df[df['anomalie'] == 'oui']
    volume_anomalies = anomalies_df.groupby('Compagnie')['veh_immatriculation'].nunique().reset_index(name='vehicules_anomalies')
    
    # Fusion pour avoir toutes les compagnies
    volume_compare = pd.merge(volume_total, volume_anomalies, on='Compagnie', how='left')
    volume_compare['vehicules_anomalies'] = volume_compare['vehicules_anomalies'].fillna(0)
    
    # Trier par volume total décroissant et prendre les top 15
    volume_compare = volume_compare.sort_values('total_vehicules', ascending=False).head(15)
    
    # Créer un dataframe au format long pour Plotly
    df_long = pd.melt(
        volume_compare,
        id_vars=['Compagnie'],
        value_vars=['total_vehicules', 'vehicules_anomalies'],
        var_name='Type',
        value_name='Nombre'
    )
    
    # Renommer les types pour l'affichage
    df_long['Type'] = df_long['Type'].replace({
        'total_vehicules': 'Véhicules Totaux',
        'vehicules_anomalies': 'Véhicules avec Anomalies'
    })
    
    # Créer le graphique à barres groupées
    fig = px.bar(
        df_long,
        x='Compagnie',
        y='Nombre',
        color='Type',
        title='Comparaison Véhicules Totaux vs Véhicules avec Anomalies par Compagnie',
        barmode='group',
        color_discrete_map={
            'Véhicules Totaux': '#3b82f6',
            'Véhicules avec Anomalies': '#ef4444'
        }
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Compagnie",
        yaxis_title="Nombre de véhicules",
        xaxis_tickangle=-45,
        legend_title="Type de véhicules",
        showlegend=True,
        plot_bgcolor='rgba(249, 250, 251, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        margin=dict(l=20, r=20, t=60, b=100),
        font=dict(
            family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
            size=12,
            color="#1f2937"
        )
    )
    
    # Améliorer la visibilité des axes et du texte
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction ici : titlefont devient title=dict(font=...)
        title=dict(
            text="Date",  # Remplacez par le nom de votre axe X si besoin
            font=dict(color="#1f2937", size=13)
        )
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction ici aussi
        title=dict(
            text="Nombre", # Remplacez par le nom de votre axe Y si besoin
            font=dict(color="#1f2937", size=13)
        )
    )

    
    # Améliorer le style des barres et tooltips
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>' +
                     '%{fullData.name}: %{y:,.0f} véhicules<extra></extra>',
        marker=dict(line=dict(width=1, color='rgba(255, 255, 255, 0.8)'))
    )
    
    # Améliorer la légende
    fig.update_layout(
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.1)',
            bordercolor='rgba(209, 213, 219, 0.3)',
            borderwidth=1,
            font=dict(color="#1f2937", size=11)
        )
    )
    
    return fig

def create_category_charts(df):
    """Créer les graphiques de catégorie basés sur veh_genre"""
    # Nettoyer les données de genre
    df_genre = df.dropna(subset=['veh_genre'])
    
    # Graphique 1: Pie chart des genres
    genre_counts = df_genre['veh_genre'].value_counts().reset_index()
    genre_counts.columns = ['Genre', 'Nombre']
    
    # Créer un pie chart avec des couleurs modernes
    fig_pie = px.pie(
        genre_counts,
        values='Nombre',
        names='Genre',
        title='Répartition des Véhicules par Genre',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.3  # Donut chart style
    )
    
    fig_pie.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01,
            font=dict(size=11, color="#1f2937")
        ),
        plot_bgcolor='rgba(249, 250, 251, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        font=dict(
            family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
            size=12,
            color="#1f2937"
        )
    )
    
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>' +
                     'Nombre: %{value:,.0f}<br>' +
                     'Pourcentage: %{percent}<extra></extra>'
    )
    
    # Graphique 2: Bar chart des genres avec anomalies
    # Compter les véhicules par genre et par statut d'anomalie
    genre_anomalie = df_genre.groupby(['veh_genre', 'anomalie']).size().reset_index(name='count')
    
    # Créer un bar chart groupé
    fig_bar = px.bar(
        genre_anomalie,
        x='veh_genre',
        y='count',
        color='anomalie',
        title='Répartition des Anomalies par Genre de Véhicule',
        barmode='group',
        color_discrete_map={
            'non': '#10b981',  # Vert pour les véhicules sains
            'oui': '#ef4444'   # Rouge pour les anomalies
        }
    )
    
    fig_bar.update_layout(
        height=400,
        xaxis_title="Genre de Véhicule",
        yaxis_title="Nombre de Véhicules",
        showlegend=True,
        plot_bgcolor='rgba(249, 250, 251, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        margin=dict(l=20, r=20, t=60, b=80),
        font=dict(
            family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
            size=12,
            color="#1f2937"
        )
    )
    
        # Améliorer les axes
    fig_bar.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction : titlefont devient title=dict(font=...)
        title=dict(
            font=dict(color="#1f2937", size=13)
        )
    )
    
    fig_bar.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction : titlefont devient title=dict(font=...)
        title=dict(
            font=dict(color="#1f2937", size=13)
        )
    )

    fig_bar.update_traces(
        hovertemplate='<b>Genre: %{x}</b><br>' +
                     'Statut: %{fullData.name}<br>' +
                     'Nombre: %{y:,.0f}<extra></extra>',
        marker=dict(line=dict(width=1, color='rgba(255, 255, 255, 0.8)'))
    )
    
    # Améliorer la légende
    fig_bar.update_layout(
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.1)',
            bordercolor='rgba(209, 213, 219, 0.3)',
            borderwidth=1,
            font=dict(color="#1f2937", size=11),
            title="Statut Anomalie"
        )
    )
    
    return fig_pie, fig_bar

def create_yearly_records_charts(df):
    """Créer les graphiques du nombre d'enregistrements par année"""
    # Extraire l'année et compter les enregistrements
    df_year = df.copy()
    df_year['year'] = df_year['date_effet_corrige'].dt.year
    
    # Graphique 1: Bar chart des enregistrements par année
    year_counts = df_year.groupby('year').size().reset_index(name='count')
    year_counts = year_counts.sort_values('year')
    
    fig_bar = px.bar(
        year_counts,
        x='year',
        y='count',
        title='Nombre d\'Enregistrements par Année',
        color_discrete_sequence=['#1e40af']  # Bleu foncé très visible
    )
    
    fig_bar.update_layout(
        height=400,
        xaxis_title="Année",
        yaxis_title="Nombre d'enregistrements",
        showlegend=False,
        plot_bgcolor='rgba(249, 250, 251, 0.1)',
        paper_bgcolor='rgba(249, 250, 251, 0.1)',
        margin=dict(l=20, r=20, t=60, b=80),
        font=dict(
            family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
            size=12,
            color="#1f2937"
        )
    )
    
    # Améliorer les axes
       # Améliorer les axes pour le graphique en barres
    fig_bar.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction de titlefont
        title=dict(
            font=dict(color="#1f2937", size=13)
        )
    )
    
    fig_bar.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction de titlefont
        title=dict(
            font=dict(color="#1f2937", size=13)
        )
    )

    
    fig_bar.update_traces(
        hovertemplate='<b>Année: %{x}</b><br>' +
                     'Enregistrements: %{y:,.0f}<extra></extra>',
        marker=dict(line=dict(width=1, color='rgba(59, 130, 246, 0.8)'))
    )
    
    # Graphique 2: Line chart avec tendance
    fig_line = px.line(
        year_counts,
        x='year',
        y='count',
        title='Évolution des Enregistrements par Année',
        markers=True,
        color_discrete_sequence=['#3b82f6']
    )
    
    fig_line.update_layout(
        height=400,
        xaxis_title="Année",
        yaxis_title="Nombre d'enregistrements",
        showlegend=False,
        plot_bgcolor='rgba(249, 250, 251, 0.1)',
        paper_bgcolor='rgba(255, 255, 255, 0.05)',
        margin=dict(l=20, r=20, t=60, b=80),
        font=dict(
            family="Segoe UI, Tahoma, Geneva, Verdana, sans-serif",
            size=12,
            color="#1f2937"
        )
    )
    
       # Améliorer les axes
    fig_line.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction de titlefont
        title=dict(
            font=dict(color="#1f2937", size=13)
        )
    )
    
    fig_line.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(209, 213, 219, 0.5)',
        tickfont=dict(color="#4b5563", size=11),
        # Correction de titlefont
        title=dict(
            font=dict(color="#1f2937", size=13)
        )
    )

    
    fig_line.update_traces(
        hovertemplate='<b>Année: %{x}</b><br>' +
                     'Enregistrements: %{y:,.0f}<extra></extra>',
        line=dict(width=3),
        marker=dict(size=8, line=dict(width=2, color='white'))
    )
    
    return fig_bar, fig_line

def create_timeline_chart(df):
    """Créer le graphique de série temporelle"""
    # Grouper par date
    timeline_df = df.groupby(df['date_effet_corrige'].dt.date).size().reset_index(name='count')
    timeline_df.columns = ['date', 'count']
    
    fig = px.area(
        timeline_df,
        x='date',
        y='count',
        title='Évolution du Nombre de Véhicules dans le Temps',
        color_discrete_sequence=['#3b82f6']
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Nombre de véhicules",
        showlegend=False
    )
    
    return fig

def create_anomaly_analysis(df):
    """Créer le graphique d'analyse des anomalies par marque"""
    anomalies_df = df[df['anomalie'] == 'oui']
    
    # Grouper par marque
    marque_anomalies = anomalies_df.groupby('veh_marque').size().reset_index(name='count')
    marque_anomalies = marque_anomalies.sort_values('count', ascending=False).head(15)
    
    # Créer un treemap
    fig = px.treemap(
        marque_anomalies,
        path=['veh_marque'],
        values='count',
        title='Distribution des Anomalies par Marque de Véhicule',
        color='count',
        color_continuous_scale='Oranges'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    return fig

def main():
    inject_css()
    
    # Charger les données
    df = load_data()
    
    if df.empty:
        st.error("Impossible de charger les données. Vérifiez que le fichier 'resultats_avril_2026.parquet' est présent.")
        return
    
    # Titre principal avec carte dégradée moderne
    st.markdown("""
    <div class="title-gradient-card">
        <div class="title-gradient-content">
            <h1 class="title-gradient-text">🏢 Tableau de bord des compagnies d'assurances </h1>
            <p class="title-gradient-subtitle">Analyse intelligente des données d'assurance de 2024 à 2026</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtres en top bar (dates)
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 2])
    
    # with col1:
    #     st.markdown('<div class="filter-title">Période d\'Analyse</div>', unsafe_allow_html=True)
    
    with col1:
        date_debut = st.date_input(
            "Date de Début",
            value=df['date_effet_corrige'].min().date(),
            min_value=df['date_effet_corrige'].min().date(),
            max_value=df['date_effet_corrige'].max().date()
        )
    
    with col2:
        date_fin = st.date_input(
            "Date de Fin",
            value=df['date_effet_corrige'].max().date(),
            min_value=df['date_effet_corrige'].min().date(),
            max_value=df['date_effet_corrige'].max().date()
        )
    
    with col3:
        # Sélecteur d'année
        # st.markdown('<div class="filter-title">OU</div>', unsafe_allow_html=True)
        annees_disponibles = sorted(df['date_effet_corrige'].dt.year.unique())
        annee_selectionnee = st.selectbox(
            "Filtrer par année",
            options=["Toutes"] + [str(annee) for annee in annees_disponibles],
            index=0,
            help="Alternative : sélectionner une année complète"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar pour les filtres additionnels
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Filtres Avancés</div>', unsafe_allow_html=True)
        
        # Filtres multi-sélection
        marques_disponibles = sorted(df['veh_marque'].unique())
        marques_selectionnees = st.multiselect(
            "Marques de véhicules",
            options=marques_disponibles,
            default=[]
        )
        
        modeles_disponibles = sorted(df['veh_modele'].unique())
        modeles_selectionnes = st.multiselect(
            "Modèles de véhicules",
            options=modeles_disponibles,
            default=[]
        )
        
        # immatriculations_disponibles = sorted(df['veh_immatriculation'].unique())
        # immatriculations_selectionnees = st.multiselect(
        #     "Immatriculations",
        #     options=immatriculations_disponibles[:1000],  # Limiter pour performance
        #     # options=immatriculations_disponibles[:1000],  # Limiter pour performance
        #     default=[]
        # )
        
        # Filtre par compagnie
        compagnies_disponibles = sorted(df['Compagnie'].unique())
        compagnies_selectionnees = st.multiselect(
            "Compagnies",
            options=compagnies_disponibles,
            default=[]
        )
        
        # Filtre par anomalie
        # st.markdown("---")
        # st.markdown('<div class="filter-title">Filtre Anomalie</div>', unsafe_allow_html=True)
        anomalie_selection = st.selectbox(
            "Statut d'anomalie",
            options=["Toutes", "oui", "non"],
            index=0,
            help="Filtrer les véhicules selon leur statut d'anomalie"
        )

        anomalie_matricule = st.selectbox(
            "Matricule incorrect",
            options=["Toutes", "oui", "non"],
            index=0,
            help="Filtrer les matricules selon leur etat si incorrect ou non"
        )
        
        # Filtre par genre de véhicule
        # st.markdown("---")
        # st.markdown('<div class="filter-title">Genre de Véhicule</div>', unsafe_allow_html=True)
        genres_disponibles = sorted(df['veh_genre'].dropna().unique())
        genres_selectionnes = st.multiselect(
            "Genres de véhicules",
            options=genres_disponibles,
            default=[],
            help="Filtrer les véhicules par genre (VP, VUL, CAMION, etc.)"
        )
    
    # Appliquer les filtres
    df_filtre = df.copy()
    
    # Filtrage par dates
    df_filtre = df_filtre[
        (df_filtre['date_effet_corrige'].dt.date >= date_debut) &
        (df_filtre['date_effet_corrige'].dt.date <= date_fin)
    ]
    
    # Filtrage par année (si sélectionnée)
    if annee_selectionnee != "Toutes":
        annee = int(annee_selectionnee)
        df_filtre = df_filtre[df_filtre['date_effet_corrige'].dt.year == annee]
    
    # Filtrage par marques
    if marques_selectionnees:
        df_filtre = df_filtre[df_filtre['veh_marque'].isin(marques_selectionnees)]
    
    # Filtrage par modèles
    if modeles_selectionnes:
        df_filtre = df_filtre[df_filtre['veh_modele'].isin(modeles_selectionnes)]
    
    # # Filtrage par immatriculations
    # if immatriculations_selectionnees:
    #     df_filtre = df_filtre[df_filtre['veh_immatriculation'].isin(immatriculations_selectionnees)]
    
    # Filtrage par compagnies
    if compagnies_selectionnees:
        df_filtre = df_filtre[df_filtre['Compagnie'].isin(compagnies_selectionnees)]
    
    # Filtrage par anomalie
    if anomalie_matricule != "Toutes":
        df_filtre = df_filtre[df_filtre['Pl_Incorrect'] == anomalie_matricule]


    # Filtrage par anomalie
    if anomalie_selection != "Toutes":
        df_filtre = df_filtre[df_filtre['anomalie'] == anomalie_selection]
    
    # Filtrage par genres
    if genres_selectionnes:
        df_filtre = df_filtre[df_filtre['veh_genre'].isin(genres_selectionnes)]
    
    # Message si aucun résultat
    if df_filtre.empty:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
        return
    
    # Afficher les informations de filtrage
    # st.info(f"📊 {len(df_filtre):,} enregistrements trouvés sur {len(df):,} au total")
    
    # Bloc 1: KPIs
    # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="chart-title">📈 Indicateurs Clés de Performance</h2>', unsafe_allow_html=True)
    
    kpis = create_kpi_cards(df_filtre)
    
    cols = st.columns(4)
    for i, kpi in enumerate(kpis):
        with cols[i]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">{kpi['title']}</div>
                <div class="kpi-value">{kpi['value']}</div>
                <div class="kpi-change {kpi['change_type']}">{kpi['change']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Bloc Nouveau : Aperçu des données
    st.markdown("### 📋 Aperçu des données filtrées")
    st.markdown('<hr style="margin: 5px 0px; border: 2px solid #f1f1f1;">', unsafe_allow_html=True)
    # On affiche les 10 premières lignes du dataset filtré
    with st.expander("Voir les données détaillées (10 premières lignes)"):
        st.dataframe(
            df_filtre.tail(2100000),
            use_container_width=True, 
            hide_index=True
        )
    # Un séparateur de 1px d'épaisseur avec très peu d'espace autour
    
    # Bloc 2: Analyse par Année
    st.markdown('<hr style="margin: 5px 0px; border: 2px solid #f1f1f1;">', unsafe_allow_html=True)
    st.markdown('<h2 class="chart-title">📊 Analyse des Enregistrements par Année</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_year_bar, fig_year_line = create_yearly_records_charts(df_filtre)
        st.plotly_chart(fig_year_bar, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig_year_line, use_container_width=True)
    
    # Bloc 3: Comparaison (côte à côte)
    col1, col2 = st.columns(2)
    
    with col1:
        # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig1, fig2 = create_comparison_charts(df_filtre)
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)



    # Bloc 2: Comparaison Complète (Largeur complète)
    st.markdown('<hr style="margin: 5px 0px; border: 2px solid #f1f1f1;">', unsafe_allow_html=True)
    dual_chart = create_comparison_dual_chart(df_filtre)
    st.plotly_chart(dual_chart, use_container_width=True)
    
    
    # Bloc 3: Chronologie
    st.markdown('<hr style="margin: 5px 0px; border: 2px solid #f1f1f1;">', unsafe_allow_html=True)
    timeline_fig = create_timeline_chart(df_filtre)
    st.plotly_chart(timeline_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bloc 4: Analyse Technique
    st.markdown('<hr style="margin: 5px 0px; border: 2px solid #f1f1f1;">', unsafe_allow_html=True)
    anomaly_fig = create_anomaly_analysis(df_filtre)
    st.plotly_chart(anomaly_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bloc 5: Analyse par Genre de Véhicule
    st.markdown('<hr style="margin: 5px 0px; border: 2px solid #f1f1f1;">', unsafe_allow_html=True)
    st.markdown('<h2 class="chart-title">🚗 Analyse par Genre de Véhicule</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_pie, fig_bar = create_category_charts(df_filtre)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #6b7280; font-size: 0.875rem;">'
        'Dashboard Audit Assurance - Données mises à jour en temps réel'
        '</div>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
