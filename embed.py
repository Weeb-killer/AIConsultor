from __future__ import annotations
import logging
from typing import Dict, List, Any
from dotenv import load_dotenv, find_dotenv
from langchain.embeddings.base import Embeddings
from langchain.pydantic_v1 import BaseModel, root_validator
from zhipuai import ZhipuAI

logger = logging.getLogger(__name__)
_ = load_dotenv(find_dotenv())


# 在 Python 中，root_validator 是 Pydantic 模块中一个用于自定义数据校验的装饰器函数。root_validator 用于在校验整个数据模型之前对整个数据模型进行自定义校验，以确保所有的数据都符合所期望的数据结构。
class ZhipuAIEmbeddings(BaseModel, Embeddings):
    """`Zhipuai Embeddings` embedding models."""

    client: Any
    """`zhipuai.ZhipuAI"""

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """
        实例化ZhipuAI为values["client"]

        Args:

            values (Dict): 包含配置信息的字典，必须包含 client 的字段.
        Returns:

            values (Dict): 包含配置信息的字典。如果环境中有zhipuai库，则将返回实例化的ZhipuAI类；否则将报错 'ModuleNotFoundError: No module named 'zhipuai''.
        """

        values["client"] = ZhipuAI(api_key="7eb749cd070d0137878a3bc9527ef662.Hmmcy4TFyhws3xLv")
        return values

    def embed_query(self, text: str) -> List[float]:
        """
        生成输入文本的 embedding.

        Args:
            texts (str): 要生成 embedding 的文本.

        Return:
            embeddings (List[float]): 输入文本的 embedding，一个浮点数值列表.
        """
        embeddings = self.client.embeddings.create(
            model="embedding-2",
            input=text
        )
        return embeddings.data[0].embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        生成输入文本列表的 embedding.
        Args:
            texts (List[str]): 要生成 embedding 的文本列表.

        Returns:
            List[List[float]]: 输入列表中每个文档的 embedding 列表。每个 embedding 都表示为一个浮点值列表。
        """
        return [self.embed_query(text) for text in texts]

