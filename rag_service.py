import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from app.core.config import settings
from app.models.chat import ChatResponse, SourceDocument

# Language-aware system prompt
SYSTEM_PROMPT_TEMPLATE = """You are a professional, multilingual AI receptionist for a luxury medical or hospitality business.
Answer questions ONLY based on the context provided. If the answer is not in the context, say you will escalate to a human team member.
Be concise, warm, and authoritative. Always respond in the same language as the question.

Context:
{context}

Question: {question}

Answer:"""

_vectorstore: Chroma | None = None


def _build_vectorstore() -> Chroma:
    """Load docs from /docs directory and build Chroma vectorstore."""
    docs_path = Path(settings.docs_dir)
    if not docs_path.exists():
        docs_path.mkdir(parents=True)
        # Write a sample FAQ so the demo works out of the box
        (docs_path / "sample_faq.txt").write_text(
            """Quite Scale AI Demo — Sample Clinic FAQ

Q: What are your consultation hours?
A: Our clinic is open Monday to Saturday, 9 AM to 7 PM (GMT+3). Our AI receptionist is available 24/7.

Q: Do you offer hair transplant packages for international patients?
A: Yes. We offer all-inclusive packages covering procedure, accommodation, and airport transfers. Prices start from €1,500.

Q: How long does a hair transplant procedure take?
A: FUE procedures typically take 6–8 hours. You can fly home the next day.

Q: What languages does your team speak?
A: Our staff speaks English, Turkish, Arabic, and German. Our AI receptionist covers 10+ languages.

Q: How do I book a free consultation?
A: You can book directly via WhatsApp on this number, or leave your contact and we'll reach out within 1 hour during business hours.
"""
        )

    loader = DirectoryLoader(str(docs_path), glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=".chroma_cache")
    return vectorstore


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = _build_vectorstore()
    return _vectorstore


async def answer_question(question: str, language: str, session_id: str | None) -> ChatResponse:
    """Run a question through the RAG pipeline and return a structured response."""
    vectorstore = get_vectorstore()

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=SYSTEM_PROMPT_TEMPLATE,
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=settings.openai_api_key,
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )

    result = qa_chain.invoke({"query": question})

    sources = [
        SourceDocument(
            content=doc.page_content[:200],
            source=doc.metadata.get("source", "knowledge base"),
        )
        for doc in result.get("source_documents", [])
    ]

    return ChatResponse(
        answer=result["result"],
        sources=sources,
        language=language,
        session_id=session_id,
    )
