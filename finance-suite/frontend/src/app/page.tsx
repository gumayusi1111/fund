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
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="px-4 py-12">
      {/* 欢迎部分 */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          欢迎使用个人指数分析平台
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          专业的指数分析、基金对比和投资预测工具，帮助您做出更明智的投资决策
        </p>
      </div>

      {/* 功能卡片 */}
      <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
        <Link href="/indices" className="group">
          <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-200 group-hover:border-primary-300">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">指数分析</h3>
            <p className="text-gray-600 mb-4">
              查询和对比各类指数表现，包括沪深300、中证500等主要指数
            </p>
            <div className="text-primary-600 font-medium group-hover:text-primary-700">
              立即分析 →
            </div>
          </div>
        </Link>

        <Link href="/funds" className="group">
          <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-200 group-hover:border-primary-300">
            <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">💰</span>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">基金分析</h3>
            <p className="text-gray-600 mb-4">
              深入分析基金表现，对比不同基金的收益和风险特征
            </p>
            <div className="text-primary-600 font-medium group-hover:text-primary-700">
              开始分析 →
            </div>
          </div>
        </Link>

        <Link href="/predictions" className="group">
          <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6 border border-gray-200 group-hover:border-primary-300">
            <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🔮</span>
            </div>
            <h3 className="text-xl font-semibold mb-2 text-gray-900">收益预测</h3>
            <p className="text-gray-600 mb-4">
              基于历史数据预测投资收益，分析定投策略效果
            </p>
            <div className="text-primary-600 font-medium group-hover:text-primary-700">
              开始预测 →
            </div>
          </div>
        </Link>
      </div>

      {/* 快速开始 */}
      <div className="bg-gray-50 rounded-lg p-8 max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-6">快速开始</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="font-semibold mb-3 text-lg">新手指南</h3>
            <ol className="space-y-2 text-gray-600">
              <li>1. 选择感兴趣的指数或基金</li>
              <li>2. 查看历史表现和风险指标</li>
              <li>3. 使用对比功能分析多个产品</li>
              <li>4. 进行投资收益预测</li>
            </ol>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-sm">
            <h3 className="font-semibold mb-3 text-lg">热门功能</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• 沪深300指数实时追踪</li>
              <li>• 定投策略收益计算</li>
              <li>• 基金风险等级评估</li>
              <li>• 投资组合优化建议</li>
            </ul>
          </div>
        </div>
      </div>

      {/* 数据来源说明 */}
      <div className="text-center mt-12 text-sm text-gray-500">
        <p>数据来源：AKShare | 本平台仅供学习和研究使用，不构成投资建议</p>
      </div>
    </div>
  )
}
