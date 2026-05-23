import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.page}>
      <section className={styles.main}>
        <div className={styles.intro}>
          <h1>AI Agent Chat Frontend</h1>
          <p>FastAPI backend と接続予定のNext.jsフロントエンドです。</p>
        </div>

        <div className={styles.chatArea}>
          <p className={styles.message}>AI: ここに会話履歴を表示します。</p>
        </div>

        <form className={styles.chatForm}>
          <input
            className={styles.messageInput}
            type="text"
            placeholder="メッセージを入力"
          />
          <button className={styles.submitButton} type="submit">
            送信
          </button>
        </form>
      </section>
    </main>
  );
}
