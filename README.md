# KelajakXarita MVP v0.2

Sirdaryo viloyati uchun hududiy ssenariylarni ko‘rish va taqqoslash prototipi.

## Imkoniyatlar
- Sirdaryo viloyati va ayrim shahar/tumanlar xarita markazlari
- Interaktiv OpenStreetMap/CARTO xaritasi va ko‘rgazmali markerlar
- Yashil hudud, suv, qurilish, yog‘in, sug‘oriladigan yerlar va aholi taxminlarini sozlash
- Ssenariylarni grafikda taqqoslash
- Joriy sessiyada ssenariy saqlash
- CSV va Markdown hisobotini yuklab olish

## Muhim cheklov
Shartli ball formulasi faqat interfeysni namoyish qilish uchun. U kalibrlanmagan, haqiqiy ekologik prognoz emas. Xarita nuqtalari orientirlar, rasmiy tuman chegaralari emas. Amaliy qarorlarda ishlatmang.

## Windows kompyuterda ishga tushirish
Python 3.10+ o‘rnating, ZIPni oching, shu papkada PowerShell ochib bajaring:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Brauzerda `http://localhost:8501` oching.

Agar virtual muhitni faollashtirish bloklansa:
```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run app.py
```

## Internetga joylashtirish
1. GitHub’da `kelajakxarita` nomli repository yarating.
2. `app.py`, `requirements.txt`, `README.md` fayllarini repository root’iga yuklang.
3. Streamlit Community Cloud’ga GitHub orqali kiring, repository va `app.py` ni tanlab Deploy qiling.
4. Xizmat sizga ommaviy `*.streamlit.app` manzil beradi.

Deploy uchun hisobga kirish va foydalanuvchi tasdig‘i kerak; ushbu ZIP hali internetga joylashtirilmagan. Maxfiy kalitlarni kodga yozmang.

## Keyingi bosqichlar
1. Rasmiy ma’muriy chegara qatlamlarini tekshirib ulash.
2. Landsat/Sentinel-2 va NDVI/NDWI qatlamlarini sanasi hamda manbasi bilan qo‘shish.
3. Modelni tarixiy kuzatuvlar bilan kalibrlash va mustaqil tekshirish.
4. Ma’lumotlar bazasi, login va doimiy saqlashni qo‘shish.
