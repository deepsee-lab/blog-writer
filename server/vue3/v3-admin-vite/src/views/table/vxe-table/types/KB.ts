
export interface New_KB {
  KB_name: string,
  desc: string,
  vector_name: string,
  embedding_model_name:string,
  code:string
}

export interface vector_list_RequestData {
  data: JSON,
  code: string,
  message:string
}

export interface embedding_list_RequestData {
  data: JSON,
  code: string,
  message:string
}