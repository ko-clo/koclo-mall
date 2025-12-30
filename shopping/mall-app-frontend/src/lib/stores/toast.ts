import { writable } from 'svelte/store';

export interface Toast {
	id: string;
	message: string;
	type: 'success' | 'error' | 'info';
	duration?: number;
	action?: {
		label: string;
		href: string;
	};
}

function createToastStore() {
	const { subscribe, update } = writable<Toast[]>([]);

	function addToast(toast: Omit<Toast, 'id'>) {
		const id = crypto.randomUUID();
		const newToast: Toast = { ...toast, id };

		update((toasts) => [...toasts, newToast]);

		const duration = toast.duration ?? 3000;
		if (duration > 0) {
			setTimeout(() => {
				removeToast(id);
			}, duration);
		}

		return id;
	}

	function removeToast(id: string) {
		update((toasts) => toasts.filter((t) => t.id !== id));
	}

	return {
		subscribe,
		success: (message: string, action?: Toast['action']) =>
			addToast({ message, type: 'success', action }),
		error: (message: string, action?: Toast['action']) =>
			addToast({ message, type: 'error', action }),
		info: (message: string, action?: Toast['action']) =>
			addToast({ message, type: 'info', action }),
		remove: removeToast
	};
}

export const toastStore = createToastStore();
