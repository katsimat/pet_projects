import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { login } from "../../api/auth";
import { setToken } from "../../auth/token";
import { paths } from "../../routes/paths";
import styles from "./AuthPage.module.css";

export function AuthPage() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState(false);

    return (
        <div className={styles.page}>
            <div className={styles.card} role="region" aria-label="Authorizing">
                <form
                    className={styles.form}
                    onSubmit={(e) => {
                        e.preventDefault();
                        setError(null);
                        setSuccess(false);
                        setIsLoading(true);

                        login(email, password)
                            .then((res) => {
                                setToken(res.token);
                                setSuccess(true);
                                navigate(paths.offers);
                            })
                            .catch((err) => {
                                setError(err?.message ?? "Ошибка авторизации");
                            })
                            .finally(() => setIsLoading(false));
                    }}
                >
                    <div className={styles.field}>
                        <label className={styles.label} htmlFor="email">
                            Email
                        </label>
                        <input
                            id="email"
                            className={styles.input}
                            placeholder="Value"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            autoComplete="email"
                        />
                    </div>

                    <div className={styles.field}>
                        <label className={styles.label} htmlFor="password">
                            Password
                        </label>
                        <input
                            id="password"
                            className={styles.input}
                            placeholder="Value"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="current-password"
                        />
                    </div>

                    <div className={styles.actions}>
                        <button className={styles.signUpBtn} type="button">
                            Sign up
                        </button>
                        <button
                            className={styles.signInBtn}
                            type="submit"
                            disabled={!email || !password || isLoading}
                        >
                            {isLoading ? "Signing..." : "Sign In"}
                        </button>
                    </div>

                    {error ? <div className={styles.error}>{error}</div> : null}
                    {success ? <div className={styles.success}>Успешный вход, токен сохранён</div> : null}

                    <a className={styles.forgotLink} href="#" onClick={(e) => e.preventDefault()}>
                        Forgot password?
                    </a>
                </form>
            </div>
        </div>
    );
}


