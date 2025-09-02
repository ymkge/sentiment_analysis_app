'use client';

import { useState, Fragment } from 'react';
import { Sparkles, LoaderCircle, AlertTriangle, Smile, Frown, Star } from 'lucide-react';

// APIレスポンスの型定義
interface SentimentDetail {
  label: string;
  score: number;
}

interface SentimentResult {
  label: 'ポジティブ' | 'ネガティブ';
  score: number;
  details: SentimentDetail[];
}

// 星のレンダリング用ヘルパー
const StarRating = ({ rating }: { rating: number }) => (
  <div className="flex items-center">
    {[...Array(5)].map((_, i) => (
      <Star key={i} className={`w-5 h-5 ${i < rating ? 'text-yellow-400' : 'text-gray-300'}`} fill="currentColor" />
    ))}
  </div>
);

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
        
        <div className="flex items-center justify-center gap-3 mb-4">
          <Sparkles className="w-8 h-8 text-indigo-500" />
          <h1 className="text-3xl sm:text-4xl font-bold text-center text-gray-800">
            感情分析AI
          </h1>
        </div>
        <p className="text-center text-gray-500 mb-8">文章を入力して、AIによる感情分析を試してみましょう。</p>

        <form onSubmit={handleSubmit}>
          <div className="relative w-full">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full h-40 p-4 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition duration-200 resize-none text-gray-800 bg-white/80"
              placeholder="ここに分析したい文章を入力してください..."
            />
            <button type="button" onClick={() => setText('')} className="absolute top-3 right-3 text-gray-400 hover:text-gray-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
          <button
            type="submit"
            disabled={isLoading || !text}
            className="w-full mt-4 px-4 py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <Fragment>
                <LoaderCircle className="animate-spin h-5 w-5" />
                <span>分析中...</span>
              </Fragment>
            ) : (
              <span>分析する</span>
            )}
          </button>
        </form>

        <div className="mt-6 min-h-[240px]">
          {error && (
            <div className="p-4 bg-red-100 text-red-800 border border-red-300 rounded-lg flex items-center gap-3 animate-fade-in">
              <AlertTriangle className="h-6 w-6" />
              <div>
                <p className="font-semibold">エラーが発生しました</p>
                <p className="text-sm">{error}</p>
              </div>
            </div>
          )}

          {result && (
            <div className="p-6 border border-gray-200/80 rounded-lg bg-gray-50/50 animate-fade-in">
              <h2 className="text-xl font-semibold text-gray-800 mb-4 text-center">分析結果</h2>
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4 mb-6">
                <div className="flex flex-col items-center gap-2">
                  <p className="text-sm text-gray-600">最終判定</p>
                  <span
                    className={`px-4 py-1 text-lg font-bold rounded-full ${result.label === 'ポジティブ' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {result.label}
                  </span>
                </div>
                <div className="flex flex-col items-center gap-2">
                   <p className="text-sm text-gray-600">モデルの予測</p>
                   <StarRating rating={parseInt(result.details.find(d => d.score === result.score)?.label.split(' ')[0] || '0')} />
                </div>
              </div>

              <h3 className="text-md font-semibold text-gray-700 mb-2">AIの思考プロセス</h3>
              <div className="space-y-2">
                {result.details.map((detail) => {
                  const rating = parseInt(detail.label.split(' ')[0]);
                  return (
                    <div key={detail.label} className="flex items-center gap-3">
                      <div className="w-12 text-sm text-gray-600 font-mono">{rating}つ星</div>
                      <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
                        <div
                          className="h-full rounded-full bg-indigo-400 transition-all duration-1000 ease-out text-right pr-2 text-white text-sm flex items-center justify-end"
                          style={{ width: `${Math.round(detail.score * 100)}%` }}
                        >
                          {(detail.score * 100).toFixed(1)}%
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
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