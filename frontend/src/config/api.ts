/**
 * API設定を一元管理するモジュール
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const AUTH_API_URL = API_BASE_URL;

export const DIARY_API_URL = `${API_BASE_URL}/api`;
