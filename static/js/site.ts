/**
 * BYT3LAB Client TypeScript (site.ts)
 * Gestion du header sticky, de la navigation mobile, des onglets et des formulaires sécurisés.
 */

interface AjaxResponse {
    success: boolean;
    data?: {
        message?: string;
        whatsapp_url?: string;
    };
    message?: string;
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Header sticky compact on scroll
    const header = document.querySelector<HTMLElement>('.b-header');
    if (header) {
        const updateHeader = () => {
            if (window.scrollY > 20) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }
        };
        window.addEventListener('scroll', updateHeader, { passive: true });
        updateHeader();
    }

    // 2. Mobile drawer navigation
    const burger = document.getElementById('b-burger-btn');
    const drawer = document.getElementById('b-mobile-drawer');
    const overlay = document.getElementById('b-nav-overlay');

    if (burger && drawer) {
        const openMenu = () => {
            drawer.classList.add('is-open');
            if (overlay) overlay.classList.add('is-open');
            burger.setAttribute('aria-expanded', 'true');
            drawer.setAttribute('aria-hidden', 'false');
            document.body.style.overflow = 'hidden';
        };

        const closeMenu = () => {
            drawer.classList.remove('is-open');
            if (overlay) overlay.classList.remove('is-open');
            burger.setAttribute('aria-expanded', 'false');
            drawer.setAttribute('aria-hidden', 'true');
            document.body.style.overflow = '';
        };

        const toggleMenu = () => {
            if (drawer.classList.contains('is-open')) {
                closeMenu();
            } else {
                openMenu();
            }
        };

        burger.addEventListener('click', toggleMenu);
        if (overlay) overlay.addEventListener('click', closeMenu);

        // Close on Escape key
        document.addEventListener('keydown', (e: KeyboardEvent) => {
            if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
                closeMenu();
                burger.focus();
            }
        });

        // Close drawer on internal link click
        drawer.querySelectorAll('a[href]').forEach((link) => {
            link.addEventListener('click', () => {
                closeMenu();
            });
        });

        // Auto close if resized to desktop
        const mql = window.matchMedia('(min-width: 992px)');
        mql.addEventListener('change', (e) => {
            if (e.matches && drawer.classList.contains('is-open')) {
                closeMenu();
            }
        });
    }

    // 3. Desktop Dropdowns (Accessible click + hover)
    const dropdownItems = document.querySelectorAll<HTMLElement>('.b-nav__item--has-drop');
    dropdownItems.forEach((item) => {
        const trigger = item.querySelector<HTMLElement>('.b-nav__link');
        if (!trigger) return;

        trigger.addEventListener('click', (e) => {
            const isDesktop = window.matchMedia('(min-width: 992px)').matches;
            if (!isDesktop) return;

            const expanded = trigger.getAttribute('aria-expanded') === 'true';

            // Close other dropdowns
            dropdownItems.forEach((other) => {
                if (other !== item) {
                    const otherTrigger = other.querySelector<HTMLElement>('.b-nav__link');
                    if (otherTrigger) otherTrigger.setAttribute('aria-expanded', 'false');
                    other.classList.remove('is-active');
                }
            });

            trigger.setAttribute('aria-expanded', String(!expanded));
            item.classList.toggle('is-active', !expanded);

            if (!expanded) {
                e.preventDefault();
            }
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', (e: MouseEvent) => {
        const target = e.target as HTMLElement;
        if (!target.closest('.b-nav__item--has-drop')) {
            dropdownItems.forEach((item) => {
                const trigger = item.querySelector<HTMLElement>('.b-nav__link');
                if (trigger) trigger.setAttribute('aria-expanded', 'false');
                item.classList.remove('is-active');
            });
        }
    });

    // 4. Tabs system (Secteurs d'activité, etc.)
    const tabGroups = document.querySelectorAll<HTMLElement>('.b-tabs');
    tabGroups.forEach((group) => {
        const buttons = group.querySelectorAll<HTMLButtonElement>('.b-tabs__btn');
        const panels = group.querySelectorAll<HTMLElement>('.b-tabs__panel');

        buttons.forEach((btn) => {
            btn.addEventListener('click', () => {
                const targetId = btn.getAttribute('aria-controls');

                buttons.forEach((b) => b.setAttribute('aria-selected', 'false'));
                panels.forEach((p) => p.classList.remove('is-active'));

                btn.setAttribute('aria-selected', 'true');
                if (targetId) {
                    const targetPanel = group.querySelector<HTMLElement>('#' + targetId);
                    if (targetPanel) {
                        targetPanel.classList.add('is-active');
                    }
                }
            });
        });
    });

    // 4b. Services Interactive Department / Branch Filter
    const filterButtons = document.querySelectorAll<HTMLButtonElement>('.service-filter-btn');
    const serviceItems = document.querySelectorAll<HTMLElement>('.service-item-col');
    if (filterButtons.length && serviceItems.length) {
        filterButtons.forEach((btn) => {
            btn.addEventListener('click', () => {
                filterButtons.forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');

                const selectedFilter = (btn.getAttribute('data-filter') || 'all').toLowerCase().trim();

                serviceItems.forEach((item) => {
                    const itemBranch = (item.getAttribute('data-branch') || '').toLowerCase().trim();
                    const isMatch =
                        selectedFilter === 'all' ||
                        itemBranch === selectedFilter ||
                        itemBranch.includes(selectedFilter) ||
                        selectedFilter.includes(itemBranch);

                    if (isMatch) {
                        item.style.display = 'block';
                        setTimeout(() => {
                            item.style.opacity = '1';
                            item.style.transform = 'scale(1)';
                        }, 30);
                    } else {
                        item.style.opacity = '0';
                        item.style.transform = 'scale(0.96)';
                        setTimeout(() => {
                            item.style.display = 'none';
                        }, 220);
                    }
                });
            });
        });
    }

    // 5. Secure AJAX Form Submission (Contact & Partner)
    const ajaxForms = document.querySelectorAll<HTMLFormElement>('form[data-b-ajax="1"]');
    ajaxForms.forEach((form) => {
        // Enregistrer le timestamp pour le time-trap anti-bot
        const tsInput = form.querySelector<HTMLInputElement>('input[name="byt3lab_ts"]');
        if (tsInput) {
            tsInput.value = String(Math.floor(Date.now() / 1000));
        }

        form.addEventListener('submit', async (e: Event) => {
            e.preventDefault();

            const feedback = form.querySelector<HTMLElement>('.b-form-feedback');
            const submitBtn = form.querySelector<HTMLButtonElement>('button[type="submit"]');
            const originalBtnText = submitBtn ? submitBtn.innerHTML : '';

            if (feedback) {
                feedback.className = 'b-form-feedback';
                feedback.style.display = 'none';
                feedback.innerHTML = '';
            }

            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'Transmission en cours...';
            }

            const formData = new FormData(form);
            const actionUrl = form.getAttribute('action') || '/api/byt3lab_app/contact';

            try {
                const response = await fetch(actionUrl, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json',
                    },
                });

                const result: AjaxResponse = await response.json();

                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                }

                if (result && result.success) {
                    if (feedback) {
                        feedback.className = 'b-form-feedback is-success';
                        feedback.style.display = 'block';

                        let html = `<p style="margin: 0 0 8px 0; font-weight: 600;">${result.data?.message || 'Demande transmise avec succès !'}</p>`;
                        if (result.data?.whatsapp_url) {
                            html += `<a href="${result.data.whatsapp_url}" target="_blank" rel="noopener noreferrer" class="b-btn b-btn--sm b-btn--primary" style="background:#16a34a; border-color:#16a34a; margin-top: 10px;">Suivre instantanément sur WhatsApp &rarr;</a>`;
                        }
                        feedback.innerHTML = html;
                    }
                    form.reset();
                } else {
                    const errMsg = result?.data?.message || result?.message || 'Une erreur est survenue lors de l\'envoi. Veuillez vérifier vos données.';
                    if (feedback) {
                        feedback.className = 'b-form-feedback is-error';
                        feedback.style.display = 'block';
                        feedback.innerHTML = `<p style="margin: 0;">${errMsg}</p>`;
                    }
                }
            } catch (err) {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                }
                if (feedback) {
                    feedback.className = 'b-form-feedback is-error';
                    feedback.style.display = 'block';
                    feedback.innerHTML = '<p style="margin: 0;">Erreur de connexion au serveur. Veuillez vérifier votre réseau ou nous contacter directement par e-mail.</p>';
                }
            }
        });
    });
});

// Bouton Copier le lien sur les articles de blog
document.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement)?.closest('[data-copy-url]') as HTMLElement | null;
    if (!btn) return;
    const url = btn.getAttribute('data-copy-url') || window.location.href;
    if (navigator.clipboard) {
        navigator.clipboard.writeText(url).then(() => {
            const orig = btn.textContent;
            btn.textContent = '✓';
            setTimeout(() => { btn.textContent = orig; }, 1800);
        }).catch(() => {});
    }
});

// Filtrage interactif du portfolio (Accueil & Réalisations)
document.addEventListener('DOMContentLoaded', () => {
    const filterBars = document.querySelectorAll<HTMLElement>('[data-portfolio-filters]');
    filterBars.forEach((bar) => {
        const container = bar.parentElement;
        const grid = container?.querySelector<HTMLElement>('[data-portfolio-grid]');
        if (!grid) return;

        const applyFilter = (filterVal: string) => {
            const items = grid.querySelectorAll<HTMLElement>('[data-portfolio-item]');
            items.forEach((el) => {
                const cat = el.getAttribute('data-portfolio-item') || 'software';
                el.style.display = (filterVal === 'all' || cat === filterVal) ? '' : 'none';
            });
        };

        const buttons = bar.querySelectorAll<HTMLButtonElement>('[data-filter]');
        buttons.forEach((btn) => {
            btn.addEventListener('click', () => {
                buttons.forEach((b) => b.classList.remove('is-active'));
                btn.classList.add('is-active');
                applyFilter(btn.getAttribute('data-filter') || 'all');
            });
        });

        const initialActive = bar.querySelector<HTMLButtonElement>('[data-filter].is-active');
        if (initialActive) {
            applyFilter(initialActive.getAttribute('data-filter') || 'all');
        }
    });

    // Synchronisation des puces de sélection rapide de Pôle sur la page Contact
    const contactChips = document.querySelector<HTMLElement>('[data-contact-pole-chips]');
    const poleSelect = document.getElementById('c-pole') as HTMLSelectElement | null;
    if (contactChips && poleSelect) {
        const chipBtns = contactChips.querySelectorAll<HTMLButtonElement>('[data-pole-val]');
        const setChipActive = (val: string) => {
            chipBtns.forEach((b) => b.classList.toggle('is-active', b.getAttribute('data-pole-val') === val));
        };
        chipBtns.forEach((btn) => {
            btn.addEventListener('click', () => {
                const val = btn.getAttribute('data-pole-val') || 'global';
                poleSelect.value = val;
                setChipActive(val);
            });
        });
        poleSelect.addEventListener('change', () => setChipActive(poleSelect.value));
    }
});

// 6. Découverte progressive légère au défilement (IntersectionObserver)
(() => {
    const initScrollReveal = () => {
        const targets = Array.from(document.querySelectorAll<HTMLElement>('[data-reveal]'));
        if (!targets.length) return;

        const prefersReduced =
            typeof window.matchMedia === 'function' &&
            window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (prefersReduced || typeof IntersectionObserver === 'undefined') {
            targets.forEach((el) => el.classList.add('is-visible'));
            return;
        }

        document.documentElement.classList.add('js-reveal-ready');

        // Révéler immédiatement les éléments Hero au chargement (chorégraphie fluide)
        const heroEls = targets.filter((el) => el.getAttribute('data-reveal') === 'hero');
        const scrollEls = targets.filter((el) => el.getAttribute('data-reveal') !== 'hero');

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                heroEls.forEach((el) => el.classList.add('is-visible'));
            });
        });

        const observer = new IntersectionObserver(
            (entries, obs) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('is-visible');
                        obs.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.08,
                rootMargin: '0px 0px -36px 0px',
            }
        );

        scrollEls.forEach((el) => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight * 0.92) {
                el.classList.add('is-visible');
            } else {
                observer.observe(el);
            }
        });
    };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initScrollReveal);
    } else {
        initScrollReveal();
    }
})();
