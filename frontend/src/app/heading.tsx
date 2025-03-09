"use client"

import React from 'react';
import { Boxes, Puzzle, Network, TextCursor, CodeSquare, Code, Brain, LogIn } from 'lucide-react';

const Heading = () => {
  const categories = [
    { icon: <CodeSquare className="w-6 h-6" />, name: 'Programming Basics - Newbie', count: '250+ Problems', value: 'Basic Programming for Absolute Beginners' },
    { icon: <Code className="w-6 h-6" />, name: 'Programming Basics - Intermediate', count: '200+ Problems', value: 'Basic Programming for Intermediate Beginner - level programmers' },
    { icon: <TextCursor className="w-6 h-6" />, name: 'String Handling', count: '150+ Problems', value: 'String Handling' },
    { icon: <Network className="w-6 h-6" />, name: 'Data Structures', count: '200+ Problems', value: 'Data Structures' },
    { icon: <Brain className="w-6 h-6" />, name: 'Algorithms', count: '180+ Problems', value: 'Algorithms' },
    { icon: <Puzzle className="w-6 h-6" />, name: 'Problem Solving', count: '120+ Problems', value: 'Problem Solving' },
    { icon: <Boxes className="w-6 h-6" />, name: 'Array', count: '350+ Problems', value: 'Array' }
  ];

  return (
    <div id="main-header">
      <nav className="bg-white">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-indigo-600">CodeSpace Academy</h1>
          <div className="flex items-center gap-4">
            <button className="px-4 py-2 text-gray-600 hover:text-gray-900">Explore</button>
            <div className="relative group">
              <button className="px-4 py-2 text-gray-600 hover:text-gray-900">Practice</button>
              <div className="absolute w-full h-3 bottom-0 translate-y-full" />
              <div className="absolute hidden group-hover:block w-72 right-0 mt-[2px] py-2 bg-white rounded-lg shadow-xl z-50">
                {categories.map((category, index) => (
                  <button
                    key={index}
                    className="w-full px-4 py-2 text-left hover:bg-gray-100 flex items-center gap-3"
                    onClick={() => window.dispatchEvent(new CustomEvent('categorySelect', { detail: category.value }))}
                  >
                    {category.icon}
                    <div className="flex flex-col">
                      <span className="font-medium">{category.name}</span>
                      <span className="text-sm text-gray-500">{category.count}</span>
                    </div>
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
      <div className="h-[1px] bg-gray-200 w-full" />
    </div>
  );
};

export default Heading; 