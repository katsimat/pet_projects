import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getCart, upsertCartItem, type CartItem } from "../../api/cart";
import { getOffer, listOffers, type Offer } from "../../api/offers";
import { clearToken } from "../../auth/token";
import { CartButton } from "../../components/CartButton/CartButton";
import { CartDrawer } from "../../components/CartDrawer/CartDrawer";
import { Sidebar } from "../../components/Sidebar/Sidebar";
import { paths } from "../../routes/paths";
import styles from "./OffersPage.module.css";

export function OffersPage() {
    const navigate = useNavigate();
    const [textSearch, setTextSearch] = useState("");
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [offers, setOffers] = useState<Offer[]>([]);
    const [cartQtyByOfferUid, setCartQtyByOfferUid] = useState<Record<string, number>>({});
    const [cartItems, setCartItems] = useState<CartItem[]>([]);
    const [isCartOpen, setIsCartOpen] = useState(false);

    const canSearch = useMemo(() => textSearch.trim().length > 0, [textSearch]);
    const cartCount = useMemo(
        () => Object.values(cartQtyByOfferUid).reduce((acc, q) => acc + q, 0),
        [cartQtyByOfferUid]
    );

    useEffect(() => {
        setIsLoading(true);
        setError(null);

        Promise.all([listOffers(), getCart()])
            .then(([offersRes, cartRes]) => {
                setOffers(offersRes.offers);
                setCartItems(cartRes.items);
                const map: Record<string, number> = {};
                for (const it of cartRes.items) {
                    map[it.offer_uid] = it.quantity;
                }
                setCartQtyByOfferUid(map);
            })
            .catch((err) => {
                if (err?.status === 401) {
                    clearToken();
                    navigate(paths.auth);
                    return;
                }
                setError(err?.message ?? "Ошибка загрузки");
            })
            .finally(() => setIsLoading(false));
    }, []);

    function onSearch() {
        setIsLoading(true);
        setError(null);

        listOffers(canSearch ? textSearch.trim() : undefined)
            .then((res) => setOffers(res.offers))
            .catch((err) => setError(err?.message ?? "Ошибка загрузки"))
            .finally(() => setIsLoading(false));
    }

    return (
        <div className={styles.layout}>
            <Sidebar
                onLogout={() => {
                    clearToken();
                    navigate(paths.auth);
                }}
            />

            <div className={styles.page}>
                <header className={styles.header}>
                    <div className={styles.topbar}>
                        <div className={styles.search}>
                            <span className={styles.searchIcon} aria-hidden="true">
                                ⌕
                            </span>
                            <input
                                className={styles.searchInput}
                                placeholder="Search Here"
                                value={textSearch}
                                onChange={(e) => setTextSearch(e.target.value)}
                                onKeyDown={(e) => {
                                    if (e.key === "Enter") {
                                        onSearch();
                                    }
                                }}
                            />
                        </div>

                        <CartButton count={cartCount} onClick={() => setIsCartOpen(true)} />
                    </div>
                </header>

                <main className={styles.content}>
                    <h2 className={styles.title}>Goods to buy</h2>

                    {isLoading ? <div className={styles.status}>Загрузка...</div> : null}
                    {error ? <div className={styles.error}>{error}</div> : null}

                    <div className={styles.grid}>
                        {offers.map((o) => {
                            const qty = cartQtyByOfferUid[o.uid] ?? 0;
                            const isAdded = qty > 0;

                            return (
                                <article key={o.uid} className={styles.card}>
                                    <div className={styles.image} aria-hidden="true">
                                        <div className={styles.imageInner} />
                                    </div>

                                    <div className={styles.cardBody}>
                                        <div className={styles.priceRow}>
                                            <div className={styles.price}>$ {o.price}</div>
                                        </div>

                                        <div className={styles.desc}>
                                            <div className={styles.productTitle}>{o.title}</div>
                                            <div className={styles.productDesc}>
                                                {o.description ?? "description"}
                                            </div>
                                        </div>

                                        <button
                                            className={isAdded ? styles.addedBtn : styles.addBtn}
                                            type="button"
                                            disabled={isAdded}
                                            onClick={(e) => {
                                                e.preventDefault();
                                                e.stopPropagation();
                                                setError(null);

                                                upsertCartItem(o.uid, 1)
                                                    .then(() => {
                                                        setCartItems((prev) => {
                                                            const exists = prev.some((it) => it.offer_uid === o.uid);
                                                            if (exists) {
                                                                return prev.map((it) =>
                                                                    it.offer_uid === o.uid
                                                                        ? { ...it, quantity: 1 }
                                                                        : it
                                                                );
                                                            }
                                                            return [...prev, { offer_uid: o.uid, quantity: 1 }];
                                                        });
                                                        setCartQtyByOfferUid((prev) => ({
                                                            ...prev,
                                                            [o.uid]: 1
                                                        }));
                                                    })
                                                    .catch((err) => {
                                                        if (err?.status === 401) {
                                                            clearToken();
                                                            navigate(paths.auth);
                                                            return;
                                                        }
                                                        setError(err?.message ?? "Ошибка добавления в корзину");
                                                    });
                                            }}
                                        >
                                            {isAdded ? "added" : "add to bag"}
                                        </button>
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                </main>
            </div>

            <CartDrawer
                isOpen={isCartOpen}
                onClose={() => setIsCartOpen(false)}
                items={cartItems}
                resolveOffer={(uid) => getOffer(uid)}
                onOrderCreated={async () => {
                    const cartRes = await getCart();
                    setCartItems(cartRes.items);
                    const map: Record<string, number> = {};
                    for (const it of cartRes.items) {
                        map[it.offer_uid] = it.quantity;
                    }
                    setCartQtyByOfferUid(map);
                }}
            />
        </div>
    );
}


