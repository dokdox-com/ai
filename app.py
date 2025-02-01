import cohere
import streamlit as st
import requests

# Streamlit secrets에서 API 키 가져오기
cohere_api_key = st.secrets["key"]
weather_api_key = st.secrets["wkey"]  # OpenWeatherMap API 키

# Cohere 클라이언트 초기화
co = cohere.ClientV2(cohere_api_key)

# Streamlit 경고 메시지
st.warning("이 페이지는 개발 중입니다. 오류가 발생할 수 있습니다.")

# 사용자 위치 입력받기
location = st.text_input("도시 이름을 입력하세요.", "Seoul")

# 날씨 정보 가져오기
def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&units=metric&lang=kr"
    response = requests.get(url)
    data = response.json()
    if data["cod"] != 200:
        return None
    return data

weather_data = get_weather_data(location)

if weather_data:
    # 날씨 데이터 파싱
    temperature = weather_data["main"]["temp"]
    weather_condition = weather_data["weather"][0]["description"]
    weather_icon = weather_data["weather"][0]["icon"]
    st.image(f"http://openweathermap.org/img/wn/{weather_icon}@2x.png", width=150)

    st.write(f"{location}의 현재 날씨: {weather_condition} / 기온: {temperature}°C")

    # 활동 추천을 위한 AI 모델 호출
    activity_prompt = f"현재 날씨는 {weather_condition}이고 기온은 {temperature}°C 입니다. 이 날씨에 맞는 추천 활동을 제시해주세요."

    response = co.chat(
        model="command-r7b-12-2024",
        response=activity_prompt,
        max_tokens=100,
        temperature=0.7
    )

    recommended_activity = response.generations[0].text.strip()
    st.write(f"추천 활동: {response}")

else:
    st.write(f"{location}의 날씨 정보를 불러오는 데 실패했습니다. 도시 이름을 다시 입력해보세요.")
