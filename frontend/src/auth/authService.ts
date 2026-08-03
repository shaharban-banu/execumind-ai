/**
 * authService.ts
 *
 * Authentication service.
 */

import api from "../lib/api";

export interface LoginRequest {
    username: string;
    password: string;
}

export interface AuthUser {
    username: string;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
    user: AuthUser;
}

class AuthService {

    async login(
        credentials: LoginRequest
    ): Promise<LoginResponse> {

        const response =
            await api.post<LoginResponse>(
                "/auth/login",
                credentials
            );

        return response.data;
    }

    saveToken(token: string): void {

        localStorage.setItem(
            "access_token",
            token
        );
    }

    getToken(): string | null {

        return localStorage.getItem(
            "access_token"
        );
    }

    logout(): void {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "username"
        );
    }
}

export default new AuthService();