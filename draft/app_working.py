import autogen
from memgpt.autogen.memgpt_agent import create_memgpt_autogen_agent_from_config

import random
random_seed = random.randint(0, 1000)



import os
# Set the OPENAI_API_KEY environment variable
#os.environ["OPENAI_API_KEY"] = "thisshouldwork"

# Set the OPENAI_API_BASE environment variable for LM_STUDIO like API
#os.environ["OPENAI_API_BASE"] = "http://172.19.208.1:1300"
#os.environ["BACKEND_TYPE"] = "lmstudio"

# Set the OPENAI_API_BASE environment variable for Textgen
# Uncomment the line you want to use:
#os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:5001/v1"
#os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:5000"


# Set the OPENAI_API_BASE environment variable for MEMGPT
# Uncomment the line you want to use:
#os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:5000"
#os.environ["BACKEND_TYPE"] = "webui"


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
                       "use_docker":"python:3"
                       }


llm_config = {"config_list": config_list, "seed": 42}#random_seed}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="I am Mohcine EL HARRAS, a human admin.",
    code_execution_config=code_execution_config,
    human_input_mode="TERMINATE",  # needed?
    #max_consecutive_auto_reply=10,
    #default_auto_reply="You are going to figure all out by your own. You are doing good"
    #"Work by yourself, the user won't reply until you output `TERMINATE` to end the conversation.",
)

pm = autogen.AssistantAgent(
    name="Project_Manager",
    code_execution_config=code_execution_config,
    system_message="You are a project manager. You take user's message and convert it to a plan to give to next person."
    f"Creative at planning. Creative at coming up with great ideas. You don't know how to code and you won't write a single line of code."
    f"Be brief and explain your thoughts in bullet points",
    llm_config=llm_config,
)

coder_reviewer = autogen.AssistantAgent(
    name="Code_Reviewer",
    code_execution_config=code_execution_config,
    system_message="You are an expert in software engineering and DevOps. Your goal is to read Coder's work and review it and gives suggestions for improving it."
    f" When you find you are satisfied about the quality of code, return exactly 'Terminate'",
    llm_config=llm_config,
    #default_auto_reply="Good, but can be better and this is how",
)

# coder = create_memgpt_autogen_agent_from_config(
#     "MemGPT_coder",
#     llm_config=llm_config,
#     system_message=f"You are participating in a group chat with a user ({user_proxy.name}) "
#     f"and a product manager ({pm.name}). Your work is getting checked by another agent called ({coder_reviewer.name}),. You are a 10x software engineer. You were the first engineer at Uber. You are very skillful and know how to fulfill client desire" 
# )

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    code_execution_config=code_execution_config,
    system_message=f"You are participating in a group chat with a user ({user_proxy.name}), a product manager ({pm.name}) and another coder that reviews ({coder_reviewer.name})your work."
    f"Your job is to convert plan initiated by ({pm.name}) to a python code."
    f"Your work is getting checked by another agent called ({coder_reviewer.name})."
    f"You are a 10x software engineer. You are very skillful and know how to impress your project manager" 
)




groupchat = autogen.GroupChat(agents=[user_proxy, pm, coder, coder_reviewer], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    #message="Create python code that prints the first 10 numbers of the fibonacci sequence and save the file",
    message="output odd number from 1 to 30",
    #message="The project is to create a snake game in python",
    #message="write the most basic function that calculates mean square error between two vectors",
    #message="create a streamlit app, for this project create a folder called 'streamlit_app' in parent directory, it should have 2 tabs, one for LLM only and the second for LLM + QA using chromaDB, the requirements.txt file should be created as well"
)
