export interface KB_list_RequestData {
  data: JSON,
  code: string
}

export interface KBRequestData {
  Type_item: "ollama" | "xinference",
  Model_item: string,
  KB_item: string,
  Top_K:Int8Array,
  Temprature:Int8Array,
  Query_content:string,
  KB_result:string,
  answer_content:string,
  code:string
}

export interface Type_list_RequestData {
  type_list: JSON,
  code: string
}
