import styles from "./Sidebar.module.css";

type SidebarProps = {
    onLogout: () => void;
};

export function Sidebar(props: SidebarProps) {
    return (
        <aside className={styles.sidebar} aria-label="Navigation">
            <div className={styles.logo}>M</div>

            <div className={styles.icons} aria-hidden="true">
                <div className={styles.iconBox}>🛒</div>
                <div className={styles.iconBox}>📋</div>
                <div className={styles.iconBox}>👤</div>
            </div>

            <div className={styles.bottom}>
                <button className={styles.logoutBtn} type="button" onClick={props.onLogout}>
                    Logout
                </button>
            </div>
        </aside>
    );
}


