/**
 * LoginPage.tsx
 *
 * Administrator login page for ExecuMind AI.
 */

import { useState } from "react";
import { Eye, EyeOff, Lock, User, Loader2 } from "lucide-react";

import { useAuth } from "../auth/AuthContext";
import { Logo } from "../components/layout/Sidebar";

export function LoginPage() {

    const { login } = useAuth();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const [showPassword, setShowPassword] =
        useState(false);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState("");

    async function handleSubmit(
        e: React.FormEvent
    ) {

        e.preventDefault();

        setError("");

        setLoading(true);

        try {

            await login({
                username,
                password,
            });

        } catch(error:any){

            if (error.response?.status === 401) {

                    setError("Invalid username or password.");

                } else {

                    setError(
                        "Unable to connect to the server. Please try again."
                    );
                }

        } finally {

            setLoading(false);

        }
    }

    return (

        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 via-slate-100 to-blue-50 p-6">

            <div className="w-full max-w-lg rounded-2xl bg-white p-8 shadow-xl">

                <div className="mb-10 flex flex-col items-center">
                    <Logo />

                    <h2 className="mt-6 text-2xl font-bold text-slate-800">
                        Welcome Back
                    </h2>

                    <p className="mt-2 text-sm text-slate-500">
                        Sign in to continue to ExecuMind AI
                    </p>
                </div>

                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                >

                    <div>

                        <label className="mb-2 block text-sm font-medium">

                            Username

                        </label>

                        <div className="relative">

                            <User
                                size={18}
                                className="absolute left-3 top-3 text-gray-400"
                            />

                            <input
                                className="w-full rounded-lg border py-2 pl-10 pr-3 focus:border-blue-500 focus:outline-none"
                                value={username}
                                onChange={(e) =>
                                    setUsername(
                                        e.target.value
                                    )
                                }
                                required
                            />

                        </div>

                    </div>

                    <div>

                        <label className="mb-2 block text-sm font-medium">

                            Password

                        </label>

                        <div className="relative">

                            <Lock
                                size={18}
                                className="absolute left-3 top-3 text-gray-400"
                            />

                            <input
                                type={
                                    showPassword
                                        ? "text"
                                        : "password"
                                }
                                className="w-full rounded-lg border py-2 pl-10 pr-10 focus:border-blue-500 focus:outline-none"
                                value={password}
                                onChange={(e) =>
                                    setPassword(
                                        e.target.value
                                    )
                                }
                                required
                            />

                            <button
                                type="button"
                                className="absolute right-3 top-2.5"
                                onClick={() =>
                                    setShowPassword(
                                        !showPassword
                                    )
                                }
                            >

                                {showPassword
                                    ? <EyeOff size={18}/>
                                    : <Eye size={18}/>
                                }

                            </button>

                        </div>

                    </div>

                    {error && (

                        <div className="
                            animate-fade-in
                            rounded-lg
                            border
                            border-red-200
                            bg-red-50
                            p-3
                            text-sm
                            font-medium
                            text-red-600
                        ">

                            {error}

                        </div>

                    )}

                    <button
                    type="submit"
                    disabled={loading}
                    className="flex w-full items-center justify-center gap-2 rounded-xl bg-brand-600 py-3 font-semibold text-white transition hover:bg-brand-700 disabled:opacity-60">

                    {loading ? (

                        <>

                            <Loader2
                                className="h-4 w-4 animate-spin"
                            />

                            Signing In...

                        </>

                    ) : (

                        "Sign In"

                    )}

                </button>

                </form>

            </div>

        </div>

    );
}