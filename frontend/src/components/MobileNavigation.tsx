import { useState } from 'react';
import { Menu } from 'lucide-react';
import { 
  Sheet, 
  SheetContent, 
  SheetHeader, 
  SheetTitle, 
  SheetTrigger 
} from '../components/ui/sheet';
import { Button } from '../components/ui/button';

interface MobileNavigationProps {
  onNavigate: (view: string) => void;
  currentView: string;
  userName?: string;
  onLogout: () => void;
}

export function MobileNavigation({ 
  onNavigate, 
  currentView, 
  userName, 
  onLogout 
}: MobileNavigationProps) {
  const [open, setOpen] = useState(false);
  
  const handleNavigate = (view: string) => {
    onNavigate(view);
    setOpen(false); // Close the menu after selection
  };
  
  const handleLogout = () => {
    onLogout();
    setOpen(false); // Close the menu after logout
  };
  
  return (
    <Sheet open={open} onOpenChange={setOpen}>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon" className="md:hidden">
          <Menu className="h-6 w-6" />
          <span className="sr-only">メニューを開く</span>
        </Button>
      </SheetTrigger>
      <SheetContent side="left">
        <SheetHeader>
          <SheetTitle>パラレルダイアリー</SheetTitle>
        </SheetHeader>
        <div className="py-4">
          {userName && (
            <div className="mb-4 pb-4 border-b">
              <p className="text-sm font-medium">{userName}</p>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={handleLogout} 
                className="mt-2 w-full justify-start"
              >
                ログアウト
              </Button>
            </div>
          )}
          <nav className="flex flex-col space-y-1">
            <Button
              variant={currentView === 'diary' ? 'default' : 'ghost'}
              className="justify-start"
              onClick={() => handleNavigate('diary')}
            >
              日記を書く
            </Button>
            <Button
              variant={currentView === 'entries' ? 'default' : 'ghost'}
              className="justify-start"
              onClick={() => handleNavigate('entries')}
            >
              日記一覧
            </Button>
            <Button
              variant={currentView === 'favorites' ? 'default' : 'ghost'}
              className="justify-start"
              onClick={() => handleNavigate('favorites')}
            >
              お気に入りの表現
            </Button>
          </nav>
        </div>
      </SheetContent>
    </Sheet>
  );
}
