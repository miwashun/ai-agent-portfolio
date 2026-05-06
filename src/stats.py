# 統計情報を初期化する関数
def create_execution_stats() -> dict[str, int]:
    return {
        "api_success_count": 0,
        "error_count": 0,
    }


# 実行サマリーを表示する関数
def print_execution_summary(stats: dict[str, int]) -> None:
    print("\n実行サマリー:")
    print(f"- API呼び出し成功回数: {stats['api_success_count']}")
    print(f"- エラー回数: {stats['error_count']}")
