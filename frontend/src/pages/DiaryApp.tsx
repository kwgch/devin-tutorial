import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { DiaryEntryForm } from '../components/DiaryEntryForm';
import { DiaryEntryList } from '../components/DiaryEntryList';
import { DiaryEntryDetail } from '../components/DiaryEntryDetail';
import { FavoriteExpressions } from '../components/FavoriteExpressions';
import { MobileNavigation } from '../components/MobileNavigation';
import { fetchFavoriteExpressions } from '../api';
import { DiaryEntry, FavoriteExpression } from '../types';
import { Button } from '../components/ui/button';

export function DiaryApp() {
  const { user, logout } = useAuth();
  const [selectedEntry, setSelectedEntry] = useState<DiaryEntry | null>(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [favoriteExpressions, setFavoriteExpressions] = useState<FavoriteExpression[]>([]);
  const [currentView, setCurrentView] = useState<string>('diary');

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

  const handleNavigate = (view: string) => {
    setCurrentView(view);
    if (selectedEntry) {
      setSelectedEntry(null);
    }
  };

  const renderContent = () => {
    if (selectedEntry) {
      return (
        <DiaryEntryDetail
          entry={selectedEntry}
          onClose={() => setSelectedEntry(null)}
          onExpressionAdded={handleExpressionAdded}
        />
      );
    }

    switch (currentView) {
      case 'diary':
        return <DiaryEntryForm onEntryCreated={handleEntryCreated} />;
      case 'entries':
        return (
          <DiaryEntryList
            onEntrySelect={setSelectedEntry}
            refreshTrigger={refreshTrigger}
          />
        );
      case 'favorites':
        return <FavoriteExpressions expressions={favoriteExpressions} />;
      default:
        return <DiaryEntryForm onEntryCreated={handleEntryCreated} />;
    }
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-5xl">
      <header className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <div className="flex items-center gap-2">
            <MobileNavigation 
              onNavigate={handleNavigate}
              currentView={currentView}
              userName={user?.name || user?.email}
              onLogout={logout}
            />
            <h1 className="text-3xl font-bold">パラレルダイアリー</h1>
          </div>
          <div className="hidden md:flex items-center gap-4">
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

      {/* Desktop navigation */}
      <div className="hidden md:flex mb-6 border-b">
        <Button
          variant={currentView === 'diary' ? 'default' : 'ghost'}
          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary"
          data-state={currentView === 'diary' ? 'active' : 'inactive'}
          onClick={() => handleNavigate('diary')}
        >
          日記を書く
        </Button>
        <Button
          variant={currentView === 'entries' ? 'default' : 'ghost'}
          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary"
          data-state={currentView === 'entries' ? 'active' : 'inactive'}
          onClick={() => handleNavigate('entries')}
        >
          日記一覧
        </Button>
        <Button
          variant={currentView === 'favorites' ? 'default' : 'ghost'}
          className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary"
          data-state={currentView === 'favorites' ? 'active' : 'inactive'}
          onClick={() => handleNavigate('favorites')}
        >
          お気に入りの表現
        </Button>
      </div>

      {/* Content area */}
      <div className="md:grid md:grid-cols-1 md:gap-8">
        <div className="md:col-span-1">
          {renderContent()}
        </div>
      </div>
    </div>
  );
}
