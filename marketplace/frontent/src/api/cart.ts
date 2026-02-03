import { getToken } from "../auth/token";
import { getJson, postJson } from "./http";

export type CartItem = {
    offer_uid: string;
    quantity: number;
};

export type GetCartResponse200 = {
    items: CartItem[];
};

export async function getCart(): Promise<GetCartResponse200> {
    const token = getToken();
    if (!token) {
        throw { status: 401, message: "unauthorized" };
    }
    return getJson<GetCartResponse200>("/api/cart", token);
}

export async function upsertCartItem(offerUid: string, quantity: number): Promise<void> {
    const token = getToken();
    if (!token) {
        throw { status: 401, message: "unauthorized" };
    }
    await postJson<unknown>("/api/cart_items", { offer_uid: offerUid, quantity }, token);
}


