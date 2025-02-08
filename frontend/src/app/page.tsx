"use client"

import React, { useState } from 'react';
import { Search, Code, BookOpen, Brain, Zap, Trophy, LogIn } from 'lucide-react';
import dynamic from 'next/dynamic';
import { LoadingSpinner } from '@/components/common/loading-spinner';

const CodeArena = dynamic(() => import('@/components/codearena/code_arena'), {
  loading: () => <LoadingSpinner />,
  ssr: false,
});

const Page = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const categories = [
    { icon: <Code className="w-6 h-6" />, name: 'String Handling', count: '150+ Problems', value: 'String Handling' },
    { icon: <BookOpen className="w-6 h-6" />, name: 'Data Structures', count: '200+ Problems', value: 'Data Structures' },
    { icon: <Brain className="w-6 h-6" />, name: 'Algorithms', count: '180+ Problems', value: 'Algorithms' },
    { icon: <Zap className="w-6 h-6" />, name: 'Problem Solving', count: '120+ Problems', value: 'Problem Solving' },
    { icon: <Zap className="w-6 h-6" />, name: 'Array', count: '120+ Problems', value: 'Array' }

  ];

  const features = [
    { title: 'Interactive Code Editor', description: 'Write, test, and debug code in 10+ programming languages' },
    { title: 'Real-time Feedback', description: 'Get instant feedback on your code submissions' },
    { title: 'Progress Tracking', description: 'Track your learning journey with detailed statistics' },
    { title: 'Structured Learning Path', description: 'Follow curated paths from basics to advanced topics' }
  ];

  const handleCategorySelect = (categoryValue: string) => {
    setSelectedCategory(categoryValue);
  };

  const handleBack = () => {
    setSelectedCategory(null);
  };

  if (selectedCategory) {
    return <CodeArena category={selectedCategory} onBack={handleBack} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">CodeCraft Academy</h1>
          <div className="flex items-center gap-4">
            <button className="px-4 py-2 text-gray-600 hover:text-gray-900">Explore</button>
            <div className="relative group">
              <button className="px-4 py-2 text-gray-600 hover:text-gray-900">Practice</button>
              <div className="absolute hidden group-hover:block w-48 right-0 mt-2 py-2 bg-white rounded-lg shadow-xl">
                {categories.map((category, index) => (
                  <button
                    key={index}
                    className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center gap-2"
                    onClick={() => handleCategorySelect(category.value)}
                  >
                    {category.icon}
                    <span>{category.name}</span>
                  </button>
                ))}
              </div>
            </div>
            <button className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              <LogIn className="w-4 h-4" />
              Login
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Be the GOAT Coder - Master Coding Through Practice!
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands of developers mastering coding skills across programming languages
          </p>
          <div className="flex justify-center gap-4">
            <button className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
              Start Practicing
            </button>
            <button className="px-6 py-3 border border-gray-300 rounded-lg hover:border-gray-400">
              View Problems
            </button>
          </div>
        </div>
      </div>

      {/* Categories Grid */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <h3 className="text-2xl font-bold text-gray-900 mb-8">Problem Categories</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category, index) => (
            <button
              key={index}
              onClick={() => handleCategorySelect(category.value)}
              className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow text-left"
            >
              <div className="flex items-center gap-4 mb-4">
                {category.icon}
                <h4 className="text-lg font-semibold">{category.name}</h4>
              </div>
              <p className="text-gray-600">{category.count}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h3 className="text-2xl font-bold text-gray-900 mb-8">Why Choose Us?</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <h4 className="text-lg font-semibold mb-2">{feature.title}</h4>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-indigo-600 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to Start Your Coding Journey?</h3>
          <p className="text-lg mb-8">Join our community of developers and level up your coding skills</p>
          <button className="px-8 py-4 bg-white text-indigo-600 rounded-lg hover:bg-gray-100">
            Get Started Now
          </button>
        </div>
      </div>
    </div>
  );
};

export default Page;