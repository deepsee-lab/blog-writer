export interface UploadFileResponse {
  message: string
  success: boolean
  data: object
  status: number
}

export interface IamgeDescRequest {
  images: string[]
  style?: string
  language?: string
  length?: string
  summary_length?: string
  temperature?: number
  type_name: string
  model_select: string
}
