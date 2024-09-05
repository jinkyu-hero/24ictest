# 제목과 설명
st.title('모의고사/학력평가 원점수 데이터 시각화 대시보드  by  Aichem')
st.write('업로드된 데이터로 반별 점수 분포와 상위 10명 학생 정보를 시각화합니다.univ 회사의 리딩 결과 파일 csv를 사용합니다.')

import streamlit as st
import pandas as pd
import altair as alt

# 파일 업로드 위젯
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # 데이터 불러오기
    try:
        data = pd.read_csv(uploaded_file, encoding='cp949')  # 필요한 경우 encoding을 변경하세요.
    except UnicodeDecodeError:
        data = pd.read_csv(uploaded_file, encoding='utf-8')  # 다른 인코딩 시도

    # 11열과 12열의 데이터 분리
    data[['탐구1_점수', '탐구1_과목']] = data['탐구1'].str.split('/', expand=True)
    data[['탐구2_점수', '탐구2_과목']] = data['탐구2'].str.split('/', expand=True)

    # 점수 열을 숫자형으로 변환
    data['탐구1_점수'] = pd.to_numeric(data['탐구1_점수'], errors='coerce')
    data['탐구2_점수'] = pd.to_numeric(data['탐구2_점수'], errors='coerce')

    # 과목별 점수 데이터프레임 생성
    subject_scores = pd.concat([
        data[['탐구1_과목', '탐구1_점수']].rename(columns={'탐구1_과목': '과목', '탐구1_점수': '점수'}),
        data[['탐구2_과목', '탐구2_점수']].rename(columns={'탐구2_과목': '과목', '탐구2_점수': '점수'})
    ])

    # 반별 총점 박스 플롯
    st.subheader('반별 총점 박스 플롯')
    box_plot = alt.Chart(data).mark_boxplot(size=40).encode(
        x='반:O',
        y='총점:Q',
        color='반:N',
        tooltip=['반', '총점']
    ).interactive()
    st.altair_chart(box_plot, use_container_width=True)

     # 국어, 수학, 영어 점수 산점도 추가
    st.subheader('국어, 수학, 영어 점수 산점도')

    korean_score_scatter = alt.Chart(data).mark_point().encode(
        x='반:O',
        y='국어:Q',
        color='반:N',
        tooltip=['반', '국어']
    ).interactive()
    st.altair_chart(korean_score_scatter, use_container_width=True)

    math_score_scatter = alt.Chart(data).mark_point().encode(
        x='반:O',
        y='수학:Q',
        color='반:N',
        tooltip=['반', '수학']
    ).interactive()
    st.altair_chart(math_score_scatter, use_container_width=True)

    english_score_scatter = alt.Chart(data).mark_point().encode(
        x='반:O',
        y='영어:Q',
        color='반:N',
        tooltip=['반', '영어']
    ).interactive()
    st.altair_chart(english_score_scatter, use_container_width=True)

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

    # 반 선택 드롭다운 메뉴 생성
    selected_class = st.selectbox('반을 선택하세요', sorted(data['반'].unique()))

    # 선택된 반의 데이터 필터링
    filtered_data = data[data['반'] == selected_class]

    # 선택된 반의 점수 시각화 (2x2 레이아웃)
    st.subheader(f'{selected_class} 반의 점수 분포')

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('총점 박스 플롯')
        st.altair_chart(alt.Chart(filtered_data).mark_boxplot().encode(
            x='반:O',
            y='총점:Q',
            color='반:N'
        ).interactive(), use_container_width=True)

    with col2:
        st.subheader('국어 점수 박스 플롯')
        st.altair_chart(alt.Chart(filtered_data).mark_boxplot().encode(
            x='반:O',
            y='국어:Q',
            color='반:N'
        ).interactive(), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader('수학 점수 박스 플롯')
        st.altair_chart(alt.Chart(filtered_data).mark_boxplot().encode(
            x='반:O',
            y='수학:Q',
            color='반:N'
        ).interactive(), use_container_width=True)

    with col4:
        st.subheader('영어 점수 박스 플롯')
        st.altair_chart(alt.Chart(filtered_data).mark_boxplot().encode(
            x='반:O',
            y='영어:Q',
            color='반:N'
        ).interactive(), use_container_width=True)

       # 탐구 과목별 점수 시각화
    st.subheader('탐구 과목별 점수 분포')
    subject_chart = alt.Chart(subject_scores).mark_boxplot().encode(
        x='과목:O',
        y='점수:Q',
        color='과목:N',
        tooltip=['과목', '점수']
    ).interactive()
    st.altair_chart(subject_chart, use_container_width=True)

else:
    st.write("CSV 파일을 업로드하세요.")

