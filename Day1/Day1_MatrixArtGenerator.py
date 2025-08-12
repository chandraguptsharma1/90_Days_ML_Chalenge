import numpy as np;
import io,os
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

st.set_page_config(page_title="Day-1 matrix Art (Lite)" , layout="centered")

PALETTES = {
    "Vibrant":  ["#EF476F","#FFD166","#06D6A0","#118AB2","#073B4C"],
    "Cool":     ["#00204A","#005792","#00BBF0","#BFEFFF","#E3F6FF"],
    "Earthy":   ["#264653","#2A9D8F","#E9C46A","#F4A261","#E76F51"],
}

def cmap(colors): return ListedColormap(colors)

def grid_random(n,k): return np.random.randint(0, k, (n, n))
def grid_checker(n,k): return (np.indices((n,n)).sum(axis = 0)%2)* (k - 1)
def grid_diagonal(n,k):
    a = np.random.randint(0,k,(n,n))
    np.fill_diagonal(a,0)
    return a

st.title("Day-1 Matrix Art (Lite)")
colA,colB = st.columns(2)

with colA:
    n = st.slider("Grid size" , 10,80,32,step=2)
    palette_name = st.selectbox("Palette", list(PALETTES.keys()),index=0)
with colB:
    pattern = st.radio("Pattern" , ["Random", "Checkerboard" , "Diagonal"], index=0)
    seed = st.number_input("Seed", value=42, step=1)

np.random.seed(seed)
colors = PALETTES[palette_name]
k = len(colors)

if pattern == "Random": G = grid_random(n, k)
elif pattern == "Checkerboard": G = grid_checker(n, k)
else:   G = grid_diagonal(n, k)

fig , ax = plt.subplots(figsize=(6, 6))
ax.imshow(G, cmap=cmap(colors), interpolation='nearest')
ax.set_xticks([]); ax.set_yticks([])

st.pyplot(fig)

#Download PNG
buf = io.BytesIO()

fig.savefig(buf , format='png', bbox_inches='tight', dpi=200)
buf.seek(0)
st.download_button("⬇️ Download PNG", data=buf, file_name="day1_matrix_art.png", mime="image/png")
