import React, { useState } from 'react';
import { DiaryEntry, FavoriteExpression } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Separator } from '../components/ui/separator';
import { Badge } from '../components/ui/badge';
import { addFavoriteExpression } from '../api';
import { format } from 'date-fns';
import { ja } from 'date-fns/locale';

interface DiaryEntryDetailProps {
  entry: DiaryEntry;
  onClose: () => void;
  onExpressionAdded: () => void;
}

export function DiaryEntryDetail({ entry, onClose, onExpressionAdded }: DiaryEntryDetailProps) {
  const [selectedJapanese, setSelectedJapanese] = useState('');
  const [selectedEnglish, setSelectedEnglish] = useState('');
  const [note, setNote] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  const handleJapaneseTextSelect = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim()) {
      setSelectedJapanese(selection.toString().trim());
    }
  };

  const handleEnglishTextSelect = () => {
    const selection = window.getSelection();
    if (selection && selection.toString().trim()) {
      setSelectedEnglish(selection.toString().trim());
    }
  };

  const handleSaveExpression = async () => {
    if (!selectedJapanese || !selectedEnglish) {
      alert('日本語と英語の両方のテキストを選択してください。');
      return;
    }

    setIsSaving(true);
    try {
      await addFavoriteExpression(entry.id, selectedJapanese, selectedEnglish, note);
      setSelectedJapanese('');
      setSelectedEnglish('');
      setNote('');
      onExpressionAdded();
      alert('表現が保存されました！');
    } catch (err) {
      console.error('Failed to save expression:', err);
      alert('表現の保存中にエラーが発生しました。');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle>
            {format(new Date(entry.created_at), 'yyyy年MM月dd日 HH:mm', { locale: ja })}
          </CardTitle>
          <Button variant="outline" onClick={onClose}>
            戻る
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h3 className="text-lg font-medium mb-2">日本語</h3>
          <div 
            className="p-4 bg-gray-50 rounded-md whitespace-pre-wrap"
            onMouseUp={handleJapaneseTextSelect}
          >
            {entry.content}
          </div>
        </div>

        <Separator />

        <div>
          <h3 className="text-lg font-medium mb-2">英語</h3>
          <div 
            className="p-4 bg-gray-50 rounded-md whitespace-pre-wrap"
            onMouseUp={handleEnglishTextSelect}
          >
            {entry.translated_content}
          </div>
        </div>

        <Separator />

        <div>
          <h3 className="text-lg font-medium mb-4">お気に入りの表現を保存</h3>
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium mb-1">選択した日本語</label>
              <div className="p-2 border rounded-md min-h-10 bg-gray-50">
                {selectedJapanese || '日本語のテキストを選択してください'}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">選択した英語</label>
              <div className="p-2 border rounded-md min-h-10 bg-gray-50">
                {selectedEnglish || '英語のテキストを選択してください'}
              </div>
            </div>
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium mb-1">メモ (オプション)</label>
            <textarea
              className="w-full p-2 border rounded-md"
              value={note}
              onChange={(e) => setNote(e.target.value)}
              placeholder="この表現についてのメモを書いてください..."
              rows={2}
            />
          </div>
          <Button 
            onClick={handleSaveExpression} 
            disabled={!selectedJapanese || !selectedEnglish || isSaving}
          >
            {isSaving ? '保存中...' : '表現を保存'}
          </Button>
        </div>

        {entry.favorite_expressions.length > 0 && (
          <>
            <Separator />
            <div>
              <h3 className="text-lg font-medium mb-2">保存した表現</h3>
              <div className="space-y-2">
                {entry.favorite_expressions.map((expr, index) => (
                  <div key={index} className="p-3 border rounded-md">
                    <div className="flex flex-wrap gap-2 mb-2">
                      <Badge variant="outline" className="bg-blue-50">
                        {expr.japanese_text}
                      </Badge>
                      <Badge variant="outline" className="bg-green-50">
                        {expr.english_text}
                      </Badge>
                    </div>
                    {expr.note && <p className="text-sm text-gray-600">{expr.note}</p>}
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
