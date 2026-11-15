/**
 * BYT3LAB Admin Console TypeScript (admin.ts)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Delete confirmation dialogs
    const deleteButtons = document.querySelectorAll<HTMLElement>('[data-confirm-delete]');
    deleteButtons.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            const msg = btn.getAttribute('data-confirm-delete') || 'Êtes-vous sûr de vouloir supprimer cet élément ?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    // 2. Settings tab switching
    const settingsTabs = document.querySelectorAll<HTMLElement>('.byt3lab-admin-tab-btn');
    const settingsPanels = document.querySelectorAll<HTMLElement>('.byt3lab-admin-tab-panel');

    settingsTabs.forEach((tab) => {
        tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-target');

            settingsTabs.forEach((t) => t.classList.remove('is-active'));
            settingsPanels.forEach((p) => p.classList.remove('is-active'));

            tab.classList.add('is-active');
            if (targetId) {
                const panel = document.getElementById(targetId);
                if (panel) {
                    panel.classList.add('is-active');
                }
            }
        });
    });
});
