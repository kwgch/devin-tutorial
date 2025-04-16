import React, { useState } from 'react';
import { GoogleLoginButton } from '../components/GoogleLoginButton';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';

export function LoginPage() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const handleLoginSuccess = (token: string) => {
    login(token);
  };

  const handleLoginError = () => {
    setError('ログインに失敗しました。もう一度お試しください。');
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">パラレルダイアリー</CardTitle>
        </CardHeader>
        <CardContent>
          <GoogleLoginButton 
            onSuccess={handleLoginSuccess} 
            onError={handleLoginError} 
          />
          {error && (
            <p className="text-red-500 text-center mt-4">{error}</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
