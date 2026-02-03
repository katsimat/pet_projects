import { getToken } from "../auth/token";
import { postJson } from "./http";

export type CreateOrderResponse201 = {
    uid: string;
    status: string;
};

export async function createOrder(): Promise<CreateOrderResponse201> {
    const token = getToken();
    if (!token) {
        throw { status: 401, message: "unauthorized" };
    }
    return postJson<CreateOrderResponse201>("/api/orders", {}, token);
}


