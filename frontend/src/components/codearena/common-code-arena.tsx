"use client"

import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown, Flag, Maximize2 } from "lucide-react"
import { cn } from "@/lib/utils"

interface CommonCodeArenaProps {
  className?: string;
}

export function CommonCodeArena({ className }: CommonCodeArenaProps) {
  return (
    <div className={cn(
      "flex items-center gap-2 bg-white/50 backdrop-blur-sm p-2 rounded-lg shadow-sm border border-gray-200",
      className
    )}>
      <Button
        variant="ghost"
        size="sm"
        className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
        title="Like"
      >
        <ThumbsUp className="h-4 w-4" />
      </Button>

      <Button
        variant="ghost"
        size="sm"
        className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
        title="Dislike"
      >
        <ThumbsDown className="h-4 w-4" />
      </Button>

      <div className="w-px h-4 bg-gray-200" /> {/* Separator */}

      <Button
        variant="ghost"
        size="sm"
        className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
        title="Report"
      >
        <Flag className="h-4 w-4" />
      </Button>

      <Button
        variant="ghost"
        size="sm"
        className="text-gray-600 hover:text-gray-900 hover:bg-gray-100"
        title="Full Screen"
      >
        <Maximize2 className="h-4 w-4" />
      </Button>
    </div>
  )
} 