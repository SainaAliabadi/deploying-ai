from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from chat_system.src.config import settings


class SemanticSearchService:

    def __init__(self):
        self.llm = ChatOpenAI(model=settings.MODEL_NAME, temperature=0.2)

        self.vector_store = Chroma(
            persist_directory=settings.CHROMA_DIR,
            collection_name=settings.COLLECTION_NAME,
            embedding_function=OpenAIEmbeddings()
        )

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    def handle(self, user_input: str):

        docs = self.retriever.invoke(user_input)

        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
        Use the context below to answer the question clearly and concisely.

        Context:
        {context}

        Question:
        {user_input}
        """

        response = self.llm.invoke(prompt)

        return response.content
