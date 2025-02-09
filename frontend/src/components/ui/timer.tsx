"use client"

import { useState, useEffect } from "react"
import { Timer as TimerIcon, Pause, Play, RotateCcw, ChevronLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tooltip } from "@/components/ui/tooltip"

export function Timer() {
  const [isVisible, setIsVisible] = useState(false)
  const [isRunning, setIsRunning] = useState(false)
  const [time, setTime] = useState(0)

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null
    
    if (isRunning) {
      interval = setInterval(() => {
        setTime((prevTime) => prevTime + 1)
      }, 1000)
    }

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [isRunning])

  const formatTime = (seconds: number) => {
    const hrs = Math.floor(seconds / 3600)
    const mins = Math.floor((seconds % 3600) / 60)
    const secs = seconds % 60
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }

  const handleReset = () => {
    setTime(0)
    setIsRunning(false)
  }

  const handleTimerClick = () => {
    setIsVisible(true)
    setIsRunning(true)
  }

  return (
    <div className="flex items-center gap-2">
      {!isVisible ? (
        <Tooltip content="Start Timer">
          <Button
            variant="ghost"
            size="icon"
            className="h-9 w-9 text-gray-500 hover:text-gray-900"
            onClick={handleTimerClick}
          >
            <TimerIcon className="h-4 w-4" />
          </Button>
        </Tooltip>
      ) : (
        <div className="flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 rounded-md px-2 py-1">
          <Tooltip content="Hide Timer">
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 text-gray-500 hover:text-gray-900"
              onClick={() => setIsVisible(false)}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
          </Tooltip>

          <span className="font-mono text-sm text-gray-700 dark:text-gray-300 min-w-[80px]">
            {formatTime(time)}
          </span>

          <Tooltip content={isRunning ? 'Pause' : 'Resume'}>
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 text-gray-500 hover:text-gray-900"
              onClick={() => setIsRunning(!isRunning)}
            >
              {isRunning ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
            </Button>
          </Tooltip>

          <Tooltip content="Reset Timer">
            <Button
              variant="ghost"
              size="icon"
              className="h-7 w-7 text-gray-500 hover:text-gray-900"
              onClick={handleReset}
            >
              <RotateCcw className="h-4 w-4" />
            </Button>
          </Tooltip>
        </div>
      )}
    </div>
  )
} 