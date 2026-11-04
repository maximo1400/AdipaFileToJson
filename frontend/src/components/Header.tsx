import React from 'react'
import { BrainCircuit } from 'lucide-react'

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-20">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center">
            <BrainCircuit className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="flex items-center space-x-2">
            <span className="font-bold text-slate-900 text-sm tracking-tight">
              Giunti Psychometrics
            </span>
            <span className="text-slate-300">|</span>
            <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full border border-indigo-100">
              Digitalizador
            </span>
          </div>
        </div>
      </div>
    </header>
  )
}
