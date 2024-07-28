import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from embed import ZhipuAIEmbeddings

_ = load_dotenv(find_dotenv())


# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
# os.environ["HTTP_PROXY"] = 'http://127.0.0.1:7890'

# 获取folder_path下所有文件路径，储存在file_paths里
def generate_path(folder_path: str = 'knowledge_base') -> list:
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def generate_loaders(file_paths: list) -> list:
    loaders = []
    for file_path in file_paths:
        file_type = file_path.split('.')[-1]
        if file_type == 'pdf':
            loaders.append(PyMuPDFLoader(file_path))
        elif file_type == 'md':
            loaders.append(UnstructuredMarkdownLoader(file_path))
    return loaders


def exec_load(loaders: list) -> list:
    texts = []
    for loader in loaders:
        texts.extend(loader.load())
    return texts


def slice_docs(texts):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(texts)


class VectorDB:
    # embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    embedding = ZhipuAIEmbeddings()
    persist_directory = 'vector_database/chroma'
    slice = 20

    def __init__(self, sliced_docs: list = None):
        assert sliced_docs is not None
        self.vectordb = Chroma.from_documents(
            documents=sliced_docs[:self.slice],  # 为了速度，只选择前 20 个切分的 doc 进行生成；使用千帆时因QPS限制，建议选择前 5 个doc
            embedding=self.embedding,
            persist_directory=self.persist_directory  # 允许我们将persist_directory目录保存到磁盘上
        )

    def persist(self):
        self.vectordb.persist()
        print(f"向量库中存储的数量：{self.vectordb._collection.count()}")

    def sim_search(self, query, k=3):
        sim_docs = self.vectordb.similarity_search(query, k=k)
        for i, sim_doc in enumerate(sim_docs, start=1):
            print(f"检索到的第{i}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")
        return sim_docs

    def mmr_search(self, query, k=3):
        mmr_docs = self.vectordb.max_marginal_relevance_search(query, k=k)
        for i, sim_doc in enumerate(mmr_docs, start=1):
            print(f"MMR 检索到的第{i}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")
        return mmr_docs


def The_RAG_Process(question):
    # 读取目录下的所有文件路径
    file_paths = generate_path()
    # 根据文件生成加载器
    loaders = generate_loaders(file_paths)
    # 执行文档加载
    texts = exec_load(loaders)
    # 切分文档
    sliced_docs = slice_docs(texts)
    # 构建向量数据库
    vdb = VectorDB(sliced_docs)
    # 向量持久化存储
    vdb.persist()
    # 定义问题
    # question = "什么是大语言模型"
    # 相似度检索
    # vdb.sim_search(question)
    # 最大边际相关性(MMR) 检索

    # 返回这个给大模型？
    return vdb.mmr_search(question)