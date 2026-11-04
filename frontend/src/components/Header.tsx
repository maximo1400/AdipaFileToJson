import React from 'react'
import { BrainCircuit } from 'lucide-react'

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-slate-200/80 sticky top-0 z-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-sm">
            <BrainCircuit className="w-5 h-5 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-900 text-sm tracking-tight">
                Giunti Psychometrics
              </span>
              <span className="text-slate-300">|</span>
              <span className="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full border border-indigo-100">
                Digitalizador
              </span>
            </div>
            <p className="text-[11px] text-slate-400 font-normal">
              Extracción y estructuración psicométrica automática
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-500 bg-slate-50 border border-slate-200 px-2.5 py-1.5 rounded-lg">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="font-medium text-slate-700">Sistema activo</span>
        </div>
      </div>
    </header>
  )
}
