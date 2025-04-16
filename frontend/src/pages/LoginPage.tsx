import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LoginForm } from '../components/auth/LoginForm';
import { RegisterForm } from '../components/auth/RegisterForm';

export function LoginPage() {
  const [showLogin, setShowLogin] = useState(true);
  const navigate = useNavigate();

  const handleSuccess = () => {
    navigate('/');
  };

  const handleSwitchToRegister = () => {
    setShowLogin(false);
  };

  const handleSwitchToLogin = () => {
    setShowLogin(true);
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      {showLogin ? (
        <LoginForm 
          onSuccess={handleSuccess} 
          onSwitchToRegister={handleSwitchToRegister} 
        />
      ) : (
        <RegisterForm 
          onSuccess={handleSuccess} 
          onSwitchToLogin={handleSwitchToLogin} 
        />
      )}
    </div>
  );
}
