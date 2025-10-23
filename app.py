
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="BusinessGraph", page_icon="💼", layout="wide")

LANGS = {
    "kk": {
        "title": "💼 BusinessGraph",
        "subtitle": "Кәсіпкерлерге арналған онлайн пайда–шығын анализаторы",
        "about": "Баға, өзіндік құн және тұрақты шығын бойынша түсім, шығын, пайда функцияларын есептеп, графикпен көрсететін веб-қосымша.",
        "inputs": "📋 Деректер",
        "price": "Өнім бағасы (теңге)",
        "cost": "Өзіндік құн (теңге)",
        "fixed": "Тұрақты шығын (теңге)",
        "qtymax": "Максималды өнім саны",
        "calc": "📊 Есептеу және график салу",
        "results": "Нәтиже",
        "breakeven": "✅ Зиянсыздық нүктесі: шамамен {x0:.2f} дана өнім",
        "nobreakeven": "⚠️ Өнім бағасы өзіндік құннан төмен. Пайда болмайды.",
        "chart_title": "Функция графигін кәсіпорын экономикасында қолдану",
        "x": "Өнім саны (x)",
        "y": "Теңге",
        "revenue": "Түсім (T(x))",
        "costs": "Шығын (S(x))",
        "profit": "Пайда (P(x))",
        "download_csv": "Деректерді жүктеу (CSV)",
        "ai_header": "🤖 ЖИ талдауы",
        "ai_tip": "💡 Кеңес: {tip}",
        "footer": "© 2025 Перизат Жақсылықова",
    },
    "ru": {
        "title": "💼 BusinessGraph",
        "subtitle": "Онлайн анализатор прибыли и издержек для предпринимателей",
        "about": "Веб‑приложение рассчитывает функции выручки, издержек и прибыли по цене, себестоимости и постоянным расходам и показывает график.",
        "inputs": "📋 Данные",
        "price": "Цена продукта (тенге)",
        "cost": "Себестоимость (тенге)",
        "fixed": "Постоянные расходы (тенге)",
        "qtymax": "Максимальный объём продукции",
        "calc": "📊 Рассчитать и построить график",
        "results": "Результаты",
        "breakeven": "✅ Точка безубыточности: около {x0:.2f} единиц продукции",
        "nobreakeven": "⚠️ Цена ниже себестоимости. Прибыли не будет.",
        "chart_title": "Применение графика функции в экономике предприятия",
        "x": "Количество продукции (x)",
        "y": "Тенге",
        "revenue": "Выручка (T(x))",
        "costs": "Издержки (S(x))",
        "profit": "Прибыль (P(x))",
        "download_csv": "Скачать данные (CSV)",
        "ai_header": "🤖 AI‑анализ",
        "ai_tip": "💡 Совет: {tip}",
        "footer": "© 2025 Перизат Жақсылықова",
    }
}

lang = st.sidebar.selectbox("Language / Тіл", options=["kk", "ru"], format_func=lambda x: "Қазақша" if x=="kk" else "Русский")
T = LANGS[lang]

h1, h2 = st.columns([1,3])
with h1:
    st.image("banner.png", use_column_width=True)
with h2:
    st.markdown(f"## {T['title']}")
    st.markdown(f"**{T['subtitle']}**")
    st.caption(T["about"])

st.markdown("---")

left, right = st.columns([1,2])
with left:
    st.subheader(T["inputs"])
    price = st.number_input(T["price"], min_value=0.0, value=2000.0, step=100.0)
    cost  = st.number_input(T["cost"],  min_value=0.0, value=1200.0, step=100.0)
    fixed = st.number_input(T["fixed"], min_value=0.0, value=400000.0, step=10000.0)
    qty_max = st.slider(T["qtymax"], min_value=100, max_value=10000, value=1000, step=100)
    go = st.button(T["calc"], use_container_width=True)

with right:
    st.subheader(T["results"])
    if 'df' not in st.session_state:
        st.session_state['df'] = None

    if go:
        x = np.linspace(0, qty_max, 500)
        revenue = price * x
        costs = cost * x + fixed
        profit = revenue - costs

        df = pd.DataFrame({'x': x, 'revenue': revenue, 'costs': costs, 'profit': profit})
        st.session_state['df'] = df

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=revenue, mode='lines', name=T['revenue']))
        fig.add_trace(go.Scatter(x=x, y=costs,   mode='lines', name=T['costs']))
        fig.add_trace(go.Scatter(x=x, y=profit,  mode='lines', name=T['profit']))

        if price > cost:
            x0 = fixed / (price - cost)
            y0 = price * x0
            fig.add_trace(go.Scatter(x=[x0], y=[y0], mode='markers', name='BE', marker=dict(size=10)))
            st.success(T['breakeven'].format(x0=x0))
        else:
            st.error(T['nobreakeven'])

        fig.update_layout(
            title=T['chart_title'],
            xaxis_title=T['x'],
            yaxis_title=T['y'],
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=40, r=20, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(T['download_csv'], data=csv, file_name='businessgraph_data.csv', mime='text/csv')

        st.markdown(f"### {T['ai_header']}")
        tips_kk = [
            "Бағаны 5–10% көтеру зиянсыздық нүктесін жақындатады, бірақ сұраныстың өзгерісін ескеріңіз.",
            "Егер өзіндік құнды 5% азайтсаңыз, табыстылық айтарлықтай өседі.",
            "Тұрақты шығындар жоғары болса, сату көлемін көбейтіңіз: акция/жарнама."
        ]
        tips_ru = [
            "Повышение цены на 5–10% приблизит точку безубыточности, но учитывайте спрос.",
            "Если снизить себестоимость на 5%, рентабельность заметно вырастет.",
            "При высоких постоянных расходах увеличьте объём продаж: акции/реклама."
        ]
        margin = price - cost
        if margin <= 0:
            tip = tips_kk[1] if lang=='kk' else tips_ru[1]
        elif price > 0 and margin / price < 0.15:
            tip = tips_kk[0] if lang=='kk' else tips_ru[0]
        else:
            tip = tips_kk[2] if lang=='kk' else tips_ru[2]
        st.info(T['ai_tip'].format(tip=tip))

st.markdown('---')
st.caption(T['footer'])
