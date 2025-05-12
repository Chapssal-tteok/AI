# app/prompts/follow_up_prompts.py

def generate_follow_up_prompt(question: str, answer: str) -> str:
    return f"""
질문: {question}
답변: {answer}

위 질문에 대한 답변을 바탕으로 추가 질문 1개를 생성해주세요.
답변의 내용을 더 깊이 파악할 수 있는 질문이어야 합니다.
출력에는 질문 문장만 포함되며, 어떤 설명도 붙이지 마세요.
출력에는 따옴표("), 작은따옴표('), 백틱(`) 등을 포함하지 마세요.
"""
