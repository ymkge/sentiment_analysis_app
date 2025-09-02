'use client';

import { useState } from 'react';
import { AppTitle } from '@/components/AppTitle';
import { InputForm } from '@/components/InputForm';
import { ResultDisplay } from '@/components/ResultDisplay';

// APIレスポンスの型定義
interface SentimentDetail {
  label: string;
  score: number;
}

export interface SentimentResult {
  label: 'ポジティブ' | 'ネガティブ';
  score: number;
  details: SentimentDetail[];
}

export default function Home() {
  const [text, setText] = useState<string>('このサービスは本当に素晴らしい！心からお勧めします。');
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
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `APIエラー: ${response.statusText}`);
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
    <main className="flex min-h-screen flex-col items-center justify-center p-4 sm:p-8 bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 font-sans">
      <div className="w-full max-w-2xl bg-white/70 backdrop-blur-xl border border-gray-200/80 shadow-2xl rounded-2xl p-6 sm:p-10">
        <AppTitle />
        <InputForm
          text={text}
          setText={setText}
          handleSubmit={handleSubmit}
          isLoading={isLoading}
        />
        <ResultDisplay result={result} error={error} />
      </div>
      <footer className="mt-8 text-center text-gray-500">
        <p>Powered by Gemini</p>
      </footer>
      <style jsx global>{`
        @keyframes fade-in {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.5s ease-out forwards;
        }
      `}</style>
    </main>
  );
}