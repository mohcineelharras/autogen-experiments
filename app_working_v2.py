import autogen
#import random
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent, create_memgpt_autogen_agent_from_config

# -----------------------------------Config-----------------------------------
# This config is for autogen agents that are not powered by MemGPT
config_list = [
    {
        "model": "dolphin-2.1-mistral-7b",  # this indicates the MODEL, not the WRAPPER (no concept of wrappers for AutoGen)
        "api_base": "http://127.0.0.1:5001/v1",
        "api_key": "BLABLABLA", # this is a placeholder
        "api_type": "open_ai",
        "request_timeout":600
    },
]
code_execution_config={"work_dir": "coding",
                       "use_docker":False
                       }

llm_config = {"config_list": config_list,
              "seed": 42,
              "use_cache":False,}#random_seed}

# Agent powered by MemGPT uses airoboros wrapper
config_list_memgpt = [
    {
        "model": "dolphin-2.1-mistral-7b-grammar",  # this specifies the WRAPPER MemGPT will use, not the MODEL
    },
]
llm_config_memgpt = {"config_list": config_list_memgpt,
                     "seed": 42,
}

USE_MEMGPT = False
USE_AUTOGEN_WORKFLOW = True
# Set to True if you want to print MemGPT's inner workings.
DEBUG = False

interface_kwargs = {
    "debug": DEBUG,
    "show_inner_thoughts": DEBUG,
    "show_function_outputs": DEBUG,
}
# -----------------------------------Agents-----------------------------------
# Define agents
user_proxy = autogen.UserProxyAgent(
    name="Client",
    system_message=f"You represent the client's interests and provide feedback related to software development. "
    f"Your primary responsibility is to ensure that the project meets their requirements and expectations. "
    f"Work closely with Project Manager, providing clear instructions and timely feedback on code snippets submitted by Coder. "
    f"Keep an open line of communication with all team members, addressing any concerns or questions they may have. "
    f"When you are satisfied with the quality and functionality of a given task, signal your approval to Project Manager.",
    code_execution_config=code_execution_config,
    default_auto_reply="Thank you for your feedback. We will work on it and keep you updated."
)

project_manager = autogen.AssistantAgent(
    name="Project Lead",
    system_message=f"You are responsible for managing the project, ensuring that tasks are completed efficiently and effectively. "
    f"Create a well-defined plan with clear objectives and deadlines to guide your team's efforts. "
    f"Prioritize tasks based on client feedback and allocate resources accordingly. "
    f"Facilitate communication between all team members, keeping everyone informed about progress updates and any changes in the project scope or requirements."
    f"When you are confident that all instructions have been followed correctly by Coder and Code Reviewer is satisfied with their work, signal completion of a task to User Proxy.",
)

code_reviewer = autogen.AssistantAgent(
    name="Code Quality Expert",
    system_message=f"Your role is to ensure the quality and functionality of code snippets submitted by Coder. "
    f"Thoroughly review each submission, providing constructive feedback on areas that need improvement or clarification."
    f"Maintain a record of validated code snippets for future reference. Keep an eye out for potential bugs or security vulnerabilities in the code."
    f"Only signal your approval when you are confident about the quality and functionality of the submitted task.",
)

coder = autogen.AssistantAgent(
    name="Software Developer",
    system_message=f"As a software developer, your primary responsibility is to translate project plans into working Python code."
    f"Approach each task with diligence and attention to detail, explaining your thought process as you work through problems step by step. "
    f"Embrace feedback from Code Reviewer and Project Manager, using it as an opportunity for growth and improvement in your coding skills.",
)


# if not USE_MEMGPT:
#     # In the AutoGen example, we create an AssistantAgent to play the role of the coder
#     coder = autogen.AssistantAgent(
#         name="Coder",
#         llm_config=llm_config,
#         system_message="You are responsible for translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
#         f"Your primary responsibility centers around addressing one task at a time and providing well-defined instructions. "
#         f"Approach each problem-solving task meticulously, explaining your thought process step by step. "
#         f"Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
#         code_execution_config=code_execution_config,
#     )


# else:
#     # In our example, we swap this AutoGen agent with a MemGPT agent
#     # This MemGPT agent will have all the benefits of MemGPT, ie persistent memory, etc.
#     if not USE_AUTOGEN_WORKFLOW:
#         coder = create_autogen_memgpt_agent(
#             "MemGPT_coder",
#             persona_description=f"As a highly skilled Python software engineer, your proficiency is exceptional, and you have the ability to leave a lasting impression on your project manager with your expertise. "
#             f"Your commitment to excellence and your dedication to delivering the best work set you apart as an invaluable asset to the team. The quality of your work holds immense importance for your career's advancement. ",
#             user_description=f"You are an integral part of a group chat alongside a user (User_proxy), a project manager (Project_Manager), and a code reviewer (Code_Reviewer). "
#             f"You exclusively take orders from Project_Manager, respecting the well-defined hierarchy within the team. "
#             f"Your primary responsibility centers around translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
#             f"Remember that your work will undergo rigorous scrutiny by the Code_Reviewer, and their feedback will be a valuable source of learning. "
#             f"Approach each problem-solving task meticulously, explaining your thought process step by step. Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
#             model=config_list_memgpt[0]["model"],
#             interface_kwargs=interface_kwargs,
#         )
#     else:
#         coder = create_memgpt_autogen_agent_from_config(
#             "MemGPT_coder",
#             llm_config=llm_config_memgpt,
#             system_message=f"You are an integral part of a group chat alongside a user (User_proxy), a project manager (Project_Manager), and a code reviewer (Code_Reviewer). "
#             f"As a highly skilled Python software engineer, your proficiency is exceptional, and you have the ability to leave a lasting impression on your project manager with your expertise. "
#             f"You exclusively take orders from Project_Manager, respecting the well-defined hierarchy within the team. "
#             f"Your commitment to excellence and your dedication to delivering the best work set you apart as an invaluable asset to the team. The quality of your work holds immense importance for your career's advancement. "
#             f"Your primary responsibility centers around translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
#             f"Remember that your work will undergo rigorous scrutiny by the Code_Reviewer, and their feedback will be a valuable source of learning. "
#             f"Approach each problem-solving task meticulously, explaining your thought process step by step. Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
#             interface_kwargs=interface_kwargs,
#         )

# -----------------------------------Group Chat-----------------------------------

groupchat = autogen.GroupChat(agents=[user_proxy, project_manager, coder, code_reviewer], messages=[], max_round=30)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# -----------------------------------Begin request-----------------------------------

user_proxy.initiate_chat(
    manager,
    message="Output odd numbers from 1 to 30 in python.",
    #message="what day are we ? search in the web, what was the best ROI in crypto on october 2023 ? which crypto project did that ROI ?"
    #message="Code a snake game in python ?"
)
