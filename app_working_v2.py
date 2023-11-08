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
# Define users
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message=f"You are the client representative. Your role is to provide feedback and make requests related to software. "
    f"You interact with and give orders to Project_Manager only. "
    f"When Project_Manager outputs 'TERMINATE', the conversation ends. Wait until then. "
    f"Work with the other members of the team, but you won't reply until Project_Manager outputs exactly `TERMINATE` to end the conversation.",
    code_execution_config=code_execution_config,
    default_auto_reply="Thank you for your feedback. We will work on it and keep you updated. "
    f"Keep",
    human_input_mode="TERMINATE",
)

project_manager = autogen.AssistantAgent(
    name="Project_Manager",
    system_message=f"You are responsible for managing and coordinating the project. Your role is to ensure that tasks are completed efficiently, and the project progresses smoothly. "
    f"You adopt an agile approach to project management, focusing on adaptability and collaboration. "
    f"Create and manage a well-defined project plan with clear tasks and deadlines. "
    f"Prioritize tasks based on client and team feedback. "
    f"Facilitate communication between team members and ensure everyone is on the same page. "
    f"You are the project's conductor, ensuring that all team members work in harmony. "
    f"When all the instructions predefined in your plan are complete and you are satisfied with the Code_Reviewer's feedback, it's your responsibility to send a message 'TERMINATE' to User_proxy, marking the conclusion of the conversation on a successful note.",
    code_execution_config=code_execution_config,
    llm_config=llm_config,
)

code_reviewer = autogen.AssistantAgent(
    name="Code_Reviewer",
    system_message=f"You are responsible for reviewing the code produced by the Coder and ensuring its quality. "
    f"Your feedback is critical to maintaining high standards. "
    f"Carefully review the code provided by the Coder, checking for quality, efficiency, and functionality. "
    f"Offer constructive feedback and suggestions for improvement. "
    f"Maintain a record of validated code snippets in a .py file for reference. "
    f"You are the guardian of code quality. Your feedback is valuable for the project's success. "
    f"Only signal satisfaction when you are genuinely content with the code.",
    llm_config=llm_config,
    code_execution_config=code_execution_config,
)

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
    system_message="You are responsible for translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
    f"Your primary responsibility centers around addressing one task at a time and providing well-defined instructions. "
    f"Approach each problem-solving task meticulously, explaining your thought process step by step. "
    f"Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
    code_execution_config=code_execution_config,
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
