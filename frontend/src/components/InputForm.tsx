'use client';

import { Fragment } from 'react';
import { LoaderCircle } from 'lucide-react';

interface InputFormProps {
  text: string;
  setText: (text: string) => void;
  handleSubmit: (e: React.FormEvent) => void;
  isLoading: boolean;
}

export const InputForm = ({ text, setText, handleSubmit, isLoading }: InputFormProps) => (
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
);
