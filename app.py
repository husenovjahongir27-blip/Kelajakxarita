import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="KelajakXarita", page_icon="🌍", layout="wide")
st.markdown("""
<style>
.block-container{padding-top:1rem;max-width:1600px}
[data-testid="stSidebar"]{background:#0b2030}
[data-testid="stSidebar"] *{color:#eefaff}
.hero{padding:22px;border-radius:16px;background:linear-gradient(120deg,#071826,#0c4a56);color:white;border:1px solid #16716e}
.hero h1{color:white;margin:0}.hero p{color:#c4e5e8;margin-bottom:0}
div[data-testid="stMetric"]{background:#102b3a;border:1px solid #205467;padding:12px;border-radius:12px}
div[data-testid="stMetric"] label,div[data-testid="stMetric"] [data-testid="stMetricValue"]{color:#f5ffff}
</style>""", unsafe_allow_html=True)

places = {
"Sirdaryo viloyati":(40.55,68.78,10),"Guliston shahri":(40.4897,68.7842,12),
"Yangiyer shahri":(40.275,68.822,12),"Shirin shahri":(40.22,69.14,12),
"Boyovut tumani":(40.58,68.90,11),"Guliston tumani":(40.55,68.75,11),
"Mirzaobod tumani":(40.45,68.95,11),"Oqoltin tumani":(40.27,68.98,11),
"Sardoba tumani":(40.20,68.75,11),"Sayxunobod tumani":(40.66,68.66,11),
"Sirdaryo tumani":(40.83,68.66,11),"Xovos tumani":(40.27,68.62,11)}
if "saved" not in st.session_state: st.session_state.saved=[]

with st.sidebar:
    st.markdown("## 🌍 KelajakXarita")
    st.caption("Hududiy ssenariylar laboratoriyasi")
    region=st.selectbox("Hudud",list(places))
    show_orientirs=st.checkbox("Yaqin orientirlarni ko‘rsatish",True)
    show_scenario=st.checkbox("Ssenariy belgilarini ko‘rsatish",True)
    map_type=st.selectbox("Xarita qatlami",["OpenStreetMap","Soddalashtirilgan"])
    st.divider()
    year=st.select_slider("Ssenariy yili",[2027,2030,2035,2040],value=2030)
    st.markdown("### O‘zgartiriladigan taxminlar")
    green=st.slider("Yashil hududlar (%)",-30,50,10,5)
    water=st.slider("Suv mavjudligi (%)",-40,40,0,5)
    built=st.slider("Qurilgan maydon (%)",-20,40,5,5)
    rain=st.slider("Yog‘in miqdori (%)",-30,50,0,5)
    farm=st.slider("Sug‘oriladigan yerlar (%)",-30,20,0,5)
    people=st.slider("Aholi o‘zgarishi (%)",-10,60,15,5)

lat,lon,zoom=places[region]
st.markdown(f'<div class="hero"><h1>🌍 KelajakXarita</h1><p>Bugungi hududni o‘rganing. Muqobil kelajak ssenariylarini solishtiring. · Sirdaryo pilot loyihasi</p></div>',unsafe_allow_html=True)
st.warning("DEMO: ko‘rsatkichlar namoyish uchun, haqiqiy prognoz emas. Xarita nuqtalari orientir bo‘lib, rasmiy ma’muriy chegaralar hisoblanmaydi.")

score=max(0,min(100,50+0.30*green+0.25*water-0.20*built+0.08*rain+0.10*farm-0.05*max(people,0)))
m1,m2,m3,m4=st.columns(4)
m1.metric("Hudud",region);m2.metric("Ssenariy yili",str(year));m3.metric("Shartli taqqoslash bali",f"{score:.1f}/100",f"{score-50:+.1f}");m4.metric("Sozlanadigan omillar","6 ta")

tabmap,tabsc,tabdata,tababout=st.tabs(["🗺️ Xarita","🔮 Ssenariylar","📊 Tahlil va eksport","ℹ️ Loyiha haqida"])
with tabmap:
    c1,c2=st.columns([1.8,1])
    with c1:
        fmap=folium.Map(location=[lat,lon],zoom_start=zoom,tiles="OpenStreetMap" if map_type=="OpenStreetMap" else "CartoDB positron",control_scale=True)
        folium.Marker([lat,lon],tooltip=region,popup=f"{region} — orientir nuqtasi").add_to(fmap)
        if show_orientirs:
            for n,(a,b,z) in places.items():
                if n!=region and abs(a-lat)<.45 and abs(b-lon)<.55:
                    folium.CircleMarker([a,b],radius=4,color="#0fc9b5",fill=True,tooltip=n).add_to(fmap)
        if show_scenario:
            for da,db,label,color in [(0.08,-0.08,"Yashil hudud","#12bca8"),(-.07,.1,"Suv resurslari","#168dd2"),(.04,.13,"Qurilish","#e6a23c")]:
                folium.CircleMarker([lat+da,lon+db],radius=8,color=color,fill=True,fill_color=color,fill_opacity=.7,tooltip=label+" — shartli belgi").add_to(fmap)
        st_folium(fmap,use_container_width=True,height=520,returned_objects=[])
        st.caption("Xarita qatlamlari internetga bog‘liq. Markerlar ko‘rgazmali; real obyektlar o‘lchovi emas.")
    with c2:
        st.subheader("Ssenariy parametrlari")
        for n,v in [("Yashil hududlar",green),("Suv mavjudligi",water),("Qurilish",built),("Yog‘in",rain),("Sug‘oriladigan yerlar",farm),("Aholi",people)]:
            st.write(f"{n}: **{v:+d}%**")
        st.info("Keyingi bosqich: rasmiy tuman poligonlari va sanasi ko‘rsatilgan sun’iy yo‘ldosh qatlamlari.")

with tabsc:
    scen=pd.DataFrame([
        {"Ssenariy":"Boshlang‘ich holat","Shartli ball":50,"Yashil hududlar (%)":0,"Suv (%)":0,"Qurilish (%)":0},
        {"Ssenariy":"Sizning ssenariyingiz","Shartli ball":score,"Yashil hududlar (%)":green,"Suv (%)":water,"Qurilish (%)":built},
        {"Ssenariy":"Yashil rivojlanish (namuna)","Shartli ball":54.5,"Yashil hududlar (%)":20,"Suv (%)":10,"Qurilish (%)":5},
        {"Ssenariy":"Tez urbanizatsiya (namuna)","Shartli ball":44.5,"Yashil hududlar (%)":-10,"Suv (%)":-10,"Qurilish (%)":25}])
    fig=px.bar(scen,x="Ssenariy",y="Shartli ball",color="Ssenariy",text_auto=".1f",title="Ssenariylarni taqqoslash — namoyish bali")
    fig.update_layout(showlegend=False,yaxis_range=[0,100],xaxis_title="",yaxis_title="Shartli ball")
    st.plotly_chart(fig,use_container_width=True);st.dataframe(scen,use_container_width=True,hide_index=True)
    name=st.text_input("Ssenariy nomi",f"{region} — {year}")
    if st.button("💾 Ssenariyni saqlash",type="primary"):
        st.session_state.saved.append({"Nomi":name,"Hudud":region,"Yil":year,"Yashil (%)":green,"Suv (%)":water,"Qurilish (%)":built,"Yog‘in (%)":rain,"Sug‘oriladigan yer (%)":farm,"Aholi (%)":people,"Shartli ball":round(score,1)})
        st.success("Ssenariy joriy sessiyada saqlandi.")
    if st.session_state.saved: st.dataframe(pd.DataFrame(st.session_state.saved),use_container_width=True,hide_index=True)

with tabdata:
    rows=[]
    for label,val in [("Yashil hududlar",green),("Suv mavjudligi",water),("Qurilgan maydon",built),("Yog‘in",rain),("Sug‘oriladigan yerlar",farm),("Aholi",people)]:
        rows.append({"Omil":label,"Boshlang‘ich indeks":100,"Ssenariy indeksi":max(0,100+val),"Farq (%)":val})
    df=pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True,hide_index=True)
    timeline=pd.DataFrame({"Yil":[2024,2027,2030,2035,2040],"Yashil hududlar":[100,100+green*.3,100+green*.6,100+green*.85,100+green],"Suv":[100,100+water*.3,100+water*.6,100+water*.85,100+water],"Qurilish":[100,100+built*.3,100+built*.6,100+built*.85,100+built]})
    fig=px.line(timeline,x="Yil",y=["Yashil hududlar","Suv","Qurilish"],markers=True,title="Vaqt bo‘yicha shartli o‘zgarish")
    st.plotly_chart(fig,use_container_width=True)
    st.download_button("⬇️ Jadvalni CSV qilib yuklab olish",df.to_csv(index=False).encode("utf-8-sig"),"kelajakxarita.csv","text/csv")
    report=f"""# KelajakXarita ssenariy hisoboti
Yaratilgan: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Hudud: {region}
Ssenariy yili: {year}
Shartli taqqoslash bali: {score:.1f}/100

Taxminlar: yashil hududlar {green:+d}%, suv {water:+d}%, qurilish {built:+d}%, yog‘in {rain:+d}%, sug‘oriladigan yerlar {farm:+d}%, aholi {people:+d}%.
MUHIM: Bu prototip hisoboti. Ball kalibrlanmagan va haqiqiy prognoz yoki rasmiy statistika emas.
"""
    st.download_button("⬇️ Hisobotni yuklab olish",report,"kelajakxarita_hisobot.md","text/markdown")

with tababout:
    st.markdown("""### Loyiha nima qiladi?
KelajakXarita — hududning bugungi holati va foydalanuvchi kiritgan taxminlar asosida muqobil ssenariylarni solishtirish laboratoriyasi.

**Mavjud:** interaktiv xarita, parametrlar, ssenariy taqqoslash, grafiklar, CSV va hisobot eksporti.

**Hali ulanmagan:** rasmiy ma’muriy chegaralar, tarixiy Landsat/Sentinel-2 tasvirlari, NDVI/NDWI hisoblash, serverda saqlash va foydalanuvchi akkauntlari.

**Ilmiy ishonchlilik:** bu relizdagi indeks faqat namoyish uchun. Haqiqiy prognoz uchun manbasi tekshirilgan ma’lumotlar, hujjatlashtirilgan model va validatsiya zarur.

**Texnologiyalar:** Python, Streamlit, Folium, OpenStreetMap, Plotly, Pandas.""")
st.divider()
st.caption("KelajakXarita MVP v0.2 · Sirdaryo pilot · Namoyish prototipi")
