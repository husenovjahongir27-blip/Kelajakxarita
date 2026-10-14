import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(page_title="KelajakXarita", page_icon="🌍", layout="wide")
st.markdown("""<style>
.block-container{padding-top:1rem;max-width:1800px}
[data-testid="stSidebar"]{background:#0b2030}
[data-testid="stSidebar"] *{color:#eefaff}
.hero{padding:22px;border-radius:16px;background:linear-gradient(120deg,#071826,#0c4a56);color:white}
.hero h1{color:white;margin:0}.hero p{color:#c4e5e8}
.map-heading{font-size:1.1rem;font-weight:700;margin-bottom:.2rem}
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
st.markdown('<div class="hero"><h1>🌍 KelajakXarita</h1><p>Bugungi hududni o‘rganing. Muqobil kelajak ssenariylarini solishtiring · Sirdaryo pilot</p></div>',unsafe_allow_html=True)
st.warning("DEMO: ko‘rsatkichlar namoyish uchun, haqiqiy prognoz emas. Rangli belgilar shartli; rasmiy chegaralar emas.")
score=max(0,min(100,50+0.30*green+0.25*water-0.20*built+0.08*rain+0.10*farm-0.05*max(people,0)))
m1,m2,m3,m4=st.columns(4)
m1.metric("Hudud",region);m2.metric("Ssenariy yili",str(year));m3.metric("Shartli taqqoslash bali",f"{score:.1f}/100",f"{score-50:+.1f}");m4.metric("Sozlanadigan omillar","6 ta")
tabmap,tabsc,tabdata,tababout=st.tabs(["🗺️ Xaritalar taqqoslanishi","🔮 Ssenariylar","📊 Tahlil va eksport","ℹ️ Loyiha haqida"])

def make_map(location, zoom, scenario=False):
    fmap=folium.Map(location=location,zoom_start=zoom,tiles="OpenStreetMap" if map_type=="OpenStreetMap" else "CartoDB positron",control_scale=True)
    folium.Marker(location,tooltip=region,popup=f"{region} — orientir nuqtasi").add_to(fmap)
    if show_orientirs:
        for n,(a,b,z) in places.items():
            if n!=region and abs(a-location[0])<.45 and abs(b-location[1])<.55:
                folium.CircleMarker([a,b],radius=4,color="#0fc9b5",fill=True,fill_opacity=.8,tooltip=n).add_to(fmap)
    if scenario and show_scenario:
        for da,db,label,color,value in [(0.08,-0.08,"Yashil hudud","#12bca8",green),(-.07,.1,"Suv resurslari","#168dd2",water),(.04,.13,"Qurilish","#e6a23c",built)]:
            folium.CircleMarker([location[0]+da,location[1]+db],radius=max(5,min(14,7+abs(value)/8)),color=color,fill=True,fill_color=color,fill_opacity=.72,tooltip=f"{label} — shartli belgi ({value:+d}%)").add_to(fmap)
    return fmap

with tabmap:
    st.subheader("Bir xil hudud: boshlang‘ich xarita va ssenariy xaritasi")
    st.caption("Ikkala xarita bir hudud markazida. O‘ngdagi rangli belgilar ko‘rgazmali, haqiqiy o‘zgarish poligonlari emas.")
    left,right=st.columns(2,gap="medium")
    with left:
        st.markdown('<div class="map-heading">1. Hozirgi / boshlang‘ich ko‘rinish</div>',unsafe_allow_html=True)
        st.caption("Orientir xaritasi · rasmiy o‘lchov emas")
        st_folium(make_map([lat,lon],zoom,False),key="base_map",use_container_width=True,height=500,returned_objects=[])
    with right:
        st.markdown(f'<div class="map-heading">2. {year}-yil ssenariysi</div>',unsafe_allow_html=True)
        st.caption("Shartli parametrlar asosidagi ko‘rgazmali belgilar")
        st_folium(make_map([lat,lon],zoom,True),key="future_map",use_container_width=True,height=500,returned_objects=[])
    st.info("Hozir ikkala xarita ham OpenStreetMap asosida. Kelajak xaritasidagi belgilar haqiqiy prognoz emas. Haqiqiy taqqoslash uchun tarixiy sun’iy yo‘ldosh tasvirlari va GIS tahlili ulanishi kerak.")
    st.subheader("Ssenariy parametrlari")
    cols=st.columns(3)
    for i,(n,v) in enumerate([("Yashil hududlar",green),("Suv mavjudligi",water),("Qurilish",built),("Yog‘in",rain),("Sug‘oriladigan yerlar",farm),("Aholi",people)]):
        cols[i%3].write(f"**{n}:** {v:+d}%")

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
    df=pd.DataFrame([{"Omil":n,"Boshlang‘ich indeks":100,"Ssenariy indeksi":max(0,100+v),"Farq (%)":v} for n,v in [("Yashil hududlar",green),("Suv mavjudligi",water),("Qurilgan maydon",built),("Yog‘in",rain),("Sug‘oriladigan yerlar",farm),("Aholi",people)]])
    st.dataframe(df,use_container_width=True,hide_index=True)
    timeline=pd.DataFrame({"Yil":[2024,2027,2030,2035,2040],"Yashil hududlar":[100,100+green*.3,100+green*.6,100+green*.85,100+green],"Suv":[100,100+water*.3,100+water*.6,100+water*.85,100+water],"Qurilish":[100,100+built*.3,100+built*.6,100+built*.85,100+built]})
    st.plotly_chart(px.line(timeline,x="Yil",y=["Yashil hududlar","Suv","Qurilish"],markers=True,title="Vaqt bo‘yicha shartli o‘zgarish"),use_container_width=True)
    st.download_button("⬇️ Jadvalni CSV qilib yuklab olish",df.to_csv(index=False).encode("utf-8-sig"),"kelajakxarita.csv","text/csv")
    report=f"""# KelajakXarita ssenariy hisoboti
Yaratilgan: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Hudud: {region}
Ssenariy yili: {year}
Shartli taqqoslash bali: {score:.1f}/100
Taxminlar: yashil hududlar {green:+d}%, suv {water:+d}%, qurilish {built:+d}%, yog‘in {rain:+d}%, sug‘oriladigan yerlar {farm:+d}%, aholi {people:+d}%.
MUHIM: ball kalibrlanmagan va haqiqiy prognoz yoki rasmiy statistika emas.
"""
    st.download_button("⬇️ Hisobotni yuklab olish",report,"kelajakxarita_hisobot.md","text/markdown")

with tababout:
    st.markdown("""### Loyiha nima qiladi?
KelajakXarita — hududning bugungi holati va foydalanuvchi kiritgan taxminlar asosida muqobil ssenariylarni solishtirish laboratoriyasi.

**Mavjud:** ikki interaktiv xarita, parametrlar, ssenariy taqqoslash, grafiklar, CSV va hisobot eksporti.

**Hali ulanmagan:** rasmiy ma’muriy chegaralar, tarixiy Landsat/Sentinel-2 tasvirlari, NDVI/NDWI hisoblash, serverda saqlash va foydalanuvchi akkauntlari.

**Ilmiy ishonchlilik:** indeks faqat namoyish uchun. Haqiqiy prognoz uchun manbasi tekshirilgan ma’lumotlar, hujjatlashtirilgan model va validatsiya zarur.

**Texnologiyalar:** Python, Streamlit, Folium, OpenStreetMap, Plotly, Pandas.""")
st.divider();st.caption("KelajakXarita MVP v0.3 · Sirdaryo pilot · Ikki xaritali prototip")
