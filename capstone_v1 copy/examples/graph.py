"""
Interactive 3D t-SNE Visualization

This script creates an interactive 3D visualization of data using t-SNE dimensionality reduction.
The plot is fully interactive with zoom, pan, and rotation capabilities.
"""

import numpy as np
from sklearn import manifold, datasets
import plotly.graph_objects as go
import plotly.express as px

# Note: matplotlib is only needed if you uncomment the static visualization section at the bottom
# import matplotlib.pyplot as plt

# Load sample data (you can replace this with your own data)
# Example: Using sklearn's digits dataset
digits = datasets.load_digits()
features = digits.data
labels = digits.target

# Alternative: You can load your own data here
# import pandas as pd
# data = pd.read_csv('your_data.csv')
# features = data.drop('target_column', axis=1).values
# labels = data['target_column'].values

# t-SNE embedding
print("Computing t-SNE embedding...")
tsne = manifold.TSNE(n_components=3, init='pca', random_state=0, perplexity=30, n_iter=1000)
x_tsne = tsne.fit_transform(features)
print("t-SNE embedding complete!")

# Create interactive 3D plot using Plotly
fig = go.Figure(data=go.Scatter3d(
    x=x_tsne[:, 0],
    y=x_tsne[:, 1],
    z=x_tsne[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=labels,
        colorscale='Viridis',  # You can change this to 'nipy_spectral', 'Rainbow', etc.
        opacity=0.8,
        colorbar=dict(title="Label"),
        line=dict(width=0.5, color='black')
    ),
    text=[f'Label: {label}' for label in labels],  # Hover text
    hovertemplate='<b>X:</b> %{x}<br>' +
                  '<b>Y:</b> %{y}<br>' +
                  '<b>Z:</b> %{z}<br>' +
                  '<b>Label:</b> %{text}<br>' +
                  '<extra></extra>'
))

# Update layout for better interactivity
fig.update_layout(
    title={
        'text': 'Interactive 3D t-SNE Visualization',
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 20}
    },
    scene=dict(
        xaxis_title='t-SNE Component 1',
        yaxis_title='t-SNE Component 2',
        zaxis_title='t-SNE Component 3',
        bgcolor='white',
        xaxis=dict(backgroundcolor='white', gridcolor='lightgray'),
        yaxis=dict(backgroundcolor='white', gridcolor='lightgray'),
        zaxis=dict(backgroundcolor='white', gridcolor='lightgray'),
        camera=dict(
            eye=dict(x=1.5, y=1.5, z=1.5)
        )
    ),
    width=900,
    height=800,
    margin=dict(l=0, r=0, b=0, t=50)
)

# Show the interactive plot
fig.show()

# Optional: Save as HTML file for sharing
# fig.write_html("interactive_3d_tsne.html")
# print("Plot saved as 'interactive_3d_tsne.html'")

# Alternative: Static matplotlib version (commented out)
# Uncomment below if you prefer matplotlib instead of plotly
# Note: You'll need to install matplotlib: pip install matplotlib
"""
import matplotlib.pyplot as plt
fig = plt.figure(1, figsize=(10, 8))
ax = fig.add_subplot(projection='3d')
scatter = ax.scatter(x_tsne[:, 0], x_tsne[:, 1], x_tsne[:, 2], 
                    c=labels, cmap=plt.cm.nipy_spectral, s=20, lw=0)
ax.set_xlabel('t-SNE Component 1')
ax.set_ylabel('t-SNE Component 2')
ax.set_zlabel('t-SNE Component 3')
ax.set_title('3D t-SNE Visualization')
plt.colorbar(scatter, ax=ax, label='Label')
plt.show()
"""
