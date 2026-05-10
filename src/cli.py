from src.agent import create_initial_conversation_history, trim_conversation_history
from src.config import EXIT_COMMANDS
from src.errors import print_openai_error_message
from src.openai_client import generate_ai_response
from src.stats import create_execution_stats, print_execution_summary
from src.project_summary import create_project_summary
from src.todo_candidates import create_todo_candidates
from src.command_suggestions import create_command_suggestions
from src.doc_suggestions import create_doc_suggestions


def run_todo_agent_chat_loop(client) -> None:
    print("AIエージェントを開始します。終了するには exit または quit と入力してください。")
    conversation_history = create_initial_conversation_history()
    stats = create_execution_stats()

    while True:
        user_input = input("あなた: ").strip()

        if user_input.lower() in EXIT_COMMANDS:
            print("終了します。")
            print_execution_summary(stats)
            break

        if not user_input:
            print("入力が空です。質問を入力してください。")
            continue

        if user_input.lower() == "summary":
            print(create_project_summary())
            continue

        if user_input.lower() == "todo-candidates":
            print(create_todo_candidates())
            continue

        if user_input.lower() == "command-suggestions":
            print(create_command_suggestions())
            continue

        if user_input.lower() == "doc-suggestions":
            print(create_doc_suggestions())
            continue

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history = trim_conversation_history(conversation_history)

        try:
            ai_response = generate_ai_response(client, conversation_history)
            stats["api_success_count"] += 1
            print(f"AI: {ai_response}")
            conversation_history.append({"role": "assistant", "content": ai_response})
            conversation_history = trim_conversation_history(conversation_history)
        except Exception as error:
            stats["error_count"] += 1
            print_openai_error_message(error)
