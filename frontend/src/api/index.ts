import { DiaryEntry, DiaryEntryCreate, FavoriteExpression } from '../types';

const API_URL = 'http://localhost:8000/api';

export const fetchDiaryEntries = async (): Promise<DiaryEntry[]> => {
  const response = await fetch(`${API_URL}/diary`);
  if (!response.ok) {
    throw new Error('Failed to fetch diary entries');
  }
  return response.json();
};

export const fetchDiaryEntry = async (id: string): Promise<DiaryEntry> => {
  const response = await fetch(`${API_URL}/diary/${id}`);
  if (!response.ok) {
    throw new Error('Failed to fetch diary entry');
  }
  return response.json();
};

export const createDiaryEntry = async (entry: DiaryEntryCreate): Promise<DiaryEntry> => {
  const response = await fetch(`${API_URL}/diary`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(entry),
  });
  if (!response.ok) {
    throw new Error('Failed to create diary entry');
  }
  return response.json();
};

export const updateDiaryEntry = async (id: string, entry: DiaryEntryCreate): Promise<DiaryEntry> => {
  const response = await fetch(`${API_URL}/diary/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(entry),
  });
  if (!response.ok) {
    throw new Error('Failed to update diary entry');
  }
  return response.json();
};

export const deleteDiaryEntry = async (id: string): Promise<void> => {
  const response = await fetch(`${API_URL}/diary/${id}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete diary entry');
  }
};

export const addFavoriteExpression = async (
  entryId: string,
  japaneseText: string,
  englishText: string,
  note?: string
): Promise<FavoriteExpression> => {
  const response = await fetch(`${API_URL}/diary/${entryId}/favorite`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      japanese_text: japaneseText,
      english_text: englishText,
      note,
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to add favorite expression');
  }
  return response.json();
};

export const fetchFavoriteExpressions = async (): Promise<FavoriteExpression[]> => {
  const response = await fetch(`${API_URL}/favorites`);
  if (!response.ok) {
    throw new Error('Failed to fetch favorite expressions');
  }
  return response.json();
};
