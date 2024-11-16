
export interface KBRequestData {
  Type_item: "ollama" | "xinference",
  Model_item: string,
  Top_K:Int8Array,
  Temprature:Int8Array,
  max_time:string,
  code:string
}

export interface Type_list_RequestData {
  type_list: JSON,
  code: string
}

export interface Model_RequestData {
  data: JSON,
  code: string
}


