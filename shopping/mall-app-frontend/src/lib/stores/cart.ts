import { writable, derived, get } from 'svelte/store';
import { browser } from '$app/environment';
import { authStore } from './auth';

const CART_STORAGE_KEY = 'koclo_cart';
const CART_MAX_ITEMS = 50;

export interface GuestCartItem {
	product_option_id: string;
	quantity: number;
	added_at: string;
}

export interface CartItem extends GuestCartItem {
	id?: string;
	product?: {
		id: string;
		name: string;
		slug: string;
		thumbnail_url: string;
	};
	option?: {
		id: string;
		color: string;
		size: string;
		price: number;
		discount_price?: number;
		stock: number;
	};
	status?: 'available' | 'out_of_stock' | 'insufficient_stock' | 'deleted';
}

export interface CartResult {
	success: boolean;
	message: string;
	isNewItem?: boolean;
}

function createCartStore() {
	const initialItems: GuestCartItem[] = browser
		? JSON.parse(localStorage.getItem(CART_STORAGE_KEY) || '[]')
		: [];

	const { subscribe, set, update } = writable<GuestCartItem[]>(initialItems);

	function saveToStorage(items: GuestCartItem[]) {
		if (browser) {
			localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
		}
	}

	function isLoggedIn(): boolean {
		const auth = get(authStore);
		return !!auth.user;
	}

	// 비회원 장바구니 추가 (로컬스토리지)
	function addItemToGuest(productOptionId: string, quantity: number): CartResult {
		let result: CartResult = { success: false, message: '' };

		update((items) => {
			const existingIndex = items.findIndex((item) => item.product_option_id === productOptionId);

			if (items.length >= CART_MAX_ITEMS && existingIndex === -1) {
				result = {
					success: false,
					message: `장바구니는 최대 ${CART_MAX_ITEMS}개 상품까지 담을 수 있습니다.`
				};
				return items;
			}

			if (existingIndex !== -1) {
				const updatedItems = [...items];
				updatedItems[existingIndex] = {
					...updatedItems[existingIndex],
					quantity: updatedItems[existingIndex].quantity + quantity
				};
				saveToStorage(updatedItems);
				result = { success: true, message: '수량이 변경되었습니다.', isNewItem: false };
				return updatedItems;
			}

			const newItem: GuestCartItem = {
				product_option_id: productOptionId,
				quantity,
				added_at: new Date().toISOString()
			};
			const updatedItems = [...items, newItem];
			saveToStorage(updatedItems);
			result = { success: true, message: '장바구니에 추가되었습니다.', isNewItem: true };
			return updatedItems;
		});

		return result;
	}

	// 회원 장바구니 추가 (API 호출) - TODO: API 연동 시 구현
	async function addItemToMember(productOptionId: string, quantity: number): Promise<CartResult> {
		// TODO: 실제 API 호출로 대체
		// const response = await fetch('/api/carts/items', {
		//   method: 'POST',
		//   headers: { 'Content-Type': 'application/json' },
		//   body: JSON.stringify({ product_option_id: productOptionId, quantity })
		// });
		// if (!response.ok) { ... }

		// 임시: 비회원과 동일하게 처리 (나중에 API로 대체)
		return addItemToGuest(productOptionId, quantity);
	}

	return {
		subscribe,

		async addItem(productOptionId: string, quantity: number): Promise<CartResult> {
			if (isLoggedIn()) {
				return await addItemToMember(productOptionId, quantity);
			}
			return addItemToGuest(productOptionId, quantity);
		},

		async updateQuantity(productOptionId: string, quantity: number): Promise<void> {
			// TODO: 회원인 경우 API 호출
			update((items) => {
				if (quantity <= 0) {
					const updatedItems = items.filter((item) => item.product_option_id !== productOptionId);
					saveToStorage(updatedItems);
					return updatedItems;
				}

				const updatedItems = items.map((item) =>
					item.product_option_id === productOptionId ? { ...item, quantity } : item
				);
				saveToStorage(updatedItems);
				return updatedItems;
			});
		},

		async removeItem(productOptionId: string): Promise<void> {
			// TODO: 회원인 경우 API 호출
			update((items) => {
				const updatedItems = items.filter((item) => item.product_option_id !== productOptionId);
				saveToStorage(updatedItems);
				return updatedItems;
			});
		},

		async removeItems(productOptionIds: string[]): Promise<void> {
			// TODO: 회원인 경우 API 호출
			update((items) => {
				const updatedItems = items.filter(
					(item) => !productOptionIds.includes(item.product_option_id)
				);
				saveToStorage(updatedItems);
				return updatedItems;
			});
		},

		async clear(): Promise<void> {
			// TODO: 회원인 경우 API 호출
			set([]);
			if (browser) {
				localStorage.removeItem(CART_STORAGE_KEY);
			}
		},

		getItems(): GuestCartItem[] {
			return get({ subscribe });
		}
	};
}

export const cartStore = createCartStore();

export const cartItemCount = derived(cartStore, ($cart) =>
	$cart.reduce((sum, item) => sum + item.quantity, 0)
);

export const cartUniqueItemCount = derived(cartStore, ($cart) => $cart.length);

// 장바구니 애니메이션 트리거용 스토어
export const cartAnimationTrigger = writable<number>(0);

export function triggerCartAnimation() {
	cartAnimationTrigger.update((n) => n + 1);
}
