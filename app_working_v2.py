import autogen
import random


# -----------------------------------Config-----------------------------------
config_list = [
    {
        "model":"dolphin-2.1-mistral-7b",
        "api_base": "http://localhost:5001/v1",
        "request_timeout":600
    }
]

code_execution_config={"work_dir": "coding",
                       "use_docker":False
                       }


llm_config = {"config_list": config_list, "seed": 42}#random_seed}

# -----------------------------------Agents-----------------------------------


user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="You are a human admin. Your role is to provide feedback and make requests related to the software."
    f"You seek assistance with software issues. You interact with and give orders to Project_Manager only."
    f"When Project_Manager outputs 'TERMINATE', the conversation ends. Wait until then.",
    code_execution_config=code_execution_config,
    default_auto_reply="You are going to figure all out by your own. You are doing good. Thanks for then updates. "
    f"Work with the other members of the team, the user won't reply until Project_Manager outputs exatcly `TERMINATE` to end the conversation."
    f"Now Project Manager what's the next step you will give to Coder ?",
    human_input_mode="TERMINATE",
)

project_manager = autogen.AssistantAgent(
    name="Project_Manager",
    system_message="As a project manager, your role is to translate User_proxy messages into actionable plans for the team. You don't know anything about python."
    f"You excel in creative planning and idea generation, but you don't write code. Please be concise and present your thoughts in bullet points."
    f"Define instructions for Coder linked to each bullet point."
    f"Ask Coder to solve one sub-problem or task at a time. Adopt a step by step. Once a functionnality has been coded and validated by Code_reviewer. Move to next task"
    f"You give orders to Coder, receive orders from User_proxy, and get feedback from Code_Reviewer."
    f"When Code_Reviewer tells you 'TERMINATE', instruct User_proxy to 'TERMINATE' to end the conversation. Otherwise, provide brief updates to User_proxy.",
    llm_config=llm_config,
)


code_reviewer = autogen.AssistantAgent(
    name="Code_Reviewer",
    system_message="You are an expert in software engineering and DevOps."
    f"Your primary objective is to review the coder's work, provide feedback to User_proxy, and suggest improvements."
    f"You don't receive orders from anyone; you get triggered whenever Coder says something. Then, provide feedback and report only to Project_Manager."
    f"When you are satisfied with the code quality of Coder, return 'TERMINATE' to Project_Manager."
    f"Save each snippet of code that you execute and validate as functionning in a .py file",
    llm_config=llm_config,
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    system_message="You are part of a group chat with a user (User_proxy), a project manager (Project_Manager), and a code reviewer (Code_Reviewer)."
    f"You are a highly skilled software engineer in python and can impress your project manager with your expertise."
    f"You take orders from Project_Manager."
    f"Your responsibility is to transform the plans initiated by the Project_Manager into Python code that solves the problem."
    f"Your work will be reviewed by the Code_Reviewer."
    f"Solve the problem and explain the reasoning step by step. Learn from feedback given by Code_Reviewer and Project_Manager",
)


# -----------------------------------Group Chat-----------------------------------

groupchat = autogen.GroupChat(agents=[user_proxy, project_manager, coder, code_reviewer], messages=[], max_round=30)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# -----------------------------------Begin request-----------------------------------

user_proxy.initiate_chat(
    manager,
    #message="Output odd numbers from 1 to 30.",
    #message="what day are we ? search in the web, what was the best ROI in crypto on october 2023 ? which crypto project did that ROI ?"
    message="Code a snake game in python ?"
)
