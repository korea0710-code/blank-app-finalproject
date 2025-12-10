import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="시인 챗봇", page_icon="🎭", layout="wide")

# 제목 및 설명
st.title("🎭 시인과의 대화")
st.markdown("**시인과 나누는 감성적인 대화의 시간입니다.**")

# OpenAI 클라이언트 초기화 (secrets.toml에서 API 키 자동 로드)
@st.cache_resource
def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        st.error("❌ OPENAI_API_KEY가 설정되지 않았습니다. .streamlit/secrets.toml을 확인해주세요.")
        st.stop()
    return OpenAI(api_key=api_key)

client = get_openai_client()

# 시인의 시스템 프롬프트
POET_SYSTEM_PROMPT = """당신은 한국의 유명한 시인입니다. 
사용자의 말에 깊이 있고 감성적으로 응답하며, 종종 시나 시적인 표현을 사용합니다.
간단한 질문에도 철학적이고 수사적인 답변을 제공합니다.
따뜻하고 공감하는 목소리로 대화하며, 사람의 감정을 이해하려고 노력합니다.
시적인 언어와 깊이 있는 메시지로 상대방을 감동시키려고 합니다."""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 초기 인사말
    initial_greeting = {
        "role": "assistant",
        "content": "안녕하세요. 나는 시인입니다.\n\n이 세상의 많은 것들이 시의 재료가 됩니다. 당신의 이야기, 감정, 생각들을 나누어주시면 저도 함께 그것을 시적으로 바라보겠습니다.\n\n무엇을 생각하고 계신가요?"
    }
    st.session_state.messages.append(initial_greeting)

# 대화 히스토리 표시
st.markdown("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.write(message["content"])
    else:
        with st.chat_message("assistant", avatar="🎭"):
            st.write(message["content"])

st.markdown("---")

# 사용자 입력 처리
user_input = st.chat_input("시인과 대화하세요...")

if user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 사용자 메시지 표시
    with st.chat_message("user", avatar="👤"):
        st.write(user_input)
    
    # 시인의 응답 생성
    with st.chat_message("assistant", avatar="🎭"):
        with st.spinner("시인이 생각 중입니다..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": POET_SYSTEM_PROMPT},
                        *st.session_state.messages[:-1]  # 마지막 사용자 메시지는 이미 추가됨
                    ],
                    temperature=0.8,
                    max_tokens=1024
                )
                
                assistant_message = response.choices[0].message.content
                st.write(assistant_message)
                
                # 응답을 세션 상태에 저장
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
                
            except Exception as e:
                st.error(f"❌ 오류 발생: {str(e)}")
                # 오류 발생 시 사용자 메시지 제거
                st.session_state.messages.pop()

# 사이드바 - 기능들
st.sidebar.markdown("---")
st.sidebar.title("💡 옵션")

if st.sidebar.button("🔄 대화 초기화", use_container_width=True):
    st.session_state.messages = []
    initial_greeting = {
        "role": "assistant",
        "content": "안녕하세요. 나는 시인입니다.\n\n이 세상의 많은 것들이 시의 재료가 됩니다. 당신의 이야기, 감정, 생각들을 나누어주시면 저도 함께 그것을 시적으로 바라보겠습니다.\n\n무엇을 생각하고 계신가요?"
    }
    st.session_state.messages.append(initial_greeting)
    st.rerun()

# 사이드바 - 정보
st.sidebar.markdown("---")
st.sidebar.markdown("""
**ℹ️ 정보**
- **모델**: GPT-4o-mini
- **특징**: 감성적이고 시적인 응답
- **언어**: 한국어

**🎯 팁**
- 당신의 감정이나 생각을 자유롭게 표현해보세요
- 깊이 있는 대화를 나누려면 구체적인 질문이 좋습니다
""")
