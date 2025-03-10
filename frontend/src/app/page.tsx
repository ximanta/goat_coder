"use client"

import React, { useEffect } from 'react';
import { Boxes, Puzzle, Network, TextCursor, CodeSquare, Search, Code, BookOpen, Brain, Zap, Trophy, LogIn } from 'lucide-react';
import dynamic from 'next/dynamic';
import { LoadingSpinner } from '@/app/components/common/loading-spinner';
import Heading from './heading';
import ProgramWisePractice from '@/app/components/program-wise-practice';
import { useRouter, useSearchParams } from 'next/navigation';
import { categories } from '@/lib/categories';

const CodeArena = dynamic(() => import('@/app/components/codearena/page'), {
  loading: () => <LoadingSpinner />,
  ssr: false,
});

const Page = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const selectedCategory = searchParams.get('category');

  const handleSprintSelect = (concept: string) => {
    console.log('Parent Page - Selected concept:', concept);
    router.push(`/?category=${concept}`);
  };

  const features = [
    { title: 'Interactive Code Editor', description: 'Write, test, and debug code in 10+ programming languages' },
    { title: 'Real-time Feedback', description: 'Get instant feedback on your code submissions' },
    { title: 'Progress Tracking', description: 'Track your learning journey with detailed statistics' },
    { title: 'Structured Learning Path', description: 'Follow curated paths from basics to advanced topics' }
  ];

  useEffect(() => {
    const handleCategorySelect = (event: CustomEvent) => {
      router.push(`/?category=${event.detail}`);
    };

    window.addEventListener('categorySelect', handleCategorySelect as EventListener);
    return () => {
      window.removeEventListener('categorySelect', handleCategorySelect as EventListener);
    };
  }, []);

  if (selectedCategory) {
    return (
      <>
        <Heading />
        <CodeArena category={selectedCategory} onBack={() => {
          router.push('/');
        }} />
      </>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Heading />
      
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <div className="text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Be the{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-300 to-[#4f4ee5] animate-gradient">
              GOAT Coder
            </span>{' '}
            - Master Coding Through Practice!
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
        {/* Program Wise Practice Section */}
        {/* <ProgramWisePractice onSprintSelect={handleSprintSelect} /> */}

        <h3 className="text-2xl font-bold text-gray-900 mb-8">Problem Categories</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {categories.map((category, index) => (
            <div
              key={index}
              onClick={() => handleSprintSelect(category.value)}
              className="bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow text-left cursor-pointer hover:bg-gray-50"
            >
              <div className="flex items-center gap-4 mb-4">
                {category.icon}
                <h4 className="text-lg font-semibold">{category.name}</h4>
              </div>
              <p className="text-gray-600">{category.count}</p>
            </div>
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