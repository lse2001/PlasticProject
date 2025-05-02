import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_pca_visuals(csv_path="HPU Subset Data Filtered.csv"):
    """
    Generates two interactive PCA visualizations:
    1. Scatter plot of observations with coloring by Language
    2. Biplot showing feature loadings (vectors)
    """
    # Load and filter data
    df = pd.read_csv(csv_path)
    df = df[["Gear Type", "Color", "Language"]].dropna()
    tooltip_df = df.copy()

    # One-hot encode
    encoder = OneHotEncoder(sparse_output=False)
    encoded = encoder.fit_transform(df)
    feature_names = encoder.get_feature_names_out(["Gear Type", "Color", "Language"])

    # PCA
    pca = PCA(n_components=2)
    coords = pca.fit_transform(encoded)
    explained_variance = pca.explained_variance_ratio_

    # Add PCA coords to tooltip dataframe
    tooltip_df["PC1"] = coords[:, 0]
    tooltip_df["PC2"] = coords[:, 1]

    # --- Visualization 1: Interactive Scatter Plot ---
    fig1 = px.scatter(
        tooltip_df,
        x="PC1",
        y="PC2",
        color="Language",
        hover_data=["Gear Type", "Color", "Language"],
        title=f"PCA Projection of One-Hot Encoded Gear Type, Color, and Language<br><sup>PC1: {explained_variance[0]:.1%} | PC2: {explained_variance[1]:.1%}</sup>",
        width=900,
        height=700,
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    fig1.update_layout(
        plot_bgcolor='white',
        legend=dict(y=1, x=1.1),
        margin=dict(l=20, r=100, t=80, b=20)
    )

    fig1.add_shape(type="line", x0=0, y0=min(coords[:, 1]), x1=0, y1=max(coords[:, 1]),
                   line=dict(color="gray", width=1, dash="dash"))
    fig1.add_shape(type="line", x0=min(coords[:, 0]), y0=0, x1=max(coords[:, 0]), y1=0,
                   line=dict(color="gray", width=1, dash="dash"))

    fig1.write_html("pca_interactive_exploration.html")

    # --- Visualization 2: Biplot with Loadings ---
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    fig2 = make_subplots(rows=1, cols=1)

    fig2.add_trace(
        go.Scatter(
            x=coords[:, 0], y=coords[:, 1],
            mode='markers',
            marker=dict(color='gray', size=8, opacity=0.5),
            name='Observations',
            hoverinfo='skip'
        )
    )

    color_map = {
        'Gear Type': 'royalblue',
        'Color': 'firebrick',
        'Language': 'darkgreen'
    }

    for i, feature in enumerate(feature_names):
        category = feature.split('_')[0]
        length = np.sqrt(loadings[i, 0] ** 2 + loadings[i, 1] ** 2)
        if length > 0.1:
            scale = 1.2
            x_end = loadings[i, 0] * scale
            y_end = loadings[i, 1] * scale

            fig2.add_trace(
                go.Scatter(
                    x=[0, x_end], y=[0, y_end],
                    mode='lines',
                    line=dict(color=color_map[category], width=2),
                    name=feature,
                    showlegend=False
                )
            )

            fig2.add_annotation(
                x=x_end, y=y_end, text=feature,
                showarrow=False,
                font=dict(size=10, color=color_map[category]),
                bgcolor="white",
                bordercolor=color_map[category],
                borderwidth=1,
                borderpad=3
            )

    for category, color in color_map.items():
        fig2.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode='lines',
                line=dict(color=color, width=3),
                name=category
            )
        )

    fig2.update_layout(
        title=f"PCA Biplot: Feature Influences<br><sup>Arrows show how categories influence the PCA axes</sup>",
        xaxis_title=f"PC1 ({explained_variance[0]:.1%} variance)",
        yaxis_title=f"PC2 ({explained_variance[1]:.1%} variance)",
        height=700,
        width=900,
        plot_bgcolor='white',
        legend=dict(y=1, x=1.1),
        margin=dict(l=20, r=100, t=80, b=20)
    )

    fig2.add_shape(type="line", x0=0, y0=min(coords[:, 1]) * 1.2, x1=0, y1=max(coords[:, 1]) * 1.2,
                   line=dict(color="gray", width=1, dash="dash"))
    fig2.add_shape(type="line", x0=min(coords[:, 0]) * 1.2, y0=0, x1=max(coords[:, 0]) * 1.2, y1=0,
                   line=dict(color="gray", width=1, dash="dash"))

    fig2.write_html("pca_biplot.html")

    print("\n✅ PCA visualizations complete!")
    print("🔹 pca_interactive_exploration.html — colored scatter plot")
    print("🔹 pca_biplot.html — feature vector biplot")


generate_pca_visuals()
