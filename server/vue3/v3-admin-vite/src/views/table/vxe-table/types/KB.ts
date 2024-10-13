
export interface New_KB {
  KB_name: string,
  desc: string,
  vector_name: string,
  embedding_model_name:string,
  code:string
}

export interface New_KB_doc {
  kb_id: string,
  doc_id: string,
  doc_name: string,
  doc_path:string,
  doc_content:string,
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

export interface file_list_RequestData {
  data: JSON,
  code: string,
  message:string
}

export interface file_base_list_RequestData {
  data: JSON,
  code: string,
  message:string
}