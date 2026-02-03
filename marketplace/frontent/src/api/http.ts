export type HttpError = {
    status: number;
    message: string;
};

export async function getJson<TResponse>(url: string, token?: string): Promise<TResponse> {
    const res = await fetch(url, {
        method: "GET",
        headers: {
            ...(token ? { Authorization: `Bearer ${token}` } : {})
        }
    });

    const text = await res.text();
    const data = text ? JSON.parse(text) : null;

    if (!res.ok) {
        const msg = data?.error ?? `HTTP ${res.status}`;
        throw { status: res.status, message: msg } satisfies HttpError;
    }

    return data as TResponse;
}

export async function postJson<TResponse>(
    url: string,
    body: unknown,
    token?: string
): Promise<TResponse> {
    const res = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            ...(token ? { Authorization: `Bearer ${token}` } : {})
        },
        body: JSON.stringify(body)
    });

    const text = await res.text();
    const data = text ? JSON.parse(text) : null;

    if (!res.ok) {
        const msg = data?.error ?? `HTTP ${res.status}`;
        throw { status: res.status, message: msg } satisfies HttpError;
    }

    return data as TResponse;
}


