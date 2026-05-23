"use client";

import { FormEvent, useState } from "react";

import styles from "./page.module.css";

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
};

export default function Home() {
  const [inputMessage, setInputMessage] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "assistant", content: "ここに会話履歴を表示します。" },
  ]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loadConversationId, setLoadConversationId] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  function getApiBaseUrl() {
    const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;
    if (!apiBaseUrl) {
      throw new Error("NEXT_PUBLIC_API_BASE_URL が設定されていません。");
    }

    return apiBaseUrl;
  }

  function handleNewConversation() {
    setInputMessage("");
    setMessages([
      { role: "assistant", content: "ここに会話履歴を表示します。" },
    ]);
    setConversationId(null);
    setLoadConversationId("");
  }

  async function handleLoadConversation(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const requestedConversationId = loadConversationId.trim();
    if (!requestedConversationId || isLoadingHistory) {
      return;
    }

    setIsLoadingHistory(true);

    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(
        `${apiBaseUrl}/conversations/${requestedConversationId}`,
      );

      if (!response.ok) {
        throw new Error("会話履歴の読み込みに失敗しました。");
      }

      const data: { conversation_id: number; messages: ChatMessage[] } =
        await response.json();

      setConversationId(data.conversation_id);
      setLoadConversationId(String(data.conversation_id));
      setMessages(data.messages);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "予期しないエラーが発生しました。";
      setMessages([
        { role: "assistant", content: `エラー: ${errorMessage}` },
      ]);
    } finally {
      setIsLoadingHistory(false);
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const userMessage = inputMessage.trim();
    if (!userMessage || isLoading) {
      return;
    }

    const nextMessages: ChatMessage[] = [
      ...messages,
      { role: "user", content: userMessage },
    ];

    setMessages(nextMessages);
    setInputMessage("");
    setIsLoading(true);

    try {
      const apiBaseUrl = getApiBaseUrl();

      const response = await fetch(`${apiBaseUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          messages: nextMessages.map((message) => ({
            role: message.role,
            content: message.content,
          })),
        }),
      });

      if (!response.ok) {
        throw new Error("APIリクエストに失敗しました。");
      }

      const data: { reply: string; conversation_id: number } =
        await response.json();

      setConversationId(data.conversation_id);
      setMessages([
        ...nextMessages,
        { role: "assistant", content: data.reply },
      ]);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "予期しないエラーが発生しました。";
      setMessages([
        ...nextMessages,
        { role: "assistant", content: `エラー: ${errorMessage}` },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className={styles.page}>
      <section className={styles.main}>
        <div className={styles.intro}>
          <h1>AI Agent Chat Frontend</h1>
          <p>FastAPI backend と接続するNext.jsフロントエンドです。</p>
          <p>
            現在の会話ID: {conversationId === null ? "未作成" : conversationId}
          </p>
          <button
            className={styles.secondaryButton}
            type="button"
            onClick={handleNewConversation}
          >
            新規会話
          </button>
        </div>

        <form className={styles.loadForm} onSubmit={handleLoadConversation}>
          <input
            className={styles.messageInput}
            type="number"
            min="1"
            placeholder="会話ID"
            value={loadConversationId}
            onChange={(event) => setLoadConversationId(event.target.value)}
            disabled={isLoadingHistory}
          />
          <button
            className={styles.submitButton}
            type="submit"
            disabled={isLoadingHistory}
          >
            {isLoadingHistory ? "読み込み中..." : "履歴を読み込む"}
          </button>
        </form>

        <div className={styles.chatArea}>
          {messages.map((message, index) => (
            <p className={styles.message} key={`${message.role}-${index}`}>
              {message.role === "user" ? "あなた" : "AI"}: {message.content}
            </p>
          ))}
        </div>

        <form className={styles.chatForm} onSubmit={handleSubmit}>
          <input
            className={styles.messageInput}
            type="text"
            placeholder="メッセージを入力"
            value={inputMessage}
            onChange={(event) => setInputMessage(event.target.value)}
            disabled={isLoading}
          />
          <button
            className={styles.submitButton}
            type="submit"
            disabled={isLoading}
          >
            {isLoading ? "送信中..." : "送信"}
          </button>
        </form>
      </section>
    </main>
  );
}
