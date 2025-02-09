"use client"

import { Button } from "@/components/ui/button"
import { ThumbsUp, ThumbsDown, Flag, Maximize2, Minimize2 } from "lucide-react"
import { cn } from "@/lib/utils"
import { useState, useEffect } from "react"

interface CommonCodeArenaProps {
  className?: string;
}

export function CommonCodeArena({ className }: CommonCodeArenaProps) {
  const [isFullscreen, setIsFullscreen] = useState(false);

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(document.fullscreenElement !== null);
      // Toggle header visibility
      const header = document.getElementById('main-header');
      if (header) {
        header.style.display = document.fullscreenElement ? 'none' : 'block';
      }
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
    };
  }, []);

  const toggleFullScreen = async () => {
    try {
      if (!isFullscreen) {
        // Target the code-arena container instead of document
        const codeArena = document.getElementById('code-arena-container');
        if (codeArena?.requestFullscreen) {
          await codeArena.requestFullscreen();
        } else if ((codeArena as any)?.webkitRequestFullscreen) {
          await (codeArena as any).webkitRequestFullscreen();
        } else if ((codeArena as any)?.msRequestFullscreen) {
          await (codeArena as any).msRequestFullscreen();
        }
      } else {
        if (document.exitFullscreen) {
          await document.exitFullscreen();
        } else if ((document as any).webkitExitFullscreen) {
          await (document as any).webkitExitFullscreen();
        } else if ((document as any).msExitFullscreen) {
          await (document as any).msExitFullscreen();
        }
      }
    } catch (error) {
      console.error('Error toggling fullscreen:', error);
    }
  };

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
        title={isFullscreen ? "Exit Full Screen" : "Full Screen"}
        onClick={toggleFullScreen}
      >
        {isFullscreen ? (
          <Minimize2 className="h-4 w-4" />
        ) : (
          <Maximize2 className="h-4 w-4" />
        )}
      </Button>
    </div>
  )
} 