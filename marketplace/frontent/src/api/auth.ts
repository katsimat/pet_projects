import { postJson } from "./http";

export type LoginResponse200 = {
    token: string;
};

export async function login(email: string, password: string): Promise<LoginResponse200> {
    return postJson<LoginResponse200>("/api/auth/login", { email, password });
}


