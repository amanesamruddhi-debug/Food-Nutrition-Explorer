# ==============================================================================
# FOOD NUTRITION EXPLORER - Streamlit dashboard
# Course: 1ADPC302 Data Exploration and Visualization (CO1-CO5)
# Run:  pip install -r requirements.txt   then   streamlit run app.py
# ==============================================================================
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
 
import os
_cfg = os.path.join(".streamlit", "config.toml")
if not os.path.exists(_cfg):          # creates the dark theme file once; takes effect on next restart
    try:
        os.makedirs(".streamlit", exist_ok=True)
        with open(_cfg, "w") as _f:
            _f.write('[theme]\nbase = "dark"\nprimaryColor = "#34D399"\nbackgroundColor = "#0F172A"\n'
                     'secondaryBackgroundColor = "#1E293B"\ntextColor = "#F8FAFC"\n')
    except OSError:
        pass
 
st.set_page_config(page_title="Food Nutrition Explorer", page_icon="🥗", layout="wide")
 
st.markdown("""<style>
:root{--bg:#0F172A;--card:#1E293B;--line:#334155;--tx:#F8FAFC;--mut:#CBD5E1;--acc:#34D399}
html,body,.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:var(--bg)!important}
[data-testid="stHeader"]{background:transparent!important}
.block-container{padding-top:1.2rem;max-width:1250px}
[data-testid="stMarkdownContainer"] *,[data-testid="stWidgetLabel"] *,label,h1,h2,h3{color:var(--tx)}
[data-testid="stCaptionContainer"] *{color:var(--mut)!important}
[data-testid="stSidebar"]{background:#0B1220!important;border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--tx)}
.hero{background:linear-gradient(120deg,#0F766E 0%,#1D4ED8 100%);border-radius:16px;padding:20px 26px;margin-bottom:16px;box-shadow:0 6px 24px rgba(0,0,0,.35)}
.hero h1{margin:0;font-size:2rem;color:#fff!important}
.hero p{margin:4px 0 6px;color:#E0F2FE!important;font-size:1.02rem}
.chip{display:inline-block;padding:3px 12px;margin:6px 8px 0 0;border-radius:14px;font-size:.82rem;font-weight:600}
.chip.good{background:#064E3B;color:#6EE7B7!important;border:1px solid #34D399}
.chip.bad{background:#7C2D12;color:#FDBA74!important;border:1px solid #FB923C}
[data-testid="stMetric"]{background:var(--card);border:1px solid var(--line);border-top:3px solid var(--acc);border-radius:12px;padding:12px 14px}
[data-testid="stMetricLabel"] *{color:var(--mut)!important}
[data-testid="stMetricValue"] *{color:var(--acc)!important;font-weight:700}
.stTabs [data-baseweb="tab-list"]{gap:6px;border-bottom:1px solid var(--line)}
.stTabs [data-baseweb="tab"]{background:var(--card);border-radius:8px 8px 0 0;padding:8px 16px}
.stTabs [data-baseweb="tab"] p{color:var(--mut)!important;font-weight:600}
.stTabs [aria-selected="true"]{background:#0F766E}
.stTabs [aria-selected="true"] p{color:#fff!important}
.stTabs [data-baseweb="tab-highlight"]{background:var(--acc)}
[data-testid="stSelectbox"] div[data-baseweb="select"],[data-testid="stMultiSelect"] div[data-baseweb="select"],
div[data-baseweb="select"] > div,div[data-baseweb="select"] > div > div,div[data-baseweb="select"] input{background-color:#1E293B!important;color:#F8FAFC!important;-webkit-text-fill-color:#F8FAFC!important}
div[data-baseweb="select"] > div{border:1px solid #475569!important;border-radius:8px!important}
div[data-baseweb="select"] *{color:#F8FAFC!important;-webkit-text-fill-color:#F8FAFC!important}
div[data-baseweb="select"] svg{fill:#CBD5E1!important}
[data-baseweb="tag"]{background:#0F766E!important}
[data-baseweb="popover"],[data-baseweb="popover"] > div,[data-baseweb="menu"],[data-baseweb="popover"] ul,[data-baseweb="popover"] li,ul[role="listbox"]{background-color:#1E293B!important;color:#F8FAFC!important}
[data-baseweb="popover"] li *,ul[role="listbox"] *{color:#F8FAFC!important}
[data-baseweb="popover"] li:hover,li[aria-selected="true"]{background-color:#0F766E!important}
[data-testid="stSlider"] [role="slider"]{background-color:#34D399!important;box-shadow:none!important}
[data-testid="stSlider"] [data-testid="stThumbValue"]{color:#34D399!important;font-weight:700}
[data-testid="stSlider"] *{color:var(--tx)}
[data-testid="stExpander"]{background:var(--card);border:1px solid var(--line);border-radius:10px}
[data-testid="stExpander"] *{color:var(--tx)}
.stDownloadButton button{background:var(--acc);border:0;font-weight:700}
.stDownloadButton button *{color:#0F172A!important}
[data-testid="stPlotlyChart"]{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:8px;margin-bottom:6px}
.tip{background:#0C2A44;border-left:4px solid #38BDF8;border-radius:8px;padding:11px 15px;margin:8px 0 16px;font-size:.93rem}
.tip,.tip *{color:#E0F2FE!important}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px;margin:8px 0 16px}
table.ft{width:100%;border-collapse:collapse;background:var(--card)}
.ft th{background:#0F766E;color:#fff!important;padding:8px 12px;text-align:right;font-weight:600}
.ft td{color:var(--tx)!important;padding:7px 12px;text-align:right;border-top:1px solid var(--line)}
.ft tbody th{background:#172033;color:#fff!important;text-align:left;border-top:1px solid var(--line)}
.ft tbody tr:hover td{background:#26354D}
</style>""", unsafe_allow_html=True)
 
# ------------------------------------------------------------------ DATA
# Approximate values per 100 g (USDA FoodData Central / IFCT 2017). Cooked where stated.
COLS = ["Food", "Category", "Calories", "Protein", "Carbs", "Fat", "Fibre", "Sugar",
        "Vitamin C", "Calcium", "Iron", "Potassium", "Sodium"]
ROWS = [
 ["Apple","Fruit",52,.3,13.8,.2,2.4,10.4,4.6,6,.12,107,1],
 ["Banana","Fruit",89,1.1,22.8,.3,2.6,12.2,8.7,5,.26,358,1],
 ["Orange","Fruit",47,.9,11.8,.1,2.4,9.4,53.2,40,.1,181,0],
 ["Mango","Fruit",60,.8,15,.4,1.6,13.7,36.4,11,.16,168,1],
 ["Grapes","Fruit",69,.7,18.1,.2,.9,15.5,3.2,10,.36,191,2],
 ["Strawberry","Fruit",32,.7,7.7,.3,2,4.9,58.8,16,.41,153,1],
 ["Avocado","Fruit",160,2,8.5,14.7,6.7,.7,10,12,.55,485,7],
 ["Spinach","Vegetable",23,2.9,3.6,.4,2.2,.4,28.1,99,2.7,558,79],
 ["Broccoli","Vegetable",34,2.8,6.6,.4,2.6,1.7,89.2,47,.73,316,33],
 ["Cauliflower","Vegetable",25,1.9,5,.3,2,1.9,48.2,22,.42,299,30],
 ["Carrot","Vegetable",41,.9,9.6,.2,2.8,4.7,5.9,33,.3,320,69],
 ["Tomato","Vegetable",18,.9,3.9,.2,1.2,2.6,13.7,10,.27,237,5],
 ["Cucumber","Vegetable",15,.7,3.6,.1,.5,1.7,2.8,16,.28,147,2],
 ["Green peas","Vegetable",81,5.4,14.5,.4,5.7,5.7,40,25,1.47,244,5],
 ["Potato (boiled)","Vegetable",87,1.9,20.1,.1,1.8,.9,13,5,.31,328,4],
 ["Sweet potato (baked)","Vegetable",90,2,20.7,.2,3.3,6.5,19.6,38,.69,475,36],
 ["White rice (cooked)","Grain",130,2.7,28.2,.3,.4,.1,0,10,.2,35,1],
 ["Brown rice (cooked)","Grain",123,2.7,25.6,1,1.6,.2,0,3,.56,86,4],
 ["Quinoa (cooked)","Grain",120,4.4,21.3,1.9,2.8,.9,0,17,1.49,172,7],
 ["Whole wheat bread","Grain",247,13,41,3.4,7,6,0,107,2.5,250,400],
 ["Oats (dry)","Grain",389,16.9,66.3,6.9,10.6,0,0,54,4.7,429,2],
 ["Lentils (cooked)","Protein",116,9,20.1,.4,7.9,1.8,1.5,19,3.3,369,2],
 ["Chickpeas (cooked)","Protein",164,8.9,27.4,2.6,7.6,4.8,1.3,49,2.9,291,7],
 ["Kidney beans (cooked)","Protein",127,8.7,22.8,.5,6.4,.3,1.2,28,2.2,403,1],
 ["Tofu","Protein",76,8.1,1.9,4.8,.3,.6,.1,350,5.4,121,7],
 ["Egg (boiled)","Protein",155,12.6,1.1,10.6,0,1.1,0,50,1.2,126,124],
 ["Chicken breast (cooked)","Protein",165,31,0,3.6,0,0,0,15,1,256,74],
 ["Salmon (cooked)","Protein",206,22.1,0,12.4,0,0,0,9,.25,384,61],
 ["Shrimp (cooked)","Protein",99,24,.2,.3,0,0,0,70,.5,259,111],
 ["Milk (whole)","Dairy",61,3.2,4.8,3.3,0,5.1,0,113,.03,132,43],
 ["Yogurt (plain)","Dairy",61,3.5,4.7,3.3,0,4.7,.5,121,.05,155,46],
 ["Paneer","Dairy",265,18.3,1.2,20.8,0,0,0,208,.2,100,18],
 ["Cheddar cheese","Dairy",403,24.9,1.3,33.1,0,.5,0,721,.7,98,621],
 ["Almonds","Nuts & Treats",579,21.2,21.6,49.9,12.5,4.4,0,269,3.7,733,1],
 ["Peanuts","Nuts & Treats",567,25.8,16.1,49.2,8.5,4.7,0,92,4.6,705,18],
 ["Walnuts","Nuts & Treats",654,15.2,13.7,65.2,6.7,2.6,1.3,98,2.9,441,2],
 ["Dark chocolate","Nuts & Treats",598,7.8,45.9,42.6,10.9,24,0,73,11.9,715,20],
]
# nutrient: (unit, daily value for 2000 kcal diet, kind)  kind: good = get enough, limit = don't overdo, energy
NUT = {"Calories":("kcal",2000,"energy"),"Protein":("g",50,"good"),"Carbs":("g",275,"energy"),
       "Fat":("g",78,"limit"),"Fibre":("g",28,"good"),"Sugar":("g",50,"limit"),
       "Vitamin C":("mg",90,"good"),"Calcium":("mg",1300,"good"),"Iron":("mg",18,"good"),
       "Potassium":("mg",4700,"good"),"Sodium":("mg",2300,"limit")}
KCOL = {"good":"#34D399","limit":"#FB923C","energy":"#38BDF8"}
MCOL = {"Protein":"#38BDF8","Carbs":"#FBBF24","Fat":"#FB7185"}
GCOL = {"Fruit":"#F472B6","Vegetable":"#34D399","Grain":"#FBBF24","Protein":"#38BDF8","Dairy":"#E2E8F0","Nuts & Treats":"#FB923C"}
SEQ = ["#34D399","#38BDF8","#FBBF24","#FB7185"]
GOOD = [n for n,v in NUT.items() if v[2]=="good"]
LIMIT = [n for n,v in NUT.items() if v[2]=="limit" and n!="Fat"] + ["Fat"]
 
 
@st.cache_data
def load() -> pd.DataFrame:
    d = pd.DataFrame(ROWS, columns=COLS)
    d["Log Calories"] = np.log1p(d["Calories"])          # CO1: transformation
    return d
 
 
def theme(fig, title="", h=380):
    fig.update_layout(template="plotly_dark", title=dict(text=f"<b>{title}</b>", x=0.01, font=dict(size=16, color="#F8FAFC")),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=h,
                      margin=dict(l=10, r=10, t=55, b=20), font=dict(size=12, color="#E2E8F0"),
                      legend=dict(font=dict(color="#E2E8F0")),
                      hoverlabel=dict(bgcolor="#0F172A", font=dict(color="#F8FAFC")))
    fig.update_xaxes(gridcolor="#334155", zerolinecolor="#475569", linecolor="#475569")
    fig.update_yaxes(gridcolor="#334155", zerolinecolor="#475569", linecolor="#475569")
    return fig
 
 
def html_table(d, index=True):
    """Readable dark table (the built-in grid follows the browser theme and can turn white)."""
    st.markdown('<div class="tw">' + d.to_html(index=index, classes="ft", border=0) + '</div>', unsafe_allow_html=True)
 
 
def tip(text):
    st.markdown(f'<div class="tip">💡 {text}</div>', unsafe_allow_html=True)
 
 
def pctile(df, n, v):
    return float((df[n] < v).mean() * 100)
 
 
df = load()
 
# ------------------------------------------------------------------ SIDEBAR
with st.sidebar:
    st.header("🥗 Choose a food")
    cat = st.selectbox("Category", ["All"] + sorted(df["Category"].unique()))
    pool = df if cat == "All" else df[df["Category"] == cat]
    food = st.selectbox("Food", pool["Food"].tolist())
    grams = st.slider("Serving size (grams)", 10, 500, 100, 10)
    st.caption("Approximate values per 100 g, scaled to your serving. "
               "Daily values (DV) assume a 2000 kcal diet.")
 
r = df[df["Food"] == food].iloc[0]
k = grams / 100
v = {n: r[n] * k for n in NUT}                                    # per serving
dv = {n: v[n] / NUT[n][1] * 100 for n in NUT}                     # % daily value
pc = {n: pctile(df, n, r[n]) for n in NUT}                        # rank vs all foods
 
# ------------------------------------------------------------------ HEADER + PLAIN-ENGLISH SUMMARY
strong = [n for n in GOOD if pc[n] >= 75 and r[n] > 0]
watch = [n for n in LIMIT if pc[n] >= 75 and r[n] > 0]
st.markdown(f'<div class="hero"><h1>🥗 {food}</h1><p>{r["Category"]} · {grams} g serving · '
            f'<b>{v["Calories"]:.0f} kcal</b> ({dv["Calories"]:.0f}% of a day\'s energy)</p>'
            + "".join(f'<span class="chip good">✔ High in {n.lower()}</span>' for n in strong)
            + "".join(f'<span class="chip bad">⚠ High in {n.lower()}</span>' for n in watch)
            + ('' if strong or watch else '<span class="chip good">Balanced, moderate food</span>')
            + '</div>', unsafe_allow_html=True)
 
c = st.columns(6)
for col, n in zip(c, ["Calories", "Protein", "Carbs", "Fat", "Fibre", "Sugar"]):
    col.metric(n, f"{v[n]:.0f} {NUT[n][0]}" if n == "Calories" else f"{v[n]:.1f} {NUT[n][0]}")
 
t1, t2, t3, t4, t5 = st.tabs(["🍽️ This food", "🏆 How it ranks", "⚖️ Compare foods",
                              "🔗 Relationships", "🕸️ Similar foods"])
 
# ------------------------------------------------------------------ TAB 1  (CO1 transformations, CO3 graphs)
with t1:
    a, b = st.columns([2, 3])
    with a:
        macro = pd.DataFrame({"Macro": ["Protein", "Carbs", "Fat"],
                              "kcal": [r.Protein*4, r.Carbs*4, r.Fat*9]})
        f = px.pie(macro, names="Macro", values="kcal", hole=.6, color="Macro", color_discrete_map=MCOL)
        f.update_traces(textinfo="label+percent", sort=False, textfont=dict(color="#0F172A", size=13), marker=dict(line=dict(color="#1E293B", width=2)))
        f.add_annotation(text=f"<b>{v['Calories']:.0f}</b><br>kcal", showarrow=False, font=dict(size=20))
        st.plotly_chart(theme(f, "Where the calories come from", 360).update_layout(showlegend=False), width="stretch")
        tip("Fat gives 9 kcal per gram, protein and carbs give 4. A food can be small in grams of fat but still get "
            "a big share of its calories from it.")
    with b:
        names = list(NUT)
        f = go.Figure(go.Bar(y=names, x=[dv[n] for n in names], orientation="h",
                             marker_color=[KCOL[NUT[n][2]] for n in names],
                             text=[f"{v[n]:.1f} {NUT[n][0]} · {dv[n]:.0f}%" for n in names], textposition="outside"))
        for x0 in (5, 20):
            f.add_vline(x=x0, line_dash="dot", line_color="#CBD5E1")
        f.update_yaxes(autorange="reversed")
        f.update_xaxes(title="% of daily value", range=[0, max(60, min(max(dv.values()) * 1.35, 400))])
        st.plotly_chart(theme(f, "Every nutrient in your serving", 430), width="stretch")
        tip("<b>Green</b> = nutrients you want enough of, <b>orange</b> = nutrients to limit, <b>blue</b> = energy. "
            "Dotted lines mark 5% (low source) and 20% (high source) of the daily value.")
 
    cat_avg = df[df["Category"] == r["Category"]][list(NUT)].mean()
    mx = df[list(NUT)].max()
    ax = ["Protein", "Fibre", "Vitamin C", "Calcium", "Iron", "Potassium"]
    f = go.Figure()
    f.add_scatterpolar(r=[cat_avg[n]/mx[n]*100 for n in ax]+[cat_avg[ax[0]]/mx[ax[0]]*100], theta=ax+[ax[0]],
                       name=f"Average {r['Category']}", line_color="#FBBF24", fill="toself", opacity=.45)
    f.add_scatterpolar(r=[r[n]/mx[n]*100 for n in ax]+[r[ax[0]]/mx[ax[0]]*100], theta=ax+[ax[0]],
                       name=food, line_color="#34D399", fill="toself", opacity=.6)
    f.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(range=[0, 100], showticklabels=False, gridcolor="#475569"),
                               angularaxis=dict(gridcolor="#475569", tickfont=dict(size=13, color="#F8FAFC"))))
    st.plotly_chart(theme(f, f"{food} vs the average {r['Category'].lower()}", 400), width="stretch")
    tip("Each axis is scaled so 100 is the best food in the whole list. A wider green shape means more of "
        "those vitamins and minerals than the typical food in its group.")
 
    with st.expander("📐 How these numbers were calculated (CO1: transformations)"):
        st.markdown(f"""
* **Serving scaling:** value per 100 g × {grams} ÷ 100. Protein: {r.Protein:.1f} × {k:.2f} = **{v['Protein']:.1f} g**
* **% daily value:** amount ÷ daily value × 100. Protein: {v['Protein']:.1f} ÷ 50 = **{dv['Protein']:.0f}%**
* **Calories from macros:** protein×4 + carbs×4 + fat×9 = {r.Protein*4:.0f} + {r.Carbs*4:.0f} + {r.Fat*9:.0f} kcal
* **Log transform:** log(1 + calories) = {r['Log Calories']:.2f}, used to compress very high-calorie foods.""")
 
# ------------------------------------------------------------------ TAB 2  (CO2 single variable, summaries)
with t2:
    names = list(NUT)
    f = go.Figure(go.Bar(y=names, x=[pc[n] for n in names], orientation="h",
                         marker_color=[KCOL[NUT[n][2]] for n in names],
                         text=[f"higher than {pc[n]:.0f}% of foods" for n in names], textposition="inside",
                         insidetextfont=dict(color="#0F172A", size=12)))
    f.update_yaxes(autorange="reversed"); f.update_xaxes(range=[0, 100], title="percentile among all foods")
    st.plotly_chart(theme(f, f"How {food} compares with all {len(df)} foods", 430), width="stretch")
    tip("A bar at 90 means this food has more of that nutrient than 90% of the foods in the list. "
        "Long green bars are strengths; long orange bars are things to watch.")
 
    m = st.selectbox("Rank all foods by", names, index=1)
    rk = df.sort_values(m, ascending=False)
    rk["Pick"] = np.where(rk["Food"] == food, "Selected", "Other foods")
    f = px.bar(rk, x=m, y="Food", orientation="h", color="Pick",
               color_discrete_map={"Selected": "#34D399", "Other foods": "#64748B"})
    f.update_yaxes(autorange="reversed", tickfont=dict(size=10)).update_layout(showlegend=False)
    st.plotly_chart(theme(f, f"{m} per 100 g ({NUT[m][0]}), highest to lowest", 760), width="stretch")
    pos = rk["Food"].tolist().index(food) + 1
    tip(f"<b>{food}</b> is <b>#{pos} of {len(df)}</b> for {m.lower()}. Average of all foods: {df[m].mean():.1f}, "
        f"median: {df[m].median():.1f}, highest: {df[m].max():.1f} ({rk.iloc[0]['Food']}).")
    html_table(df[list(NUT)].describe().T.round(2))
 
# ------------------------------------------------------------------ TAB 3  (CO4 compare characteristics)
with t3:
    others = st.multiselect("Compare with (up to 3)", [x for x in df["Food"] if x != food],
                            default=[x for x in ["Chicken breast (cooked)", "Almonds"] if x != food][:2],
                            max_selections=3)
    sel = [food] + others
    sub = df[df["Food"].isin(sel)].set_index("Food").loc[sel]
    long = (sub[list(NUT)] * k / pd.Series({n: NUT[n][1] for n in NUT}) * 100).reset_index().melt("Food", var_name="Nutrient", value_name="% DV")
    f = px.bar(long, x="Nutrient", y="% DV", color="Food", barmode="group", color_discrete_sequence=SEQ)
    st.plotly_chart(theme(f, f"Nutrients in {grams} g of each food (% of daily value)", 430), width="stretch")
    tip("Taller bar = more of that nutrient. Look for the food that wins on the nutrients you care about.")
    show = (sub[list(NUT)] * k).round(1).T
    show.index = [f"{n} ({NUT[n][0]})" for n in show.index]
    html_table(show)
    if others:
        winners = {n: sub[n].idxmax() for n in ["Protein", "Fibre", "Vitamin C", "Calcium", "Iron"]}
        st.markdown("**Best of this group:** " + " · ".join(f"{n}: **{w}**" for n, w in winners.items()))
 
# ------------------------------------------------------------------ TAB 4  (CO1 relationships, CO4 correlation)
with t4:
    x, y = st.columns(2)
    xa = x.selectbox("X axis", list(NUT), index=1)
    ya = y.selectbox("Y axis", list(NUT), index=0)
    f = px.scatter(df, x=xa, y=ya, color="Category", hover_name="Food", opacity=.9, color_discrete_map=GCOL)
    if xa != ya:
        m_, c_ = np.polyfit(df[xa], df[ya], 1)
        xs = np.array([df[xa].min(), df[xa].max()])
        f.add_scatter(x=xs, y=m_*xs+c_, mode="lines", line=dict(dash="dash", color="#CBD5E1"), name="trend")
    f.add_scatter(x=[r[xa]], y=[r[ya]], mode="markers+text", text=[food], textposition="top center",
                  marker=dict(size=20, color="rgba(0,0,0,0)", line=dict(width=3, color="white")), showlegend=False, textfont=dict(color="#fff", size=13))
    st.plotly_chart(theme(f, f"{ya} vs {xa} (per 100 g)", 480), width="stretch")
    if xa != ya:
        rr = df[xa].corr(df[ya])
        word = "strong" if abs(rr) >= .7 else "moderate" if abs(rr) >= .4 else "weak"
        tip(f"Correlation r = <b>{rr:.2f}</b>: a <b>{word} {'positive' if rr > 0 else 'negative'}</b> relationship. "
            "Positive means that when one goes up, the other usually goes up too.")
    cm = df[list(NUT)].corr()
    f = px.imshow(cm, text_auto=".2f", color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
    st.plotly_chart(theme(f, "Which nutrients move together?", 520), width="stretch")
    pairs = cm.where(np.triu(np.ones(cm.shape), 1).astype(bool)).stack().sort_values()
    tip(f"Strongest link: <b>{pairs.index[-1][0]} and {pairs.index[-1][1]}</b> (r = {pairs.iloc[-1]:.2f}). "
        f"Strongest opposite: <b>{pairs.index[0][0]} and {pairs.index[0][1]}</b> (r = {pairs.iloc[0]:.2f}).")
 
# ------------------------------------------------------------------ TAB 5  (CO3 networks, CO5 connections)
with t5:
    feats = ["Calories", "Protein", "Carbs", "Fat", "Fibre", "Sugar", "Vitamin C", "Calcium", "Iron", "Potassium"]
    z = (df[feats] - df[feats].mean()) / df[feats].std()
    dist = np.sqrt(((z - z[df["Food"] == food].values[0]) ** 2).sum(axis=1))
    sim = df.assign(Distance=dist)[df["Food"] != food].nsmallest(6, "Distance")
    ang = np.linspace(0, 2 * np.pi, len(sim), endpoint=False)
    px_, py_ = np.cos(ang), np.sin(ang)
    f = go.Figure()
    for xi, yi in zip(px_, py_):
        f.add_scatter(x=[0, xi], y=[0, yi], mode="lines", line=dict(color="#64748B", width=2), showlegend=False, hoverinfo="skip")
    f.add_scatter(x=px_, y=py_, mode="markers+text", text=sim["Food"], textposition="top center", textfont=dict(color="#F8FAFC", size=13),
                  marker=dict(size=24, color=[GCOL[x_] for x_ in sim["Category"]], line=dict(width=2, color="#0F172A")),
                  hovertext=[f"{a} · {b}" for a, b in zip(sim["Food"], sim["Category"])], showlegend=False)
    f.add_scatter(x=[0], y=[0], mode="markers+text", text=[food], textposition="bottom center",
                  marker=dict(size=38, color="#34D399", line=dict(width=3, color="#fff")), textfont=dict(color="#fff", size=15), showlegend=False)
    f.update_xaxes(visible=False, range=[-1.6, 1.6]); f.update_yaxes(visible=False, range=[-1.5, 1.5])
    st.plotly_chart(theme(f, f"Foods most similar to {food}", 520), width="stretch")
    tip("Foods are linked to the selected food when their overall nutrient profile is close. Colours show the "
        "food group, so you can see swaps that stay in or leave the group.")
    html_table(sim[["Food", "Category", "Calories", "Protein", "Carbs", "Fat", "Fibre"]].round(1), index=False)
    f = px.treemap(df, path=["Category", "Food"], values="Calories", color="Protein",
                   color_continuous_scale="Tealgrn")
    st.plotly_chart(theme(f, "Food groups: box size = calories, colour = protein", 520), width="stretch")
    st.download_button("⬇ Download dataset (CSV)", df.to_csv(index=False).encode(), "food_nutrition.csv", "text/csv")