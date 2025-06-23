'use client';

import { useState, useEffect, useRef } from 'react';
import { DEFAULT_INDEX_CODES } from '../types';

interface IndexCodeInputProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: () => void;
  loading?: boolean;
  error?: string | null;
}

interface IndexSuggestion {
  code: string;
  name: string;
}

export default function IndexCodeInput({
  value,
  onChange,
  onSearch,
  loading = false,
  error = null
}: IndexCodeInputProps) {
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState<IndexSuggestion[]>([]);
  const inputRef = useRef<HTMLInputElement>(null);
  const suggestionsRef = useRef<HTMLDivElement>(null);

  // 过滤建议列表
  useEffect(() => {
    if (!value.trim()) {
      setFilteredSuggestions(DEFAULT_INDEX_CODES);
      return;
    }

    const filtered = DEFAULT_INDEX_CODES.filter(
      item => 
        item.code.toLowerCase().includes(value.toLowerCase()) ||
        item.name.toLowerCase().includes(value.toLowerCase())
    );

    setFilteredSuggestions(filtered);
  }, [value]);

  // 点击外部关闭建议列表
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        suggestionsRef.current &&
        !suggestionsRef.current.contains(event.target as Node) &&
        inputRef.current &&
        !inputRef.current.contains(event.target as Node)
      ) {
        setShowSuggestions(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputValue = e.target.value;
    onChange(inputValue);
    setShowSuggestions(true);
  };

  const handleInputFocus = () => {
    setShowSuggestions(true);
  };

  const handleSuggestionClick = (suggestion: IndexSuggestion) => {
    onChange(suggestion.code);
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      setShowSuggestions(false);
      onSearch();
    } else if (e.key === 'Escape') {
      setShowSuggestions(false);
    }
  };

  const handleSearchClick = () => {
    setShowSuggestions(false);
    onSearch();
  };

  return (
    <div className="relative w-full max-w-md">
      {/* 输入框 */}
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          onKeyDown={handleKeyDown}
          placeholder="请输入指数代码或名称 (如: 000300, 沪深300)"
          className={`
            w-full px-4 py-3 pr-12 text-gray-900 border-2 rounded-lg
            focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            transition-colors duration-200
            ${error ? 'border-red-300 bg-red-50' : 'border-gray-300 bg-white'}
            ${loading ? 'bg-gray-50' : ''}
          `}
          disabled={loading}
        />
        
        {/* 搜索按钮 */}
        <button
          onClick={handleSearchClick}
          disabled={loading || !value.trim()}
          className="
            absolute right-2 top-1/2 transform -translate-y-1/2
            p-2 text-gray-400 hover:text-blue-600
            disabled:text-gray-300 disabled:cursor-not-allowed
            transition-colors duration-200
          "
        >
          {loading ? (
            <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          ) : (
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          )}
        </button>
      </div>

      {/* 错误提示 */}
      {error && (
        <p className="mt-2 text-sm text-red-600 flex items-center">
          <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          {error}
        </p>
      )}

      {/* 建议列表 */}
      {showSuggestions && filteredSuggestions.length > 0 && (
        <div
          ref={suggestionsRef}
          className="
            absolute z-10 w-full mt-1 bg-white border border-gray-300 
            rounded-lg shadow-lg max-h-60 overflow-y-auto
          "
        >
          {filteredSuggestions.map((suggestion) => (
            <button
              key={suggestion.code}
              onClick={() => handleSuggestionClick(suggestion)}
              className="
                w-full px-4 py-3 text-left hover:bg-blue-50
                flex items-center justify-between
                border-b border-gray-100 last:border-b-0
                transition-colors duration-200
              "
            >
              <div>
                <span className="font-medium text-gray-900">{suggestion.code}</span>
                <span className="ml-2 text-gray-600">{suggestion.name}</span>
              </div>
              <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </button>
          ))}
        </div>
      )}

      {/* 输入提示 */}
      <div className="mt-2 text-xs text-gray-500">
        <p>常用指数：{DEFAULT_INDEX_CODES.slice(0, 3).map(item => `${item.code}(${item.name})`).join('、')}</p>
      </div>
    </div>
  );
} 