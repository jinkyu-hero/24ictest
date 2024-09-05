import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 제목과 설명
st.title('데이터 시각화 대시보드')
st.write('총점, 국어 점수, 수학 점수, 영어 점수의 히스토그램과 반별 총점 분포를 보여주는 박스플롯입니다.')

# 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # 데이터 불러오기
    try:
        data = pd.read_csv(uploaded_file, encoding='cp949')  # 필요한 경우 encoding을 변경하세요.
    except UnicodeDecodeError:
        data = pd.read_csv(uploaded_file, encoding='utf-8')  # 다른 인코딩 시도

    # 히스토그램 그리기
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    axs[0, 0].hist(data['총점'], bins=20, color='skyblue', edgecolor='black')
    axs[0, 0].set_title('총점')

    axs[0, 1].hist(data['국어'], bins=20, color='lightgreen', edgecolor='black')
    axs[0, 1].set_title('국어 점수')

    axs[1, 0].hist(data['수학'], bins=20, color='lightcoral', edgecolor='black')
    axs[1, 0].set_title('수학 점수')

    axs[1, 1].hist(data['영어'], bins=20, color='gold', edgecolor='black')
    axs[1, 1].set_title('영어 점수')

    st.pyplot(fig)

    # 박스플롯 그리기
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    data.boxplot(column='총점', by='반', ax=ax2)
    plt.title('반별 총점 분포')
    plt.suptitle('')  # 기본제목 제거
    plt.xlabel('반')
    plt.ylabel('총점')

    st.pyplot(fig2)

    # 국어 점수 기준 상위 10명 출력
    st.subheader('국어 점수 기준 상위 10명')
    top_korean = data.sort_values(by='국어', ascending=False).head(10)
    st.write(top_korean[['이름', '국어']])

    # 수학 점수 기준 상위 10명 출력
    st.subheader('수학 점수 기준 상위 10명')
    top_math = data.sort_values(by='수학', ascending=False).head(10)
    st.write(top_math[['이름', '수학']])

    # 영어 점수 기준 상위 10명 출력
    st.subheader('영어 점수 기준 상위 10명')
    top_english = data.sort_values(by='영어', ascending=False).head(10)
    st.write(top_english[['이름', '영어']])
else:
    st.write("CSV 파일을 업로드하세요.")
