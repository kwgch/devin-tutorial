import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { Button } from './ui/button';

interface GoogleLoginButtonProps {
  onSuccess: (token: string) => void;
  onError: () => void;
}

export function GoogleLoginButton({ onSuccess, onError }: GoogleLoginButtonProps) {
  return (
    <div className="flex flex-col items-center space-y-4">
      <h2 className="text-xl font-semibold">Googleアカウントでログイン</h2>
      <p className="text-gray-600 text-center mb-4">
        パラレルダイアリーを使用するには、Googleアカウントでログインしてください。
      </p>
      <GoogleLogin
        onSuccess={(credentialResponse) => {
          if (credentialResponse.credential) {
            onSuccess(credentialResponse.credential);
          }
        }}
        onError={() => {
          console.error('Login Failed');
          onError();
        }}
        useOneTap
      />
    </div>
  );
}
