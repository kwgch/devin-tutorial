import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { DiaryEntryForm } from '../components/DiaryEntryForm';
import { DiaryEntryList } from '../components/DiaryEntryList';
import { DiaryEntryDetail } from '../components/DiaryEntryDetail';
import { FavoriteExpressions } from '../components/FavoriteExpressions';
import { fetchFavoriteExpressions } from '../api';
import { DiaryEntry, FavoriteExpression } from '../types';
import { Button } from '../components/ui/button';

export function DiaryApp() {
  const { user, logout } = useAuth();
  const [selectedEntry, setSelectedEntry] = useState<DiaryEntry | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [favoriteExpressions, setFavoriteExpressions] = useState<FavoriteExpression[]>([]);

  useEffect(() => {
    const loadFavorites = async () => {
      try {
        const data = await fetchFavoriteExpressions();
        setFavoriteExpressions(data);
      } catch (err) {
        console.error('Failed to load favorite expressions:', err);
      }
    };

    loadFavorites();
  }, [refreshTrigger]);

  const handleEntryCreated = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleExpressionAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <header className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-3xl font-bold">パラレルダイアリー</h1>
          <div className="flex items-center gap-4">
            {user && (
              <>
                <div className="flex items-center gap-2">
                  {user.picture && (
                    <img 
                      src={user.picture} 
                      alt={user.name || 'User'} 
                      className="w-8 h-8 rounded-full"
                    />
                  )}
                  <span className="text-sm font-medium">{user.name || user.email}</span>
                </div>
                <Button variant="outline" size="sm" onClick={logout}>
                  ログアウト
                </Button>
              </>
            )}
          </div>
        </div>
        <p className="text-gray-600 text-center">
          日本語で日記を書くと、英語に自動翻訳されます。お気に入りの表現も保存できます。
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-2">
          {selectedEntry ? (
            <DiaryEntryDetail
              entry={selectedEntry}
              onClose={() => setSelectedEntry(null)}
              onExpressionAdded={handleExpressionAdded}
            />
          ) : (
            <div className="space-y-8">
              <DiaryEntryForm onEntryCreated={handleEntryCreated} />
              <DiaryEntryList
                onEntrySelect={setSelectedEntry}
                refreshTrigger={refreshTrigger}
              />
            </div>
          )}
        </div>
        
        <div>
          <FavoriteExpressions expressions={favoriteExpressions} />
        </div>
      </div>
    </div>
  );
}
