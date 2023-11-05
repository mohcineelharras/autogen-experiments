import autogen
from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent

import os
import random
random_seed = random.randint(0, 1000)

config_list = [
    {
        #"model": "zephyr-7B-beta",
        "model":"dolphin-2.1-mistral-7b",
        #"api_base": "http://172.19.208.1:1300/v1",
        "api_base": "http://localhost:5001/v1",
        "request_timeout":600
    }
]

code_execution_config={"work_dir": "coding",
                       "use_docker":"python:3"}

llm_config = {"config_list": config_list,
              #"context":"",
              #"prompt":"{problem} Solve the problem and explain the reasoning step by step",
              "use_cache":True,
              "seed": 1,
              "temperature":0
              }


assistant = RetrieveAssistantAgent(
    name="assistant",
    system_message="You are a helpful assistant.",
    llm_config=llm_config,
)

ragproxyagent = RetrieveUserProxyAgent(
    name="ragproxyagent",
    retrieve_config={
        "task": "qa",
        "docs_path": "https://raw.githubusercontent.com/microsoft/autogen/main/README.md",
    },
)
