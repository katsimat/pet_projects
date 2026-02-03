import { Navigate, Route, Routes } from "react-router-dom";

import { getToken } from "./auth/token";
import { AuthPage } from "./pages/AuthPage/AuthPage";
import { OffersPage } from "./pages/OffersPage/OffersPage";
import { paths } from "./routes/paths";

export function App() {
    const hasToken = Boolean(getToken());

    return (
        <Routes>
            <Route
                path="/"
                element={<Navigate to={hasToken ? paths.offers : paths.auth} replace />}
            />
            <Route path={paths.auth} element={<AuthPage />} />
            <Route path={paths.offers} element={<OffersPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}


