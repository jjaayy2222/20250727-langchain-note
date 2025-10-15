"""
myrag.py
========================================
RAG (Retrieval-Augmented Generation) 시스템 구현
- PDF 문서 로드 및 처리
- HuggingFace 임베딩 지원
- FAISS 벡터스토어
- Gemini LLM 지원
========================================
"""

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings


class PDFRAG:
    """
    PDF 기반 RAG 시스템
    
    Parameters
    ----------
    pdf_path : str
        PDF 파일 경로
    llm : 
        LLM 모델 (ChatOpenAI, ChatGoogleGenerativeAI 등)
    embedding_model_name : str, optional
        HuggingFace 임베딩 모델 이름
        기본값: "all-MiniLM-L6-v2"
        대안: "BAAI/bge-small-en-v1.5"
    """
    
    def __init__(
        self,
        pdf_path: str,
        llm,
        embedding_model_name: str = "all-MiniLM-L6-v2",
    ):
        self.pdf_path = pdf_path
        self.llm = llm
        self.embedding_model_name = embedding_model_name
        self.docs = None
        self.split_documents = None
        self.vectorstore = None
        self.retriever = None
        self.chain = None
        
        # 문서 로드
        self._load_documents()
        
        # 문서 분할
        self._split_documents()
        
        # 임베딩 생성
        self._create_embeddings()
        
        # 벡터스토어 생성
        self._create_vectorstore()
    
    def _load_documents(self):
        """PDF 문서 로드"""
        loader = PyMuPDFLoader(self.pdf_path)
        self.docs = loader.load()
        print(f"✅ 문서 로드 완료: {len(self.docs)}개 페이지")
    
    def _split_documents(self):
        """문서 분할"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50
        )
        self.split_documents = text_splitter.split_documents(self.docs)
        print(f"✅ 문서 분할 완료: {len(self.split_documents)}개 청크")
    
    def _create_embeddings(self):
        """HuggingFace 임베딩 생성"""
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model_name,
            model_kwargs={'device': 'cpu'},  # M1/M2는 'cpu' 사용
            encode_kwargs={'normalize_embeddings': True}
        )
        print(f"✅ 임베딩 모델 로드: {self.embedding_model_name}")
    
    def _create_vectorstore(self):
        """FAISS 벡터스토어 생성"""
        self.vectorstore = FAISS.from_documents(
            documents=self.split_documents,
            embedding=self.embeddings
        )
        print(f"✅ 벡터스토어 생성 완료")
    
    def create_retriever(self, k: int = 4):
        """
        검색기 생성
        
        Parameters
        ----------
        k : int, optional
            검색할 문서 개수 (기본값: 4)
        
        Returns
        -------
        retriever
            문서 검색기
        """
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        print(f"✅ 검색기 생성 완료 (k={k})")
        return self.retriever
    
    def create_chain(self, retriever=None):
        """
        RAG 체인 생성
        
        Parameters
        ----------
        retriever : optional
            문서 검색기 (기본값: self.retriever)
        
        Returns
        -------
        chain
            RAG 체인
        """
        if retriever is None:
            if self.retriever is None:
                self.create_retriever()
            retriever = self.retriever
        
        # 프롬프트 템플릿
        prompt = PromptTemplate.from_template(
            """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.

#Context:
{context}

#Question:
{question}

#Answer:"""
        )
        
        # 체인 생성
        self.chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        print(f"✅ RAG 체인 생성 완료")
        return self.chain
    
    def ask(self, question: str):
        """
        질문에 답변
        
        Parameters
        ----------
        question : str
            사용자 질문
        
        Returns
        -------
        str
            답변
        """
        if self.chain is None:
            self.create_chain()
        return self.chain.invoke(question)