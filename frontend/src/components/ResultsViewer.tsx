import React, { useState } from 'react'
import {
  Download,
  Copy,
  Check,
  Globe,
  ListOrdered,
  CheckCircle2,
} from 'lucide-react'
import { QuestionnaireResponse, ItemType } from '../types/questionnaire'

interface ResultsViewerProps {
  data: QuestionnaireResponse
  filename?: string
}

export const ResultsViewer: React.FC<ResultsViewerProps> = ({ data, filename }) => {
  const [activeTab, setActiveTab] = useState<'items' | 'json'>('items')
  const [copied, setCopied] = useState(false)

  const jsonString = JSON.stringify(data, null, 2)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(jsonString)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    const baseName = filename ? filename.replace(/\.[^/.]+$/, '') : 'cuestionario'
    a.href = url
    a.download = `${baseName}_estructurado.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const getTypeBadge = (tipo: ItemType) => {
    switch (tipo) {
      case 'escala_likert':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-purple-50 text-purple-700 border border-purple-200">
            Escala Likert
          </span>
        )
      case 'seleccion_multiple':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
            Selección Múltiple
          </span>
        )
      case 'verdadero_falso':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200">
            Verdadero / Falso
          </span>
        )
      case 'desarrollo':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Desarrollo
          </span>
        )
      case 'emparejamiento':
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-50 text-rose-700 border border-rose-200">
            Emparejamiento
          </span>
        )
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-700">
            {tipo}
          </span>
        )
    }
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
      {/* Top Header Summary */}
      <div className="px-6 py-5 border-b border-slate-200 bg-gradient-to-b from-white to-slate-50/50">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 mb-1">
              <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100">
                Cuestionario digitalizado
              </span>
            </div>
            <h2 className="text-xl font-bold text-slate-900 tracking-tight">
              {data.titulo}
            </h2>
            <div className="flex items-center space-x-3 text-xs text-slate-500 mt-1">
              <span className="inline-flex items-center space-x-1">
                <Globe className="w-3.5 h-3.5 text-slate-400" />
                <span>Idioma: <strong className="text-slate-800 uppercase">{data.idioma}</strong></span>
              </span>
              <span>·</span>
              <span className="inline-flex items-center space-x-1">
                <ListOrdered className="w-3.5 h-3.5 text-slate-400" />
                <span>Total de preguntas: <strong className="text-slate-800">{data.total_items}</strong></span>
              </span>
            </div>
          </div>

          {/* Action CTAs & View Switcher */}
          <div className="flex items-center flex-wrap gap-2">
            <div className="flex bg-slate-100 border border-slate-200 p-1 rounded-lg text-xs font-medium">
              <button
                onClick={() => setActiveTab('items')}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  activeTab === 'items'
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                Vista de preguntas
              </button>
              <button
                onClick={() => setActiveTab('json')}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  activeTab === 'json'
                    ? 'bg-white text-slate-900 shadow-xs font-semibold'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                JSON Schema
              </button>
            </div>

            <button
              onClick={handleCopy}
              className="px-3 py-1.5 border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium rounded-lg shadow-2xs transition-colors flex items-center space-x-1.5"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-slate-500" />}
              <span>{copied ? 'Copiado' : 'Copiar'}</span>
            </button>
            <button
              onClick={handleDownload}
              className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium rounded-lg shadow-xs transition-colors flex items-center space-x-1.5"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Descargar JSON</span>
            </button>
          </div>
        </div>
      </div>

      {/* Content Area */}
      {activeTab === 'items' ? (
        data.items.length === 0 ? (
          <div className="p-12 text-center text-slate-500 text-sm">
            No se detectaron preguntas ni ítems estructurados en el documento analizado.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {data.items.map((item) => (
              <div key={item.numero} className="p-5 sm:p-6 hover:bg-slate-50/60 transition-colors">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start space-x-3.5">
                    <span className="w-8 h-8 rounded-lg bg-slate-100 border border-slate-200 text-slate-700 font-bold text-xs flex items-center justify-center shrink-0">
                      {String(item.numero).padStart(2, '0')}
                    </span>
                    <div>
                      <h3 className="text-sm font-semibold text-slate-900 leading-snug">
                        {item.enunciado}
                      </h3>
                    </div>
                  </div>
                  <div className="shrink-0">{getTypeBadge(item.tipo)}</div>
                </div>

                {/* Likert Scale View */}
                {item.tipo === 'escala_likert' && item.alternativas && item.alternativas.length > 0 && (
                  <div className="mt-4 ml-11">
                    <div className="flex flex-wrap items-center gap-2">
                      {item.alternativas.map((alt, idx) => (
                        <div
                          key={idx}
                          className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-white border border-slate-200 shadow-2xs hover:border-purple-300 hover:bg-purple-50/30 transition-colors"
                        >
                          <span className="w-5 h-5 rounded-full bg-purple-100 text-purple-700 font-bold text-[11px] flex items-center justify-center">
                            {alt.valor}
                          </span>
                          <span className="text-xs font-medium text-slate-700">{alt.texto}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Multiple Choice / True False View */}
                {(item.tipo === 'seleccion_multiple' || item.tipo === 'verdadero_falso') &&
                  item.alternativas && item.alternativas.length > 0 && (
                    <div className="mt-4 ml-11 grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {item.alternativas.map((alt, idx) => {
                        const isCorrect =
                          item.respuesta_correcta !== null &&
                          String(item.respuesta_correcta).trim().toUpperCase() ===
                            String(alt.valor).trim().toUpperCase()

                        return (
                          <div
                            key={idx}
                            className={`flex items-center justify-between px-3.5 py-2 rounded-lg border text-xs transition-colors ${
                              isCorrect
                                ? 'bg-emerald-50/80 border-emerald-300 text-emerald-950 font-medium'
                                : 'bg-white border-slate-200 text-slate-700'
                            }`}
                          >
                            <div className="flex items-center space-x-2.5">
                              <span
                                className={`w-6 h-6 rounded-md font-bold text-xs flex items-center justify-center shrink-0 ${
                                  isCorrect
                                    ? 'bg-emerald-600 text-white'
                                    : 'bg-slate-100 text-slate-600 border border-slate-200'
                                }`}
                              >
                                {alt.valor}
                              </span>
                              <span>{alt.texto}</span>
                            </div>
                            {isCorrect && (
                              <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                            )}
                          </div>
                        )
                      })}
                    </div>
                  )}

                {/* Matching items view */}
                {item.tipo === 'emparejamiento' && item.alternativas && item.alternativas.length > 0 && (
                  <div className="mt-4 ml-11 space-y-2">
                    <div className="text-xs font-medium text-slate-500 mb-1">
                      Elementos o relaciones de emparejamiento:
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {item.alternativas.map((alt, idx) => (
                        <div
                          key={idx}
                          className="flex items-center space-x-2.5 px-3.5 py-2 rounded-lg bg-rose-50/50 border border-rose-200 text-xs text-rose-950"
                        >
                          <span className="w-6 h-6 rounded-md font-bold text-xs flex items-center justify-center shrink-0 bg-rose-100 text-rose-700 border border-rose-300">
                            {alt.valor}
                          </span>
                          <span className="font-medium text-slate-800">{alt.texto}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Open-ended items */}
                {item.tipo === 'desarrollo' && (
                  <div className="mt-3 ml-11 p-3 rounded-lg bg-slate-50 border border-dashed border-slate-200 text-xs text-slate-500">
                    Respuesta abierta del evaluado.
                  </div>
                )}

                {/* Correct answer indicator */}
                {item.respuesta_correcta !== null && item.tipo !== 'seleccion_multiple' && item.tipo !== 'verdadero_falso' && (
                  <div className="mt-3 ml-11 inline-flex items-center space-x-1.5 px-2.5 py-1 rounded bg-emerald-50 text-emerald-800 text-xs font-medium border border-emerald-200">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Respuesta correcta: <strong>{String(item.respuesta_correcta)}</strong></span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )
      ) : (
        <div className="p-4 bg-slate-950">
          <pre className="p-4 rounded-lg bg-slate-900 text-slate-100 text-xs font-mono overflow-x-auto max-h-[550px] border border-slate-800 leading-relaxed">
            <code>{jsonString}</code>
          </pre>
        </div>
      )}
    </div>
  )
}
