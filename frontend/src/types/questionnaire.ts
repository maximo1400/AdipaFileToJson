export type ItemType =
  | 'escala_likert'
  | 'seleccion_multiple'
  | 'verdadero_falso'
  | 'desarrollo'
  | 'emparejamiento'

export interface Option {
  valor: string | number
  texto: string
}

export interface QuestionnaireItem {
  numero: number
  enunciado: string
  tipo: ItemType
  alternativas: Option[]
  respuesta_correcta: string | number | null
}

export interface QuestionnaireResponse {
  titulo: string
  idioma: string
  total_items: number
  items: QuestionnaireItem[]
}

