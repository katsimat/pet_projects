import styles from "./CartButton.module.css";

type CartButtonProps = {
    count: number;
    onClick?: () => void;
};

export function CartButton(props: CartButtonProps) {
    return (
        <button className={styles.btn} type="button" aria-label="Cart" onClick={props.onClick}>
            <span className={styles.icon} aria-hidden="true">
                🛒
            </span>
            {props.count > 0 ? <span className={styles.badge}>{props.count}</span> : null}
        </button>
    );
}


