import React, { useState } from 'react'
import { Header } from './components/Header'
import { FileUploader } from './components/FileUploader'
import { ResultsViewer } from './components/ResultsViewer'
import { ErrorAlert } from './components/ErrorAlert'
import { QuestionnaireResponse } from './types/questionnaire'

export const App: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<QuestionnaireResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [currentFilename, setCurrentFilename] = useState<string>('')

  const handleProcessFile = async (file: File) => {
    setLoading(true)
    setError(null)
    setResult(null)
    setCurrentFilename(file.name)

    const formData = new FormData()
    formData.append('file', file)

    const apiUrl = import.meta.env.VITE_API_URL
      ? `${import.meta.env.VITE_API_URL}/api/extract`
      : '/api/extract'

    try {
      const response = await fetch(apiUrl, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        let errorDetail = 'No fue posible extraer el cuestionario.'
        try {
          const errorJson = await response.json()
          if (errorJson.detail) {
            errorDetail =
              typeof errorJson.detail === 'string'
                ? errorJson.detail
                : JSON.stringify(errorJson.detail)
          }
        } catch {
          errorDetail = `Error ${response.status}: ${response.statusText}`
        }
        throw new Error(errorDetail)
      }

      const data: QuestionnaireResponse = await response.json()
      setResult(data)
    } catch (err: any) {
      setError(err.message || 'Error inesperado durante el procesamiento.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col antialiased">
      <Header />

      <main className="flex-1 max-w-5xl w-full mx-auto px-4 sm:px-6 py-8 space-y-6">
        <FileUploader onProcess={handleProcessFile} isLoading={loading} />

        {error && <ErrorAlert message={error} onRetry={() => setError(null)} />}

        {result && <ResultsViewer data={result} filename={currentFilename} />}
      </main>

      <footer className="border-t border-slate-200/80 bg-white py-4 text-center text-xs text-slate-500">
        Giunti Psychometrics &middot; Plataforma de digitalización de instrumentos psicométricos
      </footer>
    </div>
  )
}

export default App
