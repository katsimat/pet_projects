import { useEffect, useMemo, useState } from "react";

import type { CartItem } from "../../api/cart";
import { createOrder } from "../../api/orders";
import type { Offer } from "../../api/offers";
import styles from "./CartDrawer.module.css";

export type CartDrawerOfferLine = {
    offer: Offer;
    quantity: number;
};

type CartDrawerProps = {
    isOpen: boolean;
    onClose: () => void;
    items: CartItem[];
    resolveOffer: (offerUid: string) => Promise<Offer>;
    onOrderCreated: () => Promise<void>;
};

function parsePrice(s: string): number {
    const n = Number.parseFloat(s);
    return Number.isFinite(n) ? n : 0;
}

export function CartDrawer(props: CartDrawerProps) {
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [lines, setLines] = useState<CartDrawerOfferLine[]>([]);
    const [isOrdering, setIsOrdering] = useState(false);
    const [orderSuccess, setOrderSuccess] = useState<string | null>(null);

    const total = useMemo(() => {
        return lines.reduce((acc, l) => acc + parsePrice(l.offer.price) * l.quantity, 0);
    }, [lines]);

    useEffect(() => {
        if (!props.isOpen) {
            setError(null);
            setOrderSuccess(null);
            return;
        }

        setIsLoading(true);
        setError(null);
        setOrderSuccess(null);

        Promise.all(props.items.map((it) => props.resolveOffer(it.offer_uid)))
            .then((offers) => {
                const map = new Map<string, Offer>();
                for (const o of offers) {
                    map.set(o.uid, o);
                }
                const next: CartDrawerOfferLine[] = [];
                for (const it of props.items) {
                    const offer = map.get(it.offer_uid);
                    if (!offer) continue;
                    next.push({ offer, quantity: it.quantity });
                }
                setLines(next);
            })
            .catch((err) => setError(err?.message ?? "Ошибка загрузки корзины"))
            .finally(() => setIsLoading(false));
    }, [props.isOpen, props.items]);

    if (!props.isOpen) return null;

    return (
        <div className={styles.overlay} role="dialog" aria-modal="true" aria-label="Cart">
            <div className={styles.backdrop} onClick={props.onClose} />
            <aside className={styles.drawer}>
                <header className={styles.header}>
                    <div className={styles.title}>Корзина</div>
                    <button className={styles.closeBtn} type="button" onClick={props.onClose}>
                        ✕
                    </button>
                </header>

                <div className={styles.body}>
                    {isLoading ? <div className={styles.status}>Загрузка...</div> : null}
                    {error ? <div className={styles.error}>{error}</div> : null}
                    {orderSuccess ? <div className={styles.success}>{orderSuccess}</div> : null}

                    {!isLoading && !error && props.items.length === 0 ? (
                        <div className={styles.empty}>Пока пусто</div>
                    ) : null}

                    <div className={styles.list}>
                        {lines.map((l) => (
                            <div className={styles.row} key={l.offer.uid}>
                                <div className={styles.thumb} aria-hidden="true" />
                                <div className={styles.meta}>
                                    <div className={styles.offerTitle}>{l.offer.title}</div>
                                    <div className={styles.sub}>
                                        <span>$ {l.offer.price}</span>
                                        <span className={styles.dot} aria-hidden="true">
                                            ·
                                        </span>
                                        <span>qty {l.quantity}</span>
                                    </div>
                                </div>
                                <div className={styles.lineTotal}>
                                    $ {(parsePrice(l.offer.price) * l.quantity).toFixed(2)}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <footer className={styles.footer}>
                    <div className={styles.footerRow}>
                        <div className={styles.totalLabel}>Итого</div>
                        <div className={styles.totalValue}>$ {total.toFixed(2)}</div>
                    </div>

                    <button
                        className={styles.orderBtn}
                        type="button"
                        disabled={props.items.length === 0 || isOrdering}
                        onClick={() => {
                            setIsOrdering(true);
                            setError(null);
                            setOrderSuccess(null);

                            createOrder()
                                .then((res) => {
                                    setOrderSuccess(`Заказ создан: ${res.uid}`);
                                    return props.onOrderCreated();
                                })
                                .catch((err) => setError(err?.message ?? "Ошибка создания заказа"))
                                .finally(() => setIsOrdering(false));
                        }}
                    >
                        {isOrdering ? "Оформляем..." : "Заказать"}
                    </button>
                </footer>
            </aside>
        </div>
    );
}


