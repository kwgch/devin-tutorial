import React, { useState } from 'react';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '../components/ui/card';
import { createDiaryEntry } from '../api';
import { DiaryEntry } from '../types';

interface DiaryEntryFormProps {
  onEntryCreated: (entry: DiaryEntry) => void;
}

export function DiaryEntryForm({ onEntryCreated }: DiaryEntryFormProps) {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!content.trim()) {
      setError('日記の内容を入力してください。');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const newEntry = await createDiaryEntry({ content });
      setContent('');
      onEntryCreated(newEntry);
    } catch (err) {
      setError('日記の保存中にエラーが発生しました。もう一度お試しください。');
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>新しい日記を書く</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <Textarea
            placeholder="今日の出来事を日本語で書いてください..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={6}
            className="resize-none"
          />
          {error && <p className="text-red-500 mt-2 text-sm">{error}</p>}
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? '保存中...' : '保存して翻訳'}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
