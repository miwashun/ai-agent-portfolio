import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.page}>
      <section className={styles.main}>
        <h1>AI Agent Chat Frontend</h1>
        <p>FastAPI backend と接続予定のNext.jsフロントエンドです。</p>
        <p>まずは画面構成を作り、その後 `/chat` APIとの接続に進みます。</p>
      </section>
    </main>
  );
}
