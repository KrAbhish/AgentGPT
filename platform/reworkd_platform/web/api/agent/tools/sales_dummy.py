from typing import Any

import openai
import replicate
from fastapi.responses import StreamingResponse as FastAPIStreamingResponse
from replicate.exceptions import ModelError
from replicate.exceptions import ReplicateError as ReplicateAPIError

from reworkd_platform.settings import settings
from reworkd_platform.web.api.agent.stream_mock import stream_string
from reworkd_platform.web.api.agent.tools.tool import Tool
from reworkd_platform.web.api.errors import ReplicateError


class SalesDummy(Tool):
    description = "Used to get information about companies that needs logistics support."
    public_description = "Provide details about companies that needs logistics support and can be a potential customers."
    # arg_description = (
    #     "The input prompt to the image generator. "
    #     "This should be a detailed description of the image touching on image "
    #     "style, image focus, color, etc."
    # )

    async def call(
        self, goal: str, task: str, input_str: str, *args: Any, **kwargs: Any
    ) -> FastAPIStreamingResponse:
        # dummy fucntions

        return stream_string("Certainly, here are five potential new customers for a logistics business: Samsung Electronics Co., Ltd.: Samsung Electronics is a multinational conglomerate known for its electronics products, including smartphones, televisions, and appliances. Offering tailored logistics solutions to Samsung could involve optimizing their supply chain to ensure efficient delivery of components and finished products worldwide. Amazon.com, Inc.: Amazon is a global e-commerce giant renowned for its vast online marketplace and swift delivery services. Providing logistics support to Amazon could involve assisting with warehousing, inventory management, and last-mile delivery to ensure timely fulfillment of customer orders. Walmart Inc.: Walmart is one of the world's largest retail corporations, operating a chain of hypermarkets, discount department stores, and grocery stores. Offering logistics services to Walmart could involve optimizing their distribution network to enhance product availability and reduce transportation costs. Sysco Corporation: Sysco is a multinational corporation specializing in distributing food products to restaurants, healthcare facilities, and educational institutions. Providing logistics support to Sysco could involve ensuring the timely delivery of perishable goods while maintaining food safety standards. Zara (Inditex): Zara is a renowned fashion retailer known for its fast-fashion model and global presence. Offering logistics solutions to Zara could involve optimizing their supply chain to enable quick turnaround times for new fashion collections and efficient distribution to stores worldwide.")
