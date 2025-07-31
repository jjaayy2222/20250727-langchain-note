# 2. 프롬프트(Prompt)

## 프롬프트 단계 개요  
- 검색기에서 찾아낸 여러 문서(컨텍스트)를 바탕으로  
- 언어 모델이 최종 답변을 생성하기 위해 사용하는 **질문이나 명령문을 만드는 과정**  
- RAG 시스템에서 매우 중요한 단계임

## 프롬프트의 필요성  
1. **문맥(Context) 설정**  
   - 모델이 특정 상황·정보를 이해하고 활용하도록 도움  
   - 제공된 문서를 효과적으로 반영하여 답변의 정확성과 연관성 향상  

2. **정보 통합**  
   - 검색된 여러 문서의 서로 다른 내용이나 관점을 합쳐 일관된 형식으로 정리  
   - 모델이 혼란 없이 여러 정보를 같이 활용할 수 있게 함  

3. **응답 품질 향상**  
   - 프롬프트가 잘 구성될수록 모델이 더 정확하고 유용한 답변 생성  
   - 덜 구조화되거나 모호한 프롬프트는 부정확하거나 엉뚱한 응답 가능성 증가

## RAG 프롬프트 기본 구조  
```
지시사항(Instruction)

질문(사용자 입력 질문)

문맥(검색된 정보)

예시)  
   당신은 질문-답변 AI 어시스턴트입니다.  
   검색된 문맥(context)를 활용하여 질문(question)에 답하세요.  
   문맥에 답이 없으면 '모른다'고 답해주세요. 한국어로 대답하세요.

# Question: {사용자 질문}  
# Context: {검색된 정보}
```

## 프롬프트 중요성 요약  
- RAG에서 프롬프트는 LLM이 최적의 성능을 내도록 하는 핵심 데이터 인터페이스  
- 잘 짜인 프롬프트가 없으면, LLM이 검색된 정보를 제대로 이해·활용 못해 부정확한 답변 생성  
- 결과적으로 사용자 만족도와 시스템 신뢰도에 큰 영향  
- 따라서 프롬프트 설계에 신중을 기하고 반복 개선이 필요

---

* 출처 

    * [1] [RAG 구현시 고려사항 : (4) 프롬프트 설계 및 Generator 고려사항](https://datacookbook.kr/113)
    * [2] [[LLM][RAG] RAG(Retrieval-Augmented Generation) 소개 및 설명](https://dwin.tistory.com/172)
    * [3] [프롬프트 최적화를 위한 RAG(Retrieval-Augmented Generation) 구조 ...](https://everyday-lucky-world.com/entry/%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8-%EC%B5%9C%EC%A0%81%ED%99%94%EB%A5%BC-%EC%9C%84%ED%95%9C-RAGRetrieval-Augmented-Generation-%EA%B5%AC%EC%A1%B0-%EC%9D%B4%ED%95%B4%EC%99%80-%EC%A0%81%EC%9A%A9)
    * [4] [RAG란? - 검색 증강 생성 AI 설명 - AWS](https://aws.amazon.com/ko/what-is/retrieval-augmented-generation/)
    * [5] [Agentic RAG : prompt - velog](https://velog.io/@looa0807/Agentic-RAG)
    * [6] [LangChain RAG 파헤치기: 문서 기반 QA 시스템 설계 방법 - 심화편](https://teddylee777.github.io/langchain/rag-tutorial/)
    * [7] [Retrieval Augmented Generation (RAG) for LLMs](https://www.promptingguide.ai/kr/research/rag)
    * [8] [RAG와 프롬프트 엔지니어링의 시너지: 지식 기반 AI 구축하기](https://www.intellieffect.com/blog/rag%EC%99%80-%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8-%EC%97%94%EC%A7%80%EB%8B%88%EC%96%B4%EB%A7%81%EC%9D%98-%EC%8B%9C%EB%84%88%EC%A7%80-%EC%A7%80%EC%8B%9D-%EA%B8%B0%EB%B0%98-ai-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0)
    * [9] [ChatGPT RAG 시스템 완벽 공략: 프롬프트 엔지니어링 핵심 비법!](https://www.youtube.com/shorts/NzrIaK1UqI4)
    * [10] [Prompt Engineering vs RAG : 스마트 코드 제안의 핵심 - SLEXN](https://www.slexn.com/prompt-engineering-vs-rag-%EC%8A%A4%EB%A7%88%ED%8A%B8-%EC%BD%94%EB%93%9C-%EC%A0%9C%EC%95%88%EC%9D%98-%ED%95%B5%EC%8B%AC/)