/**
 * AuthContext.tsx
 *
 * Authentication context for ExecuMind AI.
 *
 * Responsibilities:
 * - Manage authentication session
 * - Login
 * - Logout
 * - Restore session
 */

import {
    createContext,
    ReactNode,
    useContext,
    useEffect,
    useState,
} from "react";

import AuthService, {
    LoginRequest,
} from "./authService";

interface AuthUser {
    username: string;
    token: string;
}

interface AuthContextType {

    user: AuthUser | null;

    isAuthenticated: boolean;

    login(
        credentials: LoginRequest
    ): Promise<void>;

    logout(): void;
}

const AuthContext = createContext<AuthContextType | undefined>(
    undefined
);

interface Props {
    children: ReactNode;
}

export function AuthProvider({
    children,
}: Props) {

    const [user, setUser] =
        useState<AuthUser | null>(null);

    /**
     * Restore authentication session.
     */
    useEffect(() => {

        const token = AuthService.getToken();

        const username =
            localStorage.getItem("username");

        if (token && username) {

            setUser({
                username,
                token,
            });

        }

    }, []);

    /**
     * Login administrator.
     */
    async function login(
        credentials: LoginRequest
    ): Promise<void> {

        const response =
            await AuthService.login(credentials);

        AuthService.saveToken(
            response.access_token
        );

        localStorage.setItem(
            "username",
            response.user.username
        );

        setUser({
            username: response.user.username,
            token: response.access_token,
        });
    }

    /**
     * Logout administrator.
     */
    function logout() {

        AuthService.logout();

        localStorage.removeItem(
            "username"
        );

        setUser(null);
    }

    return (

        <AuthContext.Provider
            value={{
                user,
                isAuthenticated:
                    user !== null,
                login,
                logout,
            }}
        >

            {children}

        </AuthContext.Provider>

    );
}

export function useAuth() {

    const context =
        useContext(AuthContext);

    if (!context) {

        throw new Error(
            "useAuth must be used inside AuthProvider."
        );
    }

    return context;
}