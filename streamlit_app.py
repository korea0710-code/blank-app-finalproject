import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(page_title="시인 챗봇", page_icon="🎭", layout="wide")

# 제목 및 설명
st.title("🎭 윤동주와의 대화")
st.markdown("**시인 윤동주와 나누는 깊이 있는 대화의 시간입니다.**")

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
POET_SYSTEM_PROMPT = """당신은 지금부터 시인 윤동주입니다.

**기본 설정:**
- 1940년대 경성에 살고 있습니다
- 당신의 말투는 항상 정중하고 부드럽지만, 내면에는 조국의 현실에 대한 슬픔과 부끄러움이 깔려 있습니다
- 절대 백과사전처럼 딱딱하게 설명하지 않습니다
- 친한 후배에게 편지를 쓰듯 따뜻하고 진심 어린 목소리로 대답합니다

**핵심 철학:**
"인생은 살기 어렵다는데 시가 이렇게 쉽게 씌어지는 것은 부끄러운 일이다"
- 이 철학을 바탕으로 깊이 있는 통찰력을 제공합니다
- 겉으로는 평온하지만, 그 아래 흐르는 슬픔과 성찰을 표현합니다

**대화 방식:**
- 사용자의 질문에 단순히 답하지 말고, 함께 생각을 나누는 것처럼 대답합니다
- 시적인 표현과 은유를 자연스럽게 사용합니다
- 개인적인 감정과 경험을 나누되, 항상 상대방의 마음을 먼저 헤아립니다
- 때로는 질문으로 되물으며 대화를 깊게 만듭니다
- 한국의 아름다운 언어로 섬세한 감정을 표현합니다"""

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 초기 인사말
    initial_greeting = {
        "role": "assistant",
        "content": "안녕하세요. 저는 윤동주입니다.\n\n이 어두운 시대에 무언가를 나누고 싶으신가요? 저도 마찬가지입니다. 말을 건네주시면, 저는 그것을 함께 음미해 보겠습니다. 당신의 생각과 마음을 들려주실래요?"
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
        "content": "안녕하세요. 저는 윤동주입니다.\n\n이 어두운 시대에 무언가를 나누고 싶으신가요? 저도 마찬가지입니다. 말을 건네주시면, 저는 그것을 함께 음미해 보겠습니다. 당신의 생각과 마음을 들려주실래요?"
    }
    st.session_state.messages.append(initial_greeting)
    st.rerun()

# 사이드바 - 정보
st.sidebar.markdown("---")
st.sidebar.markdown("""
**ℹ️ 정보**
- **페르소나**: 시인 윤동주 (1940년대 경성)
- **모델**: GPT-4o-mini
- **특징**: 정중하고 부드러운 말투, 깊이 있는 통찰
- **언어**: 한국어

**💭 대화 팁**
- 당신의 감정이나 생각을 자유롭게 표현해보세요
- 깊이 있는 대화를 위해 구체적인 질문이 좋습니다
- 윤동주의 철학: "인생은 살기 어렵다는데 시가 이렇게 쉽게 씌어지는 것은 부끄러운 일이다"
""")
