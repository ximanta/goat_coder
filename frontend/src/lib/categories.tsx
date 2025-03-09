import { CodeSquare, TextCursor } from 'lucide-react';

export interface Category {
  icon: JSX.Element;
  name: string;
  count: string;
  value: string;
}

export const categories: Category[] = [
  { icon: <CodeSquare className="w-6 h-6" />, name: 'Programming Basics - Newbie', count: '250+ Problems', value: 'basic programming absolute beginners' },
  { icon: <TextCursor className="w-6 h-6" />, name: 'String Handling', count: '150+ Problems', value: 'array search' },
  { icon: <CodeSquare className="w-6 h-6" />, name: 'Data Structures', count: '250+ Problems', value: 'data structures' },
];

export function getCategoryDisplayName(value: string): string {
  const category = categories.find(cat => cat.value === value);
  return category?.name || value;
}
