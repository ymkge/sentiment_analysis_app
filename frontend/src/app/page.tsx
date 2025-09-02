'use client';

import { useState } from 'react';

// APIレスポンスの型定義
interface SentimentResult {
  label: 'ポジティブ' | 'ネガティブ';
  score: number;
}

export default function Home() {
  const [text, setText] = useState<string>('このサービスは本当に素晴らしい！');
  const [result, setResult] = useState<SentimentResult | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });

      if (!response.ok) {
        throw new Error(`APIエラー: ${response.statusText}`);
      }

      const data: SentimentResult = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || '分析中に不明なエラーが発生しました。');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gray-50 font-sans">
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-lg p-8">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-2">感情分析アプリ</h1>
        <p className="text-center text-gray-500 mb-8">scikit-learn + FastAPI + Next.js</p>

        <form onSubmit={handleSubmit}>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="w-full h-40 p-4 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 resize-none"
            placeholder="ここに分析したい文章を入力してください..."
          />
          <button
            type="submit"
            disabled={isLoading || !text}
            className="w-full mt-4 px-4 py-3 bg-blue-600 text-white font-semibold rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition duration-200"
          >
            {isLoading ? '分析中...' : '分析する'}
          </button>
        </form>

        {error && (
          <div className="mt-6 p-4 bg-red-100 text-red-700 border border-red-300 rounded-md">
            <p className="font-semibold">エラー</p>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="mt-6 p-6 border border-gray-200 rounded-lg bg-gray-50">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">分析結果</h2>
            <div className="flex items-center justify-between">
              <p className="text-lg">判定:</p>
              <span
                className={`px-4 py-1 text-lg font-bold rounded-full ${result.label === 'ポジティブ' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {result.label}
              </span>
            </div>
            <div className="flex items-center justify-between mt-4">
              <p className="text-lg">確信度:</p>
              <div className="w-1/2 bg-gray-200 rounded-full h-6">
                <div
                  className={`h-6 rounded-full ${result.label === 'ポジティブ' ? 'bg-green-500' : 'bg-red-500'}`}
                  style={{ width: `${Math.round(result.score * 100)}%` }}
                ></div>
              </div>
              <span className="text-lg font-mono w-20 text-right">{(result.score * 100).toFixed(1)}%</span>
            </div>
          </div>
        )}
      </div>
      <footer className="mt-8 text-center text-gray-500">
        <p>Powered by Gemini</p>
      </footer>
    </main>
  );
}
