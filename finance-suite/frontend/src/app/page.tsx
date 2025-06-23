'use client'

import Link from 'next/link'
import { useState, useEffect } from 'react'

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    setIsLoading(false)
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="px-4 py-12">
      {/* 欢迎部分 */}
      <div className="text-center mb-16">
        <div className="mb-6">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <span className="text-4xl text-white">📈</span>
          </div>
        </div>
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          专业的金融数据分析平台
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          提供全面的指数分析、基金对比和投资预测工具，基于真实市场数据，帮助您做出更明智的投资决策
        </p>
        <div className="mt-8 flex justify-center space-x-4">
          <Link href="/index-analysis" className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg font-medium transition-colors duration-200 flex items-center space-x-2">
            <span>📊</span>
            <span>开始分析</span>
          </Link>
          <Link href="#features" className="border border-gray-300 hover:border-gray-400 text-gray-700 px-8 py-3 rounded-lg font-medium transition-colors duration-200">
            了解更多
          </Link>
        </div>
      </div>

      {/* 功能卡片 */}
      <div id="features" className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
        <Link href="/index-analysis" className="group">
          <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 group-hover:border-blue-200 transform group-hover:-translate-y-1">
            <div className="w-16 h-16 bg-gradient-to-br from-blue-100 to-blue-200 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
              <span className="text-3xl">📊</span>
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900 group-hover:text-blue-600 transition-colors">指数分析</h3>
            <p className="text-gray-600 mb-6 leading-relaxed">
              深度分析主要指数表现，包括沪深300、中证500等核心指数的历史走势和技术指标
            </p>
            <div className="flex items-center text-blue-600 font-medium group-hover:text-blue-700">
              <span>立即分析</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </Link>

        <Link href="/funds" className="group">
          <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 group-hover:border-green-200 transform group-hover:-translate-y-1">
            <div className="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
              <span className="text-3xl">💰</span>
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900 group-hover:text-green-600 transition-colors">基金分析</h3>
            <p className="text-gray-600 mb-6 leading-relaxed">
              全面评估基金表现，对比不同基金的收益率、风险指标和投资策略
            </p>
            <div className="flex items-center text-green-600 font-medium group-hover:text-green-700">
              <span>开始分析</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </Link>

        <Link href="/predictions" className="group">
          <div className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 p-8 border border-gray-100 group-hover:border-purple-200 transform group-hover:-translate-y-1">
            <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-purple-200 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-200">
              <span className="text-3xl">🔮</span>
            </div>
            <h3 className="text-2xl font-bold mb-4 text-gray-900 group-hover:text-purple-600 transition-colors">收益预测</h3>
            <p className="text-gray-600 mb-6 leading-relaxed">
              基于历史数据和机器学习算法，预测投资收益并分析定投策略效果
            </p>
            <div className="flex items-center text-purple-600 font-medium group-hover:text-purple-700">
              <span>开始预测</span>
              <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </Link>
      </div>

      {/* 特色功能 */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-12 max-w-6xl mx-auto mb-16">
        <div className="text-center mb-10">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">平台特色</h2>
          <p className="text-gray-600 text-lg">为什么选择我们的分析平台</p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-blue-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-white text-2xl">⚡</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">实时数据</h3>
            <p className="text-gray-600 text-sm">接入权威数据源，提供实时准确的市场信息</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-white text-2xl">🎯</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">精准分析</h3>
            <p className="text-gray-600 text-sm">专业的技术指标和风险评估模型</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-white text-2xl">📱</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">响应式设计</h3>
            <p className="text-gray-600 text-sm">支持所有设备，随时随地进行分析</p>
          </div>
          <div className="text-center">
            <div className="w-12 h-12 bg-orange-500 rounded-lg flex items-center justify-center mx-auto mb-4">
              <span className="text-white text-2xl">🔒</span>
            </div>
            <h3 className="font-bold text-gray-900 mb-2">安全可靠</h3>
            <p className="text-gray-600 text-sm">数据加密传输，保护您的隐私安全</p>
          </div>
        </div>
      </div>

      {/* 快速开始 */}
      <div className="bg-white rounded-2xl shadow-lg p-12 max-w-5xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-10 text-gray-900">快速开始</h2>
        <div className="grid md:grid-cols-2 gap-10">
          <div className="bg-gray-50 p-8 rounded-xl">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center mr-4">
                <span className="text-white font-bold">1</span>
              </div>
              <h3 className="font-bold text-xl text-gray-900">新手指南</h3>
            </div>
            <ol className="space-y-3 text-gray-600">
              <li className="flex items-start">
                <span className="text-blue-500 mr-3">•</span>
                选择感兴趣的指数或基金代码
              </li>
              <li className="flex items-start">
                <span className="text-blue-500 mr-3">•</span>
                查看详细的历史表现和风险指标
              </li>
              <li className="flex items-start">
                <span className="text-blue-500 mr-3">•</span>
                使用对比功能分析多个投资标的
              </li>
              <li className="flex items-start">
                <span className="text-blue-500 mr-3">•</span>
                进行收益预测和投资策略分析
              </li>
            </ol>
          </div>
          <div className="bg-gray-50 p-8 rounded-xl">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center mr-4">
                <span className="text-white font-bold">⭐</span>
              </div>
              <h3 className="font-bold text-xl text-gray-900">热门功能</h3>
            </div>
            <ul className="space-y-3 text-gray-600">
              <li className="flex items-start">
                <span className="text-green-500 mr-3">📈</span>
                沪深300指数实时追踪分析
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-3">💡</span>
                智能定投策略收益计算
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-3">⚖️</span>
                基金风险等级专业评估
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-3">🎯</span>
                个性化投资组合优化建议
              </li>
            </ul>
          </div>
        </div>
      </div>

      {/* 数据来源说明 */}
      <div className="text-center mt-16 py-8 border-t border-gray-200">
        <p className="text-sm text-gray-500 mb-2">
          <span className="font-medium">数据来源：</span>AKShare 实时金融数据接口
        </p>
        <p className="text-xs text-gray-400">
          本平台仅供学习和研究使用，所有分析结果不构成投资建议，投资有风险，入市需谨慎
        </p>
      </div>
    </div>
  )
}
