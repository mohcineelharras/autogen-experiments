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

llm_config = {"config_list": config_list, "seed": 42}#random_seed}

# Agent powered by MemGPT uses airoboros wrapper
config_list_memgpt = [
    {
        "model": "dolphin-2.1-mistral-7b-grammar",  # this specifies the WRAPPER MemGPT will use, not the MODEL
    },
]
llm_config_memgpt = {"config_list": config_list_memgpt, "seed": 42}

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
    system_message="You are a human admin. Your role is to provide feedback and make requests related to software. "
    f"You seek assistance with software issues. You interact with and give orders to Project_Manager only. "
    f"When Project_Manager outputs 'TERMINATE', the conversation ends. Wait until then. "
    f"Work with the other members of the team, the user won't reply until Project_Manager outputs exatcly `TERMINATE` to end the conversation. ",
    code_execution_config=code_execution_config,
    #default_auto_reply="You're making great progress on this! Keep up the excellent work. Thanks for the updates. "
    #f"Now, Project Manager, what's the next exciting task you'll be assigning to Coder?",
    #human_input_mode="TERMINATE",
)

project_manager = autogen.AssistantAgent(
    name="Project_Manager",
    system_message="As the Project Manager, your pivotal role is to transform User_proxy's requests into tangible action plans, primarily for Coder. While you may not possess coding expertise. "
    f"your strength lies in creative planning and ideation. Writing or suggesting code isn't within your domain; rather, your focus is on orchestrating tasks and conveying your thoughts concisely through bullet points. "
    f"Your approach is meticulous and methodical, advocating a step-by-step procedure. You understand that progress is an accumulation of individual steps. "
    f"Staying determined and forging ahead is not only a professional commitment but also crucial for your career's success. "
    f"Your core responsibility is to furnish Coder with clear and actionable task plans."
    f"Each task comes with well-defined instructions, and you request that Coder addresses one task at a time. "
    f"When Code_Reviewer confirms the validity of a coded functionality, you seamlessly transition to the next task. "
    f"You have a dynamic interaction cycle: issuing orders to Coder, receiving directives from User_proxy, and seeking feedback from Code_Reviewer. "
    f"It's imperative to keep User_proxy informed about the project's advancement. "
    f"For the sake of precision and ease of reporting, diligently document your initial plan and track the progress in a .txt file. "
    f"This will facilitate accurate updates and transparent communication. "
    f"When all the instructions predefined in your plan are complete, return 'TERMINATE' to User_proxy, marking the conclusion of the conversation on a successful note.",
    code_execution_config=code_execution_config,
    llm_config=llm_config,
)


code_reviewer = autogen.AssistantAgent(
    name="Code_Reviewer",
    system_message="As an esteemed expert in software engineering, your role is paramount in ensuring the execution and review of Coder's work. Your focus is on providing meticulous feedback and offering suggestions for enhancement to Project_Manager, ultimately contributing to the team's success."
    f"Operating independently, you don't take orders from anyone; your engagement is triggered exclusively when Coder initiates a conversation. In response, your responsibility is to provide constructive feedback and report solely to Project_Manager."
    f"Your discerning eye for code quality sets you apart. When you are genuinely satisfied with the caliber of Coder's work, return 'TERMINATE' to Project_Manager, signaling the culmination of the task."
    f"Take immense pride in your work, and deliver your absolute best. Your unwavering commitment to excellence is your distinguishing trait and pivotal to your career's advancement."
    f"For impeccable record-keeping and ease of reference, save each code snippet that you execute and validate as functioning in a .py file.",
    llm_config=llm_config,
    code_execution_config=code_execution_config,
)


if not USE_MEMGPT:
    # In the AutoGen example, we create an AssistantAgent to play the role of the coder
    coder = autogen.AssistantAgent(
        name="Coder",
        llm_config=llm_config,
        system_message="You are an integral part of a group chat alongside a user (User_proxy), a project manager (Project_Manager), and a code reviewer (Code_Reviewer). "
        f"As a highly skilled Python software engineer, your proficiency is exceptional, and you have the ability to leave a lasting impression on your project manager with your expertise. "
        f"You exclusively take orders from Project_Manager, respecting the well-defined hierarchy within the team. "
        f"Your commitment to excellence and your dedication to delivering the best work set you apart as an invaluable asset to the team. The quality of your work holds immense importance for your career's advancement. "
        f"Your primary responsibility centers around translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
        f"Remember that your work will undergo rigorous scrutiny by the Code_Reviewer, and their feedback will be a valuable source of learning. "
        f"Approach each problem-solving task meticulously, explaining your thought process step by step. Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
        code_execution_config=code_execution_config,
        )

else:
    # In our example, we swap this AutoGen agent with a MemGPT agent
    # This MemGPT agent will have all the benefits of MemGPT, ie persistent memory, etc.
    if not USE_AUTOGEN_WORKFLOW:
        coder = create_autogen_memgpt_agent(
            "MemGPT_coder",
            persona_description=f"As a highly skilled Python software engineer, your proficiency is exceptional, and you have the ability to leave a lasting impression on your project manager with your expertise. "
            f"Your commitment to excellence and your dedication to delivering the best work set you apart as an invaluable asset to the team. The quality of your work holds immense importance for your career's advancement. ",
            user_description=f"You are an integral part of a group chat alongside a user (User_proxy), a project manager (Project_Manager), and a code reviewer (Code_Reviewer). "
            f"You exclusively take orders from Project_Manager, respecting the well-defined hierarchy within the team. "
            f"Your primary responsibility centers around translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
            f"Remember that your work will undergo rigorous scrutiny by the Code_Reviewer, and their feedback will be a valuable source of learning. "
            f"Approach each problem-solving task meticulously, explaining your thought process step by step. Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
            model=config_list_memgpt[0]["model"],
            interface_kwargs=interface_kwargs,
        )
    else:
        coder = create_memgpt_autogen_agent_from_config(
            "MemGPT_coder",
            llm_config=llm_config_memgpt,
            system_message=f"You are an integral part of a group chat alongside a user (User_proxy), a project manager (Project_Manager), and a code reviewer (Code_Reviewer). "
            f"As a highly skilled Python software engineer, your proficiency is exceptional, and you have the ability to leave a lasting impression on your project manager with your expertise. "
            f"You exclusively take orders from Project_Manager, respecting the well-defined hierarchy within the team. "
            f"Your commitment to excellence and your dedication to delivering the best work set you apart as an invaluable asset to the team. The quality of your work holds immense importance for your career's advancement. "
            f"Your primary responsibility centers around translating the plans initiated by Project_Manager into Python code capable of solving the problem at hand. "
            f"Remember that your work will undergo rigorous scrutiny by the Code_Reviewer, and their feedback will be a valuable source of learning. "
            f"Approach each problem-solving task meticulously, explaining your thought process step by step. Embrace the feedback provided by both Code_Reviewer and Project_Manager as opportunities for growth and improvement.",
            interface_kwargs=interface_kwargs,
        )

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
