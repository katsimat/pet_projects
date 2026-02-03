import { getJson } from "./http";

export type Offer = {
    uid: string;
    title: string;
    description?: string;
    price: string;
    quantity: number;
    status: "active" | "inactive" | "sold_out";
    seller: {
        email: string;
        name: string;
        surname: string;
    };
};

export type ListOffersResponse200 = {
    offers: Offer[];
};

export async function listOffers(textSearch?: string): Promise<ListOffersResponse200> {
    const params = new URLSearchParams();
    if (textSearch) {
        params.set("text_search", textSearch);
    }
    const qs = params.toString();
    return getJson<ListOffersResponse200>(`/api/offers${qs ? `?${qs}` : ""}`);
}

export async function getOffer(uid: string): Promise<Offer> {
    const params = new URLSearchParams();
    params.set("uid", uid);
    return getJson<Offer>(`/api/offers/get?${params.toString()}`);
}


