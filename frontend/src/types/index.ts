export interface DiaryEntry {
  id: string;
  content: string;
  translated_content: string;
  created_at: string;
  updated_at: string | null;
  favorite_expressions: FavoriteExpression[];
}

export interface FavoriteExpression {
  japanese_text: string;
  english_text: string;
  note: string | null;
}

export interface DiaryEntryCreate {
  content: string;
}
