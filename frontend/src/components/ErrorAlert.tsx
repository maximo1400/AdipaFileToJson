import React from 'react'
import { AlertCircle } from 'lucide-react'

interface ErrorAlertProps {
  message: string
  onRetry?: () => void
}

export const ErrorAlert: React.FC<ErrorAlertProps> = ({ message, onRetry }) => {
  return (
    <div className="border border-rose-200 bg-rose-50/60 rounded-md p-4 flex items-start justify-between gap-3 text-xs text-rose-800">
      <div className="flex items-start space-x-2">
        <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
        <span className="leading-relaxed">{message}</span>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="underline font-medium hover:text-rose-950 shrink-0"
        >
          Reintentar
        </button>
      )}
    </div>
  )
}
