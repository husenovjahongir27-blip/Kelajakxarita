        )

    st.info(
        "Chap xarita boshlang‘ich ko‘rinish. O‘ng xaritadagi doiralar "
        "tanlangan parametrlar va yilga qarab o‘zgaradi. Bu qatlamlar "
        "hozircha ko‘rgazmali demo, haqiqiy ekologik prognoz emas. "
        "Haqiqiy taqqoslash uchun rasmiy GIS chegaralari va tarixiy "
        "sun’iy yo‘ldosh ma’lumotlari kerak."
    )
    st.subheader("Ssenariy parametrlari")
    cols = st.columns(3)
    for i, (name, value) in enumerate([
        ("Yashil hududlar", green), ("Suv mavjudligi", water),
        ("Qurilish", built), ("Yog‘in", rain),
        ("Sug‘oriladigan yerlar", farm), ("Aholi", people),
    ]):
        cols[i % 3].write(f"**{name}:** {value:+d}%")


with tabsc:
    scen = pd.DataFrame([
        {"Ssenariy": "Boshlang‘ich holat", "Shartli ball": 50,
         "Yashil hududlar (%)": 0, "Suv (%)": 0, "Qurilish (%)": 0},
        {"Ssenariy": "Sizning ssenariyingiz", "Shartli ball": score,
         "Yashil hududlar (%)": green, "Suv (%)": water, "Qurilish (%)": built},
        {"Ssenariy": "Yashil rivojlanish (namuna)", "Shartli ball": 54.5,
         "Yashil hududlar (%)": 20, "Suv (%)": 10, "Qurilish (%)": 5},
        {"Ssenariy": "Tez urbanizatsiya (namuna)", "Shartli ball": 44.5,
         "Yashil hududlar (%)": -10, "Suv (%)": -10, "Qurilish (%)": 25},
    ])
    fig = px.bar(
        scen, x="Ssenariy", y="Shartli ball", color="Ssenariy",
        text_auto=".1f", title="Ssenariylarni taqqoslash — namoyish bali"
    )
    fig.update_layout(
        showlegend=False, yaxis_range=[0, 100],
        xaxis_title="", yaxis_title="Shartli ball"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(scen, use_container_width=True, hide_index=True)

    name = st.text_input("Ssenariy nomi", f"{region} — {year}")
    if st.button("💾 Ssenariyni saqlash", type="primary"):
        st.session_state.saved.append({
            "Nomi": name, "Hudud": region, "Yil": year,
            "Yashil (%)": green, "Suv (%)": water, "Qurilish (%)": built,
            "Yog‘in (%)": rain, "Sug‘oriladigan yer (%)": farm,
            "Aholi (%)": people, "Shartli ball": round(score, 1),
        })
        st.success("Ssenariy joriy sessiyada saqlandi.")
    if st.session_state.saved:
        st.dataframe(
            pd.DataFrame(st.session_state.saved),
            use_container_width=True, hide_index=True
        )


with tabdata:
    df = pd.DataFrame([
        {"Omil": name, "Boshlang‘ich indeks": 100,
         "Ssenariy indeksi": max(0, 100 + value), "Farq (%)": value}
        for name, value in [
            ("Yashil hududlar", green), ("Suv mavjudligi", water),
            ("Qurilgan maydon", built), ("Yog‘in", rain),
            ("Sug‘oriladigan yerlar", farm), ("Aholi", people),
        ]
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

    timeline = pd.DataFrame({
        "Yil": [2024, 2027, 2030, 2035, 2040],
        "Yashil hududlar": [
            100, 100 + green * 0.3, 100 + green * 0.6,
            100 + green * 0.85, 100 + green
        ],
        "Suv": [
            100, 100 + water * 0.3, 100 + water * 0.6,
            100 + water * 0.85, 100 + water
        ],
        "Qurilish": [
            100, 100 + built * 0.3, 100 + built * 0.6,
            100 + built * 0.85, 100 + built
        ],
    })
    st.plotly_chart(
        px.line(
            timeline, x="Yil",
            y=["Yashil hududlar", "Suv", "Qurilish"],
            markers=True, title="Vaqt bo‘yicha shartli o‘zgarish"
        ),
        use_container_width=True,
    )
    st.download_button(
        "⬇️ Jadvalni CSV qilib yuklab olish",
        df.to_csv(index=False).encode("utf-8-sig"),
        "kelajakxarita.csv", "text/csv"
    )

    report = f"""# KelajakXarita ssenariy hisoboti
Yaratilgan: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Hudud: {region}
Ssenariy yili: {year}
Shartli taqqoslash bali: {score:.1f}/100

Taxminlar: yashil hududlar {green:+d}%, suv {water:+d}%, qurilish {built:+d}%, yog‘in {rain:+d}%, sug‘oriladigan yerlar {farm:+d}%, aholi {people:+d}%.

MUHIM: ball kalibrlanmagan va haqiqiy prognoz yoki rasmiy statistika emas.
"""
    st.download_button(
        "⬇️ Hisobotni yuklab olish", report,
        "kelajakxarita_hisobot.md", "text/markdown"
    )


with tababout:
    st.markdown("""### Loyiha nima qiladi?
KelajakXarita — hududning bugungi holati va foydalanuvchi kiritgan
taxminlar asosida muqobil ssenariylarni solishtirish laboratoriyasi.

**Mavjud:** ikki interaktiv xarita, parametrlar, ssenariy taqqoslash,
grafiklar, CSV va hisobot eksporti.

**Hali ulanmagan:** rasmiy ma’muriy chegaralar, tarixiy Landsat/Sentinel-2
tasvirlari, NDVI/NDWI hisoblash, serverda saqlash va foydalanuvchi akkauntlari.

**Ilmiy ishonchlilik:** indeks va xaritadagi doiralar faqat namoyish uchun.
Haqiqiy prognoz uchun manbasi tekshirilgan ma’lumotlar, hujjatlashtirilgan
model va validatsiya zarur.
