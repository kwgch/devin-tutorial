import React, { useState, useEffect } from 'react';
import { fetchDiaryEntries, deleteDiaryEntry } from '../api';
import { DiaryEntry } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Separator } from '../components/ui/separator';
import { formatDistanceToNow } from 'date-fns';
import { ja } from 'date-fns/locale';

interface DiaryEntryListProps {
  onEntrySelect: (entry: DiaryEntry) => void;
  refreshTrigger: number;
}

export function DiaryEntryList({ onEntrySelect, refreshTrigger }: DiaryEntryListProps) {
  const [entries, setEntries] = useState<DiaryEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadEntries = async () => {
      setLoading(true);
      setError(null);
      
      try {
        const data = await fetchDiaryEntries();
        setEntries(data.sort((a, b) => 
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        ));
      } catch (err) {
        setError('日記の読み込み中にエラーが発生しました。');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadEntries();
  }, [refreshTrigger]);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!window.confirm('この日記を削除してもよろしいですか？')) {
      return;
    }
    
    try {
      await deleteDiaryEntry(id);
      setEntries(entries.filter(entry => entry.id !== id));
    } catch (err) {
      console.error('Failed to delete entry:', err);
      alert('日記の削除中にエラーが発生しました。');
    }
  };

  if (loading) {
    return <div className="text-center py-8">読み込み中...</div>;
  }

  if (error) {
    return <div className="text-red-500 text-center py-8">{error}</div>;
  }

  if (entries.length === 0) {
    return <div className="text-center py-8">日記がまだありません。新しい日記を書いてみましょう！</div>;
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">日記一覧</h2>
      {entries.map(entry => (
        <Card 
          key={entry.id} 
          className="cursor-pointer hover:bg-gray-50 transition-colors"
          onClick={() => onEntrySelect(entry)}
        >
          <CardHeader className="pb-2">
            <div className="flex justify-between items-center">
              <CardTitle className="text-lg">
                {formatDistanceToNow(new Date(entry.created_at), { addSuffix: true, locale: ja })}
              </CardTitle>
              <Button 
                variant="destructive" 
                size="sm"
                onClick={(e) => handleDelete(entry.id, e)}
              >
                削除
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <p className="line-clamp-3 text-gray-700">{entry.content}</p>
            <Separator className="my-2" />
            <p className="line-clamp-3 text-gray-500 italic">{entry.translated_content}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
