import React, { useRef, useState } from 'react'
import { UploadCloud, X, AlertCircle, ArrowRight, Loader2 } from 'lucide-react'

interface FileUploaderProps {
  onProcess: (file: File) => Promise<void>
  isLoading: boolean
}

export const FileUploader: React.FC<FileUploaderProps> = ({ onProcess, isLoading }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [dragActive, setDragActive] = useState(false)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const allowedExtensions = ['.pdf', '.docx', '.xlsx']

  const getFileBadge = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase()
    if (ext === 'pdf') {
      return (
        <span className="px-2 py-0.5 text-[11px] font-bold bg-rose-100 text-rose-700 rounded border border-rose-200 uppercase">
          PDF
        </span>
      )
    }
    if (ext === 'docx') {
      return (
        <span className="px-2 py-0.5 text-[11px] font-bold bg-blue-100 text-blue-700 rounded border border-blue-200 uppercase">
          DOCX
        </span>
      )
    }
    if (ext === 'xlsx') {
      return (
        <span className="px-2 py-0.5 text-[11px] font-bold bg-emerald-100 text-emerald-700 rounded border border-emerald-200 uppercase">
          XLSX
        </span>
      )
    }
    return null
  }

  const validateAndSetFile = (file: File) => {
    setErrorMsg(null)
    const ext = '.' + file.name.split('.').pop()?.toLowerCase()
    if (!allowedExtensions.includes(ext)) {
      setErrorMsg('Formato no soportado. Selecciona un archivo PDF, DOCX o XLSX.')
      return
    }
    if (file.size > 15 * 1024 * 1024) {
      setErrorMsg('El archivo supera el límite de 15 MB.')
      return
    }
    setSelectedFile(file)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragActive(false)
    if (e.dataTransfer.files?.[0]) {
      validateAndSetFile(e.dataTransfer.files[0])
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!selectedFile) return
    onProcess(selectedFile)
  }

  const formatSize = (bytes: number) => {
    return bytes < 1024 * 1024
      ? `${(bytes / 1024).toFixed(0)} KB`
      : `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Dropzone */}
        <div
          onDragOver={(e) => {
            e.preventDefault()
            setDragActive(true)
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
            dragActive
              ? 'border-indigo-500 bg-indigo-50/50 scale-[0.99]'
              : selectedFile
              ? 'border-indigo-300 bg-indigo-50/20'
              : 'border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-300'
          }`}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.docx,.xlsx"
            onChange={(e) => e.target.files?.[0] && validateAndSetFile(e.target.files[0])}
            className="hidden"
          />

          {!selectedFile ? (
            <div className="flex flex-col items-center justify-center space-y-2">
              <div className="w-10 h-10 rounded-full bg-white shadow-sm border border-slate-200 flex items-center justify-center text-slate-500">
                <UploadCloud className="w-5 h-5 text-indigo-600" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-800">
                  Arrastra un documento o haz clic para seleccionarlo
                </p>
                <div className="flex items-center justify-center space-x-2 mt-2">
                  <span className="text-[11px] font-semibold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                    PDF
                  </span>
                  <span className="text-[11px] font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                    Word (.docx)
                  </span>
                  <span className="text-[11px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                    Excel (.xlsx)
                  </span>
                  <span className="text-xs text-slate-400">· hasta 15 MB</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-between p-3 bg-white rounded-lg border border-slate-200 max-w-lg mx-auto shadow-sm">
              <div className="flex items-center space-x-3 text-left truncate">
                {getFileBadge(selectedFile.name)}
                <div className="truncate">
                  <span className="text-sm font-semibold text-slate-900 block truncate">
                    {selectedFile.name}
                  </span>
                  <span className="text-xs text-slate-400">
                    {formatSize(selectedFile.size)}
                  </span>
                </div>
              </div>
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation()
                  setSelectedFile(null)
                  if (inputRef.current) inputRef.current.value = ''
                }}
                className="p-1 text-slate-400 hover:text-rose-600 rounded transition-colors"
                title="Quitar archivo"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {errorMsg && (
          <div className="flex items-center space-x-2 text-rose-600 text-xs bg-rose-50 p-2.5 rounded-lg border border-rose-200">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Action button */}
        <div className="flex justify-end pt-1">
          <button
            type="submit"
            disabled={!selectedFile || isLoading}
            className={`px-6 py-2.5 text-sm font-semibold rounded-lg transition-all flex items-center justify-center space-x-2 shadow-sm ${
              !selectedFile || isLoading
                ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-indigo-100 hover:shadow-md'
            }`}
          >
            {isLoading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Extrayendo estructura...</span>
              </>
            ) : (
              <>
                <span>Digitalizar cuestionario</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  )
}
