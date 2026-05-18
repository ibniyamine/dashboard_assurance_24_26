import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Audit Assurance · Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Theme Definitions ────────────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":           "#0d1117",
        "surface":      "#161b22",
        "surface2":     "#21262d",
        "border":       "#30363d",
        "accent":       "#58a6ff",
        "accent2":      "#3fb950",
        "danger":       "#f85149",
        "warning":      "#d29922",
        "text":         "#e6edf3",
        "text2":        "#c9d1d9",
        "muted":        "#8b949e",
        "chart_blue_scale": [[0, "#1a2744"], [0.5, "#1d4ed8"], [1, "#58a6ff"]],
        "chart_red_scale":  [[0, "#450a0a"], [0.5, "#991b1b"], [1, "#f85149"]],
        "multi": ["#58a6ff","#3fb950","#f85149","#d29922","#a371f7","#39d353","#ff7b72","#ffa657"],
        "plot_bg":      "#161b22",
        "paper_bg":     "#161b22",
        "grid":         "#30363d",
        "hero_grad":    "linear-gradient(135deg, #0d1117 0%, #161b22 40%, #1a2744 100%)",
        "hero_radial":  "radial-gradient(ellipse 60% 80% at 100% 0%, rgba(88,166,255,.14) 0%, transparent 60%), radial-gradient(ellipse 40% 60% at 0% 100%, rgba(63,185,80,.09) 0%, transparent 60%)",
        "badge_bg":     "rgba(88,166,255,.1)",
        "badge_border": "rgba(88,166,255,.25)",
        "badge_color":  "#58a6ff",
        "kpi_bg":       "#161b22",
        "kpi_border":   "#30363d",
        "filter_bg":    "#161b22",
        "filter_border":"#30363d",
        "sidebar_bg":   "#161b22",
        "toggle_icon":  "☀️",
        "toggle_label": "Mode Clair",
    },
    "light": {
        "bg":           "#f0f4f8",
        "surface":      "#ffffff",
        "surface2":     "#f8fafc",
        "border":       "#e2e8f0",
        "accent":       "#1d4ed8",
        "accent2":      "#16a34a",
        "danger":       "#dc2626",
        "warning":      "#d97706",
        "text":         "#0f172a",
        "text2":        "#1e293b",
        "muted":        "#64748b",
        "chart_blue_scale": [[0, "#bfdbfe"], [0.5, "#3b82f6"], [1, "#1d4ed8"]],
        "chart_red_scale":  [[0, "#fecaca"], [0.5, "#ef4444"], [1, "#b91c1c"]],
        "multi": ["#1d4ed8","#16a34a","#dc2626","#d97706","#7c3aed","#0891b2","#be185d","#b45309"],
        "plot_bg":      "#ffffff",
        "paper_bg":     "#ffffff",
        "grid":         "#e2e8f0",
        "hero_grad":    "linear-gradient(135deg, #dbeafe 0%, #eff6ff 50%, #f0fdf4 100%)",
        "hero_radial":  "radial-gradient(ellipse 60% 80% at 100% 0%, rgba(29,78,216,.08) 0%, transparent 60%), radial-gradient(ellipse 40% 60% at 0% 100%, rgba(22,163,74,.06) 0%, transparent 60%)",
        "badge_bg":     "rgba(29,78,216,.08)",
        "badge_border": "rgba(29,78,216,.2)",
        "badge_color":  "#1d4ed8",
        "kpi_bg":       "#ffffff",
        "kpi_border":   "#e2e8f0",
        "filter_bg":    "#ffffff",
        "filter_border":"#e2e8f0",
        "sidebar_bg":   "#ffffff",
        "toggle_icon":  "🌙",
        "toggle_label": "Mode Sombre",
    }
}

# ─── Session State Init ───────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

T = THEMES[st.session_state.theme]

# ─── CSS ─────────────────────────────────────────────────────────────────────
def inject_css(T):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Sora:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset ── */
    .stApp {{ background: {T['bg']} !important; }}
    section[data-testid="stSidebar"] {{
        background: {T['surface']} !important;
        border-right: 1px solid {T['border']};
    }}
    .stApp > header {{ background: transparent !important; }}
    * {{ transition: background 0.25s, color 0.2s, border-color 0.2s; }}

    /* ── Hero ── */
    .hero {{
        background: {T['hero_grad']};
        border: 1px solid {T['border']};
        border-radius: 16px;
        padding: 2.5rem 2rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    .hero::before {{
        content: '';
        position: absolute; inset: 0;
        background: {T['hero_radial']};
        pointer-events: none;
    }}
    .hero-badge {{
        display: inline-flex; align-items: center; gap: 6px;
        background: {T['badge_bg']};
        border: 1px solid {T['badge_border']};
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.72rem;
        color: {T['badge_color']};
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 0.75rem;
        text-transform: uppercase; letter-spacing: .06em;
    }}
    .hero-title {{
        font-family: 'Sora', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: {T['text']};
        margin: 0;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }}
    .hero-title span {{ color: {T['accent']}; }}
    .hero-sub {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: {T['muted']};
        margin-top: 0.5rem;
    }}

    /* ── KPI Grid ── */
    .kpi-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 1.5rem;
    }}
    .kpi {{
        background: {T['kpi_bg']};
        border: 1px solid {T['kpi_border']};
        border-radius: 12px;
        padding: 1.2rem 1.25rem 1rem;
        position: relative;
        overflow: hidden;
    }}
    .kpi::after {{
        content: '';
        position: absolute; top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }}
    .kpi.blue::after  {{ background: {T['accent']}; }}
    .kpi.green::after {{ background: {T['accent2']}; }}
    .kpi.red::after   {{ background: {T['danger']}; }}
    .kpi.gold::after  {{ background: {T['warning']}; }}
    .kpi-label {{
        font-family: 'DM Sans', sans-serif;
        font-size: 0.69rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: .08em;
        color: {T['muted']}; margin-bottom: 0.4rem;
    }}
    .kpi-value {{
        font-family: 'Sora', sans-serif;
        font-size: 1.8rem; font-weight: 700;
        color: {T['text']}; line-height: 1;
        margin-bottom: 0.3rem;
    }}
    .kpi-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.69rem; color: {T['muted']};
    }}
    .kpi-sub.pos {{ color: {T['accent2']}; }}
    .kpi-sub.neg {{ color: {T['danger']}; }}

    /* ── Section Headers ── */
    .section-header {{
        display: flex; align-items: center; gap: 10px;
        font-family: 'Sora', sans-serif;
        font-size: 0.95rem; font-weight: 700;
        color: {T['text']};
        margin: 1.5rem 0 0.75rem;
        padding-bottom: 0.55rem;
        border-bottom: 1px solid {T['border']};
    }}
    .section-header .dot {{
        width: 7px; height: 3px; border-radius: 50%;
        background: {T['accent']};
        box-shadow: 0 0 8px {T['accent']}66;
        flex-shrink: 0;
    }}

    /* ── Filter Bar ── */
    .filter-bar {{
        background: {T['filter_bg']};
        border: 1px solid {T['filter_border']};
        border-radius: 10px;
        padding: .875rem 1rem;
        margin-bottom: 1rem;
    }}

    /* ── Sidebar ── */
    .sidebar-title {{
        font-family: 'Sora', sans-serif;
        font-size: 0.85rem; font-weight: 700;
        color: {T['text']};
        text-transform: uppercase; letter-spacing: .06em;
        margin-bottom: 1rem;
        padding-bottom: .5rem;
        border-bottom: 1px solid {T['border']};
    }}
    .theme-toggle {{
        background: {T['filter_bg']};
        border: 1px solid {T['filter_border']};
        border-radius: 8px;
        padding: .6rem .8rem;
        margin-bottom: 1.25rem;
        text-align: center;
        font-family: 'DM Sans', sans-serif;
        font-size: .8rem;
        color: {T['muted']};
    }}

    /* ── Streamlit widget labels ── */
    .stSelectbox label, .stMultiSelect label, .stDateInput label {{
        color: {T['muted']} !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: .8rem !important;
    }}
    label[data-testid="stWidgetLabel"] p {{
        color: {T['muted']} !important;
        font-family: 'DM Sans', sans-serif !important;
    }}

    /* ── Dataframe ── */
    .stDataFrame {{ border-radius: 8px; overflow: hidden; }}

    /* ── Footer ── */
    .dash-footer {{
        text-align: center;
        color: {T['muted']};
        font-family: 'JetBrains Mono', monospace;
        font-size: .73rem;
        padding: .75rem 0 .25rem;
        border-top: 1px solid {T['border']};
        margin-top: 1.5rem;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─── Plotly base layout ───────────────────────────────────────────────────────
def base_layout(T, title="", height=420):
    return dict(
        title=dict(
            text=title,
            font=dict(family="'Sora', sans-serif", size=14, color=T["text"]),
            x=0.0, xanchor="left", pad=dict(l=4, b=10)
        ),
        height=height,
        plot_bgcolor=T["plot_bg"],
        paper_bgcolor=T["paper_bg"],
        font=dict(family="'DM Sans', sans-serif", size=12, color=T["muted"]),
        margin=dict(l=16, r=16, t=52, b=16),
        xaxis=dict(
            showgrid=True, gridcolor=T["grid"], gridwidth=1,
            zeroline=False, linecolor=T["border"],
            tickfont=dict(color=T["muted"], size=11),
            title=dict(font=dict(color=T["muted"], size=12)),
        ),
        yaxis=dict(
            showgrid=True, gridcolor=T["grid"], gridwidth=1,
            zeroline=False, linecolor=T["border"],
            tickfont=dict(color=T["muted"], size=11),
            title=dict(font=dict(color=T["muted"], size=13)),
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)" if st.session_state.theme == "dark" else "rgba(255,255,255,0)",
            bordercolor=T["border"], borderwidth=1,
            font=dict(color=T["muted"], size=13),
        ),
        hoverlabel=dict(
            bgcolor=T["surface2"], bordercolor=T["border"],
            font=dict(color=T["text"], size=13, family="'DM Sans', sans-serif"),
        ),
        coloraxis_showscale=False,
    )


# ─── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_parquet("aas_30_avril_2026_V4.parquet")
        def safe_dates(s):
            try:
                return pd.to_datetime(s, errors='coerce')
            except:
                return pd.Series([pd.NaT]*len(s))
        df['EFFECT_DATE'] = safe_dates(df['EFFECT_DATE'])
        n_before = len(df)
        df = df.dropna(subset=['EFFECT_DATE'])
        # if len(df) < n_before:
        #     st.warning(f"{n_before - len(df)} enregistrements avec dates invalides filtrés.")
        df['MARQUE']         = df['MARQUE'].fillna('Non spécifié')
        df['MODEL']         = df['MODEL'].fillna('Non spécifié')
        df['IMMATRICULATION']= df['IMMATRICULATION'].fillna('Non spécifié')
        return df
    except Exception as e:
        st.error(f"Erreur chargement: {e}")
        return pd.DataFrame()


# ─── Charts ──────────────────────────────────────────────────────────────────

def chart_top_companies(df, T):
    vol = df.groupby('COMPANY')['IMMATRICULATION'].nunique().reset_index(name='n')
    vol = vol.sort_values('n').tail(10)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=vol['n'], y=vol['COMPANY'], orientation='h',
        marker=dict(color=vol['n'], colorscale=T['chart_blue_scale'],
                    line=dict(color="rgba(0,0,0,0)", width=0)),
        hovertemplate="<b>%{y}</b><br>Véhicules: <b>%{x:,}</b><extra></extra>",
        text=vol['n'].apply(lambda x: f"{x:,}"),
        textposition='outside',
        textfont=dict(color=T['muted'], size=10),
    ))
    layout = base_layout(T, "Top 10 · Véhicules par COMPANY")
    layout['xaxis']['title'] = dict(text="Véhicules uniques", font=dict(color=T['muted'], size=12))
    layout['yaxis'].update(showgrid=False, tickfont=dict(color=T['text'], size=11))
    layout['bargap'] = 0.35
    fig.update_layout(**layout)
    return fig


def chart_top_ANOMALIEs(df, T):
    anom = df[df['ANOMALIE'] == 'oui']
    vol  = anom.groupby('COMPANY')['IMMATRICULATION'].nunique().reset_index(name='n')
    vol  = vol[vol['n'] > 0].sort_values('n').tail(10)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=vol['n'], y=vol['COMPANY'], orientation='h',
        marker=dict(color=vol['n'], colorscale=T['chart_red_scale'],
                    line=dict(color="rgba(0,0,0,0)", width=0)),
        hovertemplate="<b>%{y}</b><br>ANOMALIEs: <b>%{x:,}</b><extra></extra>",
        text=vol['n'].apply(lambda x: f"{x:,}"),
        textposition='outside',
        textfont=dict(color=T['muted'], size=10),
    ))
    layout = base_layout(T, "Top 10 · Véhicules en ANOMALIE par COMPANY")
    layout['xaxis']['title'] = dict(text="Véhicules avec ANOMALIEs", font=dict(color=T['muted'], size=12))
    layout['yaxis'].update(showgrid=False, tickfont=dict(color=T['text'], size=11))
    layout['bargap'] = 0.35
    fig.update_layout(**layout)
    return fig


def chart_dual_comparison(df, T):
    vol_total = df.groupby('COMPANY')['IMMATRICULATION'].nunique().reset_index(name='total')
    vol_anom  = (df[df['ANOMALIE']=='oui']
                 .groupby('COMPANY')['IMMATRICULATION']
                 .nunique().reset_index(name='ANOMALIEs'))
    cmp = pd.merge(vol_total, vol_anom, on='COMPANY', how='left').fillna(0)
    cmp = cmp.sort_values('total', ascending=False)

    # Pourcentages
    cmp['pct_total'] = (cmp['total'] / cmp['total'].sum()) * 100
    cmp['pct_anom']  = (cmp['ANOMALIEs'] / cmp['total']) * 100  # ANOMALIEs par rapport au total de la COMPANY

    fig = go.Figure()

    # Barres totales
    fig.add_trace(go.Bar(
        name="Véhicules totaux", x=cmp['COMPANY'], y=cmp['total'],
        marker_color=T['accent'], marker_line_width=0, opacity=0.9,
        hovertemplate="<b>%{x}</b><br>Total: <b>%{y:,}</b><br>Part: %{text}<extra></extra>",
        text=cmp['pct_total'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside',
        textfont=dict(color=T['muted'], size=10),
    ))

    # Barres ANOMALIEs
    fig.add_trace(go.Bar(
        name="Avec ANOMALIEs", x=cmp['COMPANY'], y=cmp['ANOMALIEs'],
        marker_color=T['danger'], marker_line_width=0, opacity=0.9,
        hovertemplate="<b>%{x}</b><br>ANOMALIEs: <b>%{y:,}</b><br>% ANOMALIEs: %{text}<extra></extra>",
        text=cmp['pct_anom'].apply(lambda x: f"{x:.1f}%"),
        textposition='outside',
        textfont=dict(color=T['muted'], size=10),
    ))

    layout = base_layout(T, "Véhicules Totaux vs ANOMALIEs des COMPANYs", height=460)
    layout.update(barmode='group', bargap=0.25, bargroupgap=0.05)
    layout['xaxis'].update(tickangle=-38, title=dict(text="COMPANY", font=dict(color=T['muted'], size=12)))
    layout['yaxis']['title'] = dict(text="Nombre de véhicules", font=dict(color=T['muted'], size=12))
    fig.update_layout(**layout)

    return fig


def table_company_summary(df, T):
    # Totaux
    vol_total = df.groupby('COMPANY')['IMMATRICULATION'].count().reset_index(name='enregistrements')
    vol_unique = df.groupby('COMPANY')['IMMATRICULATION'].nunique().reset_index(name='vehicules_uniques')
    vol_anom = (df[df['ANOMALIE']=='oui']
                .groupby('COMPANY')['IMMATRICULATION']
                .nunique().reset_index(name='vehicules_anom'))

    # Fusion
    cmp = vol_total.merge(vol_unique, on='COMPANY')
    cmp = cmp.merge(vol_anom, on='COMPANY', how='left').fillna(0)

    # Colonnes calculées
    cmp['taux_anom_global'] = (cmp['vehicules_anom'] / cmp['vehicules_uniques'].sum()) * 100
    cmp['taux_anom_COMPANY'] = (cmp['vehicules_anom'] / cmp['vehicules_uniques']) * 100
    cmp['part_marche'] = (cmp['vehicules_uniques'] / cmp['vehicules_uniques'].sum()) * 100

    # Tri
    cmp = cmp.sort_values('vehicules_uniques', ascending=False)

    # Tableau Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[
                "<b>COMPANY</b>", 
                "<b>Enregistrements</b>", 
                "<b>Véhicules uniques</b>", 
                "<b>Véhicules anomaliés</b>", 
                "<b>% ANOMALIE global</b>", 
                "<b>% ANOMALIE COMPANY</b>", 
                "<b>Part marché</b>"
            ],
            fill_color=T['accent'],
            font=dict(color='white', size=13, family="'DM Sans', sans-serif"),
            align='center',
            height=40
        ),
        cells=dict(
            values=[
                cmp['COMPANY'],
                cmp['enregistrements'],
                cmp['vehicules_uniques'],
                cmp['vehicules_anom'],
                cmp['taux_anom_global'].apply(lambda x: f"{x:.1f}%"),
                cmp['taux_anom_COMPANY'].apply(lambda x: f"{x:.1f}%"),
                cmp['part_marche'].apply(lambda x: f"{x:.1f}%")
            ],
            fill_color=[[T['chart_blue_scale'][0][1]] * len(cmp)],
            font=dict(color=T['muted'], size=12, family="'DM Sans', sans-serif"),
            align='center',
            line_color=T['muted'],
            line_width=1,
            height=34
        )
    )])

    # Hauteur dynamique : 40px pour l’en-tête + 34px par ligne + marge
    dynamic_height = 40 + (len(cmp) * 34) + 40

    fig.update_layout(
        margin=dict(t=0, b=0),
        height=dynamic_height
    )

    return fig



def chart_yearly_bar(df, T):
    df2 = df.copy()
    df2['year'] = df2['EFFECT_DATE'].dt.year
    df2['month'] = df2['EFFECT_DATE'].dt.month

    # Total par année
    yr = df2.groupby('year').size().reset_index(name='n').sort_values('year')

    # Moyenne mensuelle par année
    monthly_avg = (
        df2.groupby(['year', 'month']).size()
        .groupby('year').apply(lambda x: x.sum() / (4 if x.name == 2026 else len(x)))
        .reset_index(name='avg_per_month')
        .sort_values('year')
    )

    # ➕ Variation par rapport à l'année précédente
    monthly_avg['evolution_vs_prev'] = monthly_avg['avg_per_month'].pct_change() * 100

    # Couleurs
    colors_total = [T['accent'] if i == len(yr)-1 else T['chart_blue_scale'][1][1] for i in range(len(yr))]
    colors_avg = [T['chart_blue_scale'][2][1] for _ in range(len(monthly_avg))]

    fig = go.Figure()

    # Barres totales
    fig.add_trace(go.Bar(
        x=yr['year'].astype(str), y=yr['n'],
        name="Total annuel",
        marker_color=colors_total, marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Total: <b>%{y:,}</b><extra></extra>",
        text=yr['n'].apply(lambda x: f"{x:,}"),
        textposition='outside',
        textfont=dict(color=T['muted'], size=10),
    ))

    # Barres moyennes mensuelles avec évolution
    fig.add_trace(go.Bar(
        x=monthly_avg['year'].astype(str), y=monthly_avg['avg_per_month'],
        name="Moyenne mensuelle",
        marker_color=colors_avg, marker_line_width=0,
        hovertemplate=(
            "<b>%{x}</b><br>Moyenne/mois: <b>%{y:,.1f}</b>"
            "<br>Évolution vs N-1: <b>%{customdata:.1f}%</b><extra></extra>"
        ),
        customdata=monthly_avg['evolution_vs_prev'],
        text=monthly_avg['avg_per_month'].apply(lambda x: f"{x:,.1f}"),
        textposition='outside',
        textfont=dict(color=T['muted'], size=10),
    ))

    layout = base_layout(T, "Enregistrements par Année")
    layout['xaxis']['title'] = dict(text="Année", font=dict(color=T['muted'], size=12))
    layout['yaxis']['title'] = dict(text="Enregistrements", font=dict(color=T['muted'], size=12))
    layout['bargap'] = 0.4
    layout['barmode'] = 'group'
    fig.update_layout(**layout)

    return fig



def chart_yearly_line(df, T):
    df2 = df.copy()
    df2['year'] = df2['EFFECT_DATE'].dt.year
    yr = df2.groupby('year').size().reset_index(name='n').sort_values('year')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yr['year'].astype(str), y=yr['n'],
        mode='lines+markers',
        line=dict(color=T['accent'], width=2.5, shape='spline'),
        marker=dict(color=T['accent'], size=7, line=dict(color=T['surface'], width=2)),
        fill='tozeroy',
        fillcolor=f"rgba({int(T['accent'][1:3],16)},{int(T['accent'][3:5],16)},{int(T['accent'][5:7],16)},.08)",
        hovertemplate="<b>%{x}</b><br>Enregistrements: <b>%{y:,}</b><extra></extra>",
    ))
    layout = base_layout(T, "Évolution Annuelle · Tendance")
    layout['xaxis']['title'] = dict(text="Année", font=dict(color=T['muted'], size=12))
    layout['yaxis']['title'] = dict(text="Enregistrements", font=dict(color=T['muted'], size=12))
    fig.update_layout(**layout)
    return fig


def chart_timeline(df, T):
    tl = df.groupby(df['EFFECT_DATE'].dt.date).size().reset_index(name='n')
    tl.columns = ['date', 'n']
    acc = T['accent2']
    r, g, b = int(acc[1:3],16), int(acc[3:5],16), int(acc[5:7],16)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tl['date'], y=tl['n'],
        mode='lines',
        line=dict(color=T['accent2'], width=1.8, shape='spline'),
        fill='tozeroy',
        fillcolor=f"rgba({r},{g},{b},.08)",
        hovertemplate="<b>%{x}</b><br>Véhicules: <b>%{y:,}</b><extra></extra>",
    ))
    layout = base_layout(T, "Évolution Quotidienne · Volume de Véhicules", height=340)
    layout['xaxis']['title'] = dict(text="Date", font=dict(color=T['muted'], size=12))
    layout['yaxis']['title'] = dict(text="Véhicules", font=dict(color=T['muted'], size=12))
    fig.update_layout(**layout)
    return fig


def chart_anomaly_treemap(df, T):
    anom = df[df['ANOMALIE'] == 'oui']
    by_brand = anom.groupby('MARQUE').size().reset_index(name='n')
    by_brand = by_brand.sort_values('n', ascending=False).head(20)
    fig = px.treemap(
        by_brand, path=['MARQUE'], values='n',
        color='n', color_continuous_scale=T['chart_red_scale'],
    )
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>ANOMALIEs: <b>%{value:,}</b><extra></extra>",
        textfont=dict(family="'DM Sans', sans-serif", size=12, color="white"),
        marker=dict(cornerradius=6),
    )
    layout = base_layout(T, "ANOMALIEs par Marque · Treemap", height=420)
    layout['margin'] = dict(l=8, r=8, t=52, b=8)
    layout['coloraxis_showscale'] = False
    fig.update_layout(**layout)
    return fig


def chart_genre_bar(df, T):
    df2 = df.dropna(subset=['GENDER'])
    ga = df2.groupby(['GENDER','ANOMALIE']).size().reset_index(name='n')
    ga = ga.sort_values(['GENDER','ANOMALIE'])
    fig = go.Figure()
    color_map  = {'non': T['accent2'], 'oui': T['danger']}
    label_map  = {'non': 'Sans ANOMALIE', 'oui': 'Avec ANOMALIE'}
    for status in ['non','oui']:
        sub = ga[ga['ANOMALIE'] == status]
        fig.add_trace(go.Bar(
            name=label_map[status], x=sub['GENDER'], y=sub['n'],
            marker_color=color_map[status], marker_line_width=0, opacity=0.9,
            hovertemplate=f"<b>%{{x}}</b><br>{label_map[status]}: <b>%{{y:,}}</b><extra></extra>",
        ))
    layout = base_layout(T, "ANOMALIEs par Genre de Véhicule", height=420)
    layout.update(barmode='group', bargap=0.3, bargroupgap=0.05)
    layout['xaxis']['title'] = dict(text="Genre", font=dict(color=T['muted'], size=12))
    layout['yaxis']['title'] = dict(text="Véhicules", font=dict(color=T['muted'], size=12))
    fig.update_layout(**layout)
    return fig


def table_gender_summary(df, T):
    # Totaux
    vol_total = df.groupby('GENDER')['IMMATRICULATION'].count().reset_index(name='enregistrements')
    vol_unique = df.groupby('GENDER')['IMMATRICULATION'].nunique().reset_index(name='vehicules_uniques')

    # Fusion
    cmp = vol_total.merge(vol_unique, on='GENDER')

    # Colonnes calculées
    cmp['part_marche'] = (cmp['vehicules_uniques'] / cmp['vehicules_uniques'].sum()) * 100

    # Tri
    cmp = cmp.sort_values('vehicules_uniques', ascending=False)

    # Tableau Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[
                "<b>Genre</b>", 
                "<b>Enregistrements</b>", 
                "<b>Véhicules uniques</b>", 
                "<b>Part marché</b>"
            ],
            fill_color=T['accent'],
            font=dict(color='white', size=13, family="'DM Sans', sans-serif"),
            align='center',
            height=40
        ),
        cells=dict(
            values=[
                cmp['GENDER'],
                cmp['enregistrements'],
                cmp['vehicules_uniques'],
                cmp['part_marche'].apply(lambda x: f"{x:.1f}%")
            ],
            fill_color=[[T['chart_blue_scale'][0][1]] * len(cmp)],
            font=dict(color=T['muted'], size=12, family="'DM Sans', sans-serif"),
            align='center',
            line_color=T['muted'],
            line_width=1,
            height=34
        )
    )])

    # Hauteur dynamique : 40px pour l’en-tête + 34px par ligne + marge
    dynamic_height = 40 + (len(cmp) * 34) + 40

    fig.update_layout(
        margin=dict(t=0, b=0),
        height=dynamic_height
    )

    return fig


### fonction pour le pie chart des statuts finaux
def chart_final_status_pie(df, T):
    # Déduplication par IMMATRICULATION
    # df2 = df.copy()
    df2 = df.drop_duplicates(subset=["IMMATRICULATION"]).copy()

    status_counts = df2["FINAL_STATUS"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    fig = go.Figure(
        go.Pie(
            labels=status_counts["status"],
            values=status_counts["count"],
            marker=dict(
                # colors=colors,
                line=dict(color="white", width=2)),
            hole=0.35,
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Nombre: %{value:,}<br>Part: %{percent}<extra></extra>",
        )
    )

    layout = base_layout(T, "Répartition des Statuts d'attestation")
    layout["legend"] = dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(color=T["muted"], size=12)
    )
    fig.update_layout(**layout)

    return fig


def chart_non_renewed_by_company(df, T):
    # Déduplication par IMMATRICULATION
    df2 = df.drop_duplicates(subset=["IMMATRICULATION"]).copy()
    # df2 = df.drop_duplicates(subset=["IMMATRICULATION"]).copy()

    # Filtrer uniquement les NON RENOUVELÉ
    df_non = df2[df2["FINAL_STATUS"].str.strip().str.upper().isin(["NON RENOUVELL", "NON RENOUVELÉ"])]

    # Comptage par COMPANY
    cmp = df_non.groupby("COMPANY")["IMMATRICULATION"].nunique().reset_index(name="vehicules_non_renouv")
    cmp = cmp.sort_values("vehicules_non_renouv", ascending=False)  # tri décroissant pour barres verticales

    # Couleur premium rouge
    colors = [T["chart_red_scale"][2][1]] * len(cmp)

    fig = go.Figure()

    # Barres verticales
    fig.add_trace(go.Bar(
        x=cmp["COMPANY"],
        y=cmp["vehicules_non_renouv"],
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Non renouvelés: <b>%{y:,}</b><extra></extra>",
        text=cmp["vehicules_non_renouv"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color=T["muted"], size=10),
    ))

    # Mise en page
    layout = base_layout(T, "Véhicules Non Renouvelés par Compagnie")
    layout["xaxis"]["title"] = dict(text="Compagnie", font=dict(color=T["muted"], size=12))
    layout["yaxis"]["title"] = dict(text="Nombre de véhicules non renouvelés", font=dict(color=T["muted"], size=12))
    layout["margin"] = dict(l=40, r=20, t=40, b=80)  # espace pour labels en bas
    fig.update_layout(**layout)

    return fig


def chart_energy_pie(df, T):
    # Déduplication par IMMATRICULATION pour ne compter qu'une fois chaque véhicule
    df2 = df.drop_duplicates(subset=["IMMATRICULATION"]).copy()

    # Comptage par type d'énergie
    energy_counts = df2["ENERGY"].value_counts().reset_index()
    energy_counts.columns = ["energy", "count"]

    # Création du pie chart
    fig = go.Figure(
        go.Pie(
            labels=energy_counts["energy"],
            values=energy_counts["count"],
            marker=dict(
                line=dict(color="white", width=2)
            ),
            hole=0.35,  # donut style
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Nombre: %{value:,}<br>Part: %{percent}<extra></extra>",
        )
    )

    # Mise en page
    layout = base_layout(T, "Répartition des Véhicules par Énergie")
    layout["legend"] = dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5,
        font=dict(color=T["muted"], size=12)
    )
    fig.update_layout(**layout)

    return fig


def chart_status_distribution(df, T):
    # Déduplication par IMMATRICULATION pour éviter doublons
    df2 = df.drop_duplicates(subset=["IMMATRICULATION"]).copy()

    # Comptage par STATUS
    status_counts = df2["STATUS"].value_counts().reset_index()
    status_counts.columns = ["status", "count"]

    # Couleurs (accent pour le plus fréquent, bleu pour les autres)
    colors = [
        T["accent"] if i == 0 else T["chart_blue_scale"][1][1]
        for i in range(len(status_counts))
    ]

    fig = go.Figure()

    # Bar chart vertical
    fig.add_trace(go.Bar(
        x=status_counts["status"],
        y=status_counts["count"],
        marker_color=colors,
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Nombre: <b>%{y:,}</b><extra></extra>",
        text=status_counts["count"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color=T["muted"], size=10),
    ))

    # Mise en page
    layout = base_layout(T, "Distribution des Statuts")
    layout["xaxis"]["title"] = dict(text="Statut", font=dict(color=T["muted"], size=12))
    layout["yaxis"]["title"] = dict(text="Nombre de véhicules", font=dict(color=T["muted"], size=12))
    layout["margin"] = dict(l=40, r=20, t=40, b=40)
    fig.update_layout(**layout)

    return fig


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    # Re-read theme each render
    T = THEMES[st.session_state.theme]
    inject_css(T)

    df = load_data()
    if df.empty:
        st.error("Fichier 'aas_30_avril_2026_V3.parquet' introuvable ou vide.")
        return

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">🛡️ ASSURANCE · 2024 – 2026</div>
        <h1 class="hero-title"><span>Tableau de bord<br>Attestations d'Assurances</span></h1>
        <p class="hero-sub">Analyse intelligente des données · Anomalies · Véhicules · Compagnies</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Filter Bar ────────────────────────────────────────────────────────────
    # st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2,2,2])
    with c1:
        date_debut = st.date_input(
            "Date de Début",
            value=df['EFFECT_DATE'].min().date(),
            min_value=df['EFFECT_DATE'].min().date(),
            max_value=df['EFFECT_DATE'].max().date()
        )
    with c2:
        date_fin = st.date_input(
            "Date de Fin",
            value=df['EFFECT_DATE'].max().date(),
            min_value=df['EFFECT_DATE'].min().date(),
            max_value=df['EFFECT_DATE'].max().date()
        )
    with c3:
        annees = sorted(df['EFFECT_DATE'].dt.year.unique())
        annee  = st.selectbox("Filtrer par année", ["Toutes"] + [str(a) for a in annees])
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        # Theme toggle
        st.markdown(f'<div class="sidebar-title">Filtres Avancés</div>', unsafe_allow_html=True)
        
        col_tog1, col_tog2 = st.columns([1,2])
        with col_tog1:
            st.markdown(f"<div style='padding-top:.4rem;font-size:1.3rem'>{T['toggle_icon']}</div>",
                        unsafe_allow_html=True)
        with col_tog2:
            if st.button(T['toggle_label'], use_container_width=True):
                st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
                st.rerun()

        st.markdown("---")
        matricule = st.text_input("Matricule", help="Filtrer par partie du numéro d'immatriculation")
        if matricule:
            df = df[df['IMMATRICULATION'].str.contains(matricule, case=False, na=False)]
        else:
            matricule = None

        marques = st.multiselect(
            "Marques de véhicules",
            options=df["MARQUE"].value_counts().index.tolist()
        )

        # modeles    = st.multiselect("Modèles de véhicules", sorted(df['MODEL'].unique()))
        COMPANYs = st.multiselect("Compagnies", sorted(df['COMPANY'].unique()))
        
        

        ANOMALIE_selection = st.selectbox(
            "Statut d'Anomalie", ["Toutes","oui","non"],
            help="Filtrer les véhicules selon leur statut d'ANOMALIE"
        )
        ANOMALIE_matricule = st.selectbox(
            "Matricule incorrect", ["Toutes","oui","non"],
            help="Filtrer selon si le matricule est incorrect"
        )

        genres = st.multiselect(
            "Genres de véhicules",
            sorted(df['GENDER'].dropna().unique()),
            help="Filtrer par genre (VP, VUL, CAMION, etc.)"
        )

        FINAL_STATUS_selection = st.selectbox(
            "Statut Renouvellement",
            ["Toutes"] + df["FINAL_STATUS"].dropna().unique().tolist(),
            help="Filtrer les véhicules selon leur statut final"
        )

    # ── Apply Filters ─────────────────────────────────────────────────────────
    d = df[
        (df['EFFECT_DATE'].dt.date >= date_debut) &
        (df['EFFECT_DATE'].dt.date <= date_fin)
    ].copy()

    if annee != "Toutes":
        d = d[d['EFFECT_DATE'].dt.year == int(annee)]
    if marques:    d = d[d['MARQUE'].isin(marques)]
    # if modeles:    d = d[d['MODEL'].isin(modeles)]
    if COMPANYs: d = d[d['COMPANY'].isin(COMPANYs)]

    if ANOMALIE_matricule != "Toutes":
        if 'IM_INCORRECT' in d.columns:
            d = d[d['IM_INCORRECT'] == ANOMALIE_matricule]


    if ANOMALIE_selection != "Toutes": d = d[d['ANOMALIE'] == ANOMALIE_selection]
    if genres:     d = d[d['GENDER'].isin(genres)]
    if FINAL_STATUS_selection != "Toutes":
        d = d[d["FINAL_STATUS"] == FINAL_STATUS_selection]

    if d.empty:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
        return

    # ── KPI ───────────────────────────────────────────────────────────────────
    st.markdown(f'<div class="section-header"><div class="dot"></div>Indicateurs Clés de Performance</div>',
                unsafe_allow_html=True)

    total_veh  = d['IMMATRICULATION'].nunique()
    total_comp = d['COMPANY'].nunique()
    total_rec  = len(d)
    total_anom = d[d['ANOMALIE']=='oui']['IMMATRICULATION'].nunique()
    pct_anom   = total_anom / total_veh * 100 if total_veh else 0

    veh_par_mois = d.groupby(d['EFFECT_DATE'].dt.to_period('M'))['IMMATRICULATION'].nunique()
    moy_veh = veh_par_mois.mean()
    rec_par_mois = d.groupby(d['EFFECT_DATE'].dt.to_period('M')).size()
    moy_rec = rec_par_mois.mean()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi blue">
            <div class="kpi-label">Véhicules Uniques</div>
            <div class="kpi-value">{total_veh:,}</div>
            <div class="kpi-sub pos">⌀ {moy_veh:,.0f} / mois</div>
        </div>
        <div class="kpi green">
            <div class="kpi-label">COMPANYs</div>
            <div class="kpi-value">{total_comp}</div>
            <div class="kpi-sub pos">assureurs actifs</div>
        </div>
        <div class="kpi blue">
            <div class="kpi-label">Enregistrements</div>
            <div class="kpi-value">{total_rec:,}</div>
            <div class="kpi-sub">⌀ {moy_rec:,.0f} / mois</div>
        </div>
        <div class="kpi {'red'}">
            <div class="kpi-label">Véhicules en ANOMALIE</div>
            <div class="kpi-value">{total_anom:,}</div>
            <div class="kpi-sub {'neg'}">↑ {pct_anom:.1f}% du parc</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="stExpander"] {
        background-color: #f0f0f0; /* gris clair */
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── Data Preview ──────────────────────────────────────────────────────────
    with st.expander("📋 Aperçu des données filtrées (100 000 lignes max)"):
        st.dataframe(d.tail(100_000), use_container_width=True, hide_index=True)

    # ── Section: Enregistrements par Année ────────────────────────────────────
    # st.markdown(f'<div class="section-header"><div class="dot"></div>Enregistrements par Année</div>',unsafe_allow_html=True)
    c1, c2 = st.columns([2, 1])
    with c1:
        st.plotly_chart(chart_yearly_bar(d, T), use_container_width=True)
    with c2:
        st.plotly_chart(chart_energy_pie(d, T), use_container_width=True)

    # ── Section: Volume par COMPANY ─────────────────────────────────────────
    st.markdown(f'<div class="section-header"><div class="dot"></div>Volume par COMPANY</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(chart_top_companies(d, T), use_container_width=True)
    with c2:
        st.plotly_chart(chart_top_ANOMALIEs(d, T), use_container_width=True)


    # comparaison des COMPANYs
    st.plotly_chart(chart_dual_comparison(d, T), use_container_width=True)

    st.markdown(f'<div class="section-header"><div class="dot"></div>Résumé des COMPANYs</div>',
                unsafe_allow_html=True)
    st.plotly_chart(table_company_summary(d, T), use_container_width=True)

    # ── Section: Timeline ─────────────────────────────────────────────────────
    st.markdown(f'<div class="section-header"><div class="dot"></div>Évolution Temporelle</div>',
                unsafe_allow_html=True)
    st.plotly_chart(chart_timeline(d, T), use_container_width=True)

    # ── Section: ANOMALIEs ────────────────────────────────────────────────────
    st.markdown(f'<div class="section-header"><div class="dot"></div>Analyse des ANOMALIEs par Marque</div>',
                unsafe_allow_html=True)
    st.plotly_chart(chart_anomaly_treemap(d, T), use_container_width=True)

    # ── Section: Genre ────────────────────────────────────────────────────────
    st.markdown(f'<div class="section-header"><div class="dot"></div>Genre des Véhicules</div>',
                unsafe_allow_html=True)
    st.plotly_chart(table_gender_summary(d, T), use_container_width=True)

    # ── Section: Statut final ─────────────────────────────────────────────────
    st.markdown(f'<div class="section-header"><div class="dot"></div>Répartition des Statuts d\'attestations</div>',
                unsafe_allow_html=True)
    col1, col2 = st.columns([2,2])
    with col1:
        st.plotly_chart(chart_final_status_pie(d, T), use_container_width=True)

    with col2:
        st.plotly_chart(chart_status_distribution(d, T), use_container_width=True)
    
    st.plotly_chart(chart_non_renewed_by_company(d, T), use_container_width=True)

    # ── Footer ────────────────────────────────────────────────────────────────
    yr_min = d['EFFECT_DATE'].dt.year.min()
    yr_max = d['EFFECT_DATE'].dt.year.max()
    st.markdown(
        f'<div class="dash-footer">'
        f'Dashboard Audit Assurance · {yr_min}–{yr_max} · {total_rec:,} enregistrements analysés'
        f'</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()