# myrag5.py

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings


class PDFRAG:
    def __init__(self, pdf_path, llm, chunk_size=300, chunk_overlap=50):
        """
        PDF RAG 시스템 초기화
        
        Parameters
        ----------
        pdf_path : str
            PDF 파일 경로
        llm : ChatOpenAI
            사용할 LLM
        chunk_size : int
            청크 크기 (기본값: 300)
        chunk_overlap : int
            청크 오버랩 (기본값: 50)
        """
        self.pdf_path = pdf_path
        self.llm = llm
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.documents = None
        self.vectorstore = None
        self.retriever = None
        
        # 초기화
        self._load_and_process()
    
    def _load_and_process(self):
        """PDF 로드 및 처리"""
        # 1. PDF 로드
        loader = PyMuPDFLoader(self.pdf_path)
        docs = loader.load()
        print(f"✅ PDF 로드 완료: {len(docs)} 페이지")
        
        # 2. 청크 분할
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        self.documents = text_splitter.split_documents(docs)
        print(f"✅ 청크 분할 완료: {len(self.documents)} 청크 (크기={self.chunk_size}, 오버랩={self.chunk_overlap})")
        
        # 3. 임베딩
        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        print(f"✅ 임베딩 모델 로드 완료: {embeddings.model_name}")
        
        # 4. 벡터스토어 생성
        self.vectorstore = FAISS.from_documents(
            documents=self.documents,
            embedding=embeddings
        )
        print(f"✅ 벡터스토어 생성 완료: FAISS")
    
    def create_retriever(self, k=10, search_type="similarity"):
        """
        검색기 생성
        
        Parameters
        ----------
        k : int, optional
            검색할 문서 개수 (기본값: 7)
        search_type : str, optional
            검색 타입 (기본값: similarity)
        
        Returns
        -------
        retriever
            문서 검색기
        """
        self.retriever = self.vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )
        print(f"✅ 검색기 생성 완료 (k={k}, search_type={search_type})")
        return self.retriever
    
    def create_chain(self, retriever):
        """
        RAG 체인 생성
        
        Parameters
        ----------
        retriever
            문서 검색기
        
        Returns
        -------
        chain
            RAG 체인
        """
        # 프롬프트 템플릿
        prompt = PromptTemplate.from_template(
            """당신은 질문에 답변하는 AI 어시스턴트입니다.

        주어진 Context를 **반드시** 참고하여 정확하게 답변하세요.
        Context에 정보가 없으면 "죄송합니다. 제공된 문서에서 해당 정보를 찾을 수 없습니다."라고 답변하세요.

        Context:
        {context}

        Question: {question}

        Answer:"""
        )
        
        # 체인 생성
        chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        print(f"✅ RAG 체인 생성 완료")
        return chain

# ========================================
# Question-Answer Evaluator 추가
# ========================================
    
    def create_chain_with_context(self, retriever):
        """
        Context를 포함하여 반환하는 체인 생성
        
        Returns
        -------
        chain
            Context와 Answer를 함께 반환하는 체인
        """
        from langchain_core.runnables import RunnablePassthrough
        
        # Context 추출 함수
        def format_docs(docs):
            return "\n\n".join([doc.page_content for doc in docs])
        
        # 프롬프트는 기존과 동일
        prompt = PromptTemplate.from_template(
            """당신은 질문에 답변하는 AI 어시스턴트입니다.

        주어진 Context를 **반드시** 참고하여 정확하게 답변하세요.
        Context에 정보가 없으면 "죄송합니다. 제공된 문서에서 해당 정보를 찾을 수 없습니다."라고 답변하세요.

        Context:
        {context}

        Question: {question}

        Answer:"""
        )
        
        # Context와 Answer를 함께 반환하는 체인
        chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | RunnablePassthrough.assign(
                answer=prompt | self.llm | StrOutputParser()
            )
        )
        
        print(f"✅ Context 포함 RAG 체인 생성 완료")
        return chain
