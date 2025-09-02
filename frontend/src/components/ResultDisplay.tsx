'use client';

import { AlertTriangle, Smile, Frown } from 'lucide-react';
import { StarRating } from './StarRating';
import type { SentimentResult } from '../app/page';

interface ResultDisplayProps {
  result: SentimentResult | null;
  error: string | null;
}

export const ResultDisplay = ({ result, error }: ResultDisplayProps) => (
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
);