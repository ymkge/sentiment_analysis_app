'use client';

import { Sparkles } from 'lucide-react';

export const AppTitle = () => (
  <>
    <div className="flex items-center justify-center gap-3 mb-4">
      <Sparkles className="w-8 h-8 text-indigo-500" />
      <h1 className="text-3xl sm:text-4xl font-bold text-center text-gray-800">
        感情分析AI
      </h1>
    </div>
    <p className="text-center text-gray-500 mb-8">文章を入力して、AIによる感情分析を試してみましょう。</p>
  </>
);
