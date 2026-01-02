export type OrderStatus = 'PENDING' | 'PAID' | 'PREPARING' | 'SHIPPING' | 'DELIVERED' | 'CANCELLED';

export interface DeliveryTracking {
	status: 'IN_TRANSIT' | 'OUT_FOR_DELIVERY' | 'DELIVERED';
	location: string;
	description: string;
	timestamp: string;
}

export interface OrderItem {
	id: string;
	product: {
		id: string;
		name: string;
		slug: string;
		thumbnail_url: string;
	};
	option: {
		color: string;
		size: string;
	};
	quantity: number;
	unit_price: number;
	subtotal: number;
}

export interface Order {
	id: string;
	order_number: string;
	status: OrderStatus;
	orderer: {
		name: string;
		phone: string;
		email: string;
	};
	shipping: {
		recipient: string;
		phone: string;
		postal_code: string;
		address: string;
		address_detail: string;
		memo: string;
		tracking_number?: string;
		carrier?: string;
	};
	items: OrderItem[];
	amounts: {
		items_total: number;
		shipping_fee: number;
		discount: number;
		total: number;
	};
	ordered_at: string;
	paid_at?: string;
	shipped_at?: string;
	delivered_at?: string;
	cancelled_at?: string;
	cancel_reason?: string;
}

export const orderStatusLabels: Record<OrderStatus, string> = {
	PENDING: '결제 대기',
	PAID: '결제 완료',
	PREPARING: '상품 준비중',
	SHIPPING: '배송중',
	DELIVERED: '배송 완료',
	CANCELLED: '주문 취소'
};

export const orderStatusColors: Record<OrderStatus, string> = {
	PENDING: 'badge-pending',
	PAID: 'badge-paid',
	PREPARING: 'badge-preparing',
	SHIPPING: 'badge-shipping',
	DELIVERED: 'badge-delivered',
	CANCELLED: 'badge-cancelled'
};

// Mock 주문 데이터
export const mockOrders: Order[] = [
	{
		id: 'order-1',
		order_number: 'ORD_20251230143052_a3f2e1',
		status: 'DELIVERED',
		orderer: {
			name: '홍길동',
			phone: '010-1234-5678',
			email: 'hong@example.com'
		},
		shipping: {
			recipient: '홍길동',
			phone: '010-1234-5678',
			postal_code: '06000',
			address: '서울특별시 강남구 테헤란로 123',
			address_detail: '456호',
			memo: '문 앞에 놔주세요',
			tracking_number: '1234567890',
			carrier: 'CJ대한통운'
		},
		items: [
			{
				id: 'item-1',
				product: {
					id: '1',
					name: '오버핏 캐시미어 니트',
					slug: 'overfit-cashmere-knit',
					thumbnail_url: 'https://picsum.photos/seed/knit1/400/533'
				},
				option: { color: 'Black', size: 'M' },
				quantity: 2,
				unit_price: 62000,
				subtotal: 124000
			}
		],
		amounts: {
			items_total: 124000,
			shipping_fee: 0,
			discount: 0,
			total: 124000
		},
		ordered_at: '2024-12-28T10:00:00Z',
		paid_at: '2024-12-28T10:05:00Z',
		shipped_at: '2024-12-29T09:00:00Z',
		delivered_at: '2024-12-30T14:00:00Z'
	},
	{
		id: 'order-2',
		order_number: 'ORD_20251229101530_b4c3d2',
		status: 'SHIPPING',
		orderer: {
			name: '홍길동',
			phone: '010-1234-5678',
			email: 'hong@example.com'
		},
		shipping: {
			recipient: '김철수',
			phone: '010-9876-5432',
			postal_code: '12345',
			address: '경기도 성남시 분당구 판교역로 235',
			address_detail: '101동 202호',
			memo: '경비실에 맡겨주세요',
			tracking_number: '9876543210',
			carrier: '한진택배'
		},
		items: [
			{
				id: 'item-2',
				product: {
					id: '2',
					name: '울 블렌드 롱 코트',
					slug: 'wool-blend-long-coat',
					thumbnail_url: 'https://picsum.photos/seed/coat1/400/533'
				},
				option: { color: 'Camel', size: 'L' },
				quantity: 1,
				unit_price: 129000,
				subtotal: 129000
			},
			{
				id: 'item-3',
				product: {
					id: '7',
					name: '울 머플러',
					slug: 'wool-muffler',
					thumbnail_url: 'https://picsum.photos/seed/muffler1/400/533'
				},
				option: { color: 'Gray', size: 'Free' },
				quantity: 1,
				unit_price: 29000,
				subtotal: 29000
			}
		],
		amounts: {
			items_total: 158000,
			shipping_fee: 0,
			discount: 0,
			total: 158000
		},
		ordered_at: '2024-12-29T10:15:30Z',
		paid_at: '2024-12-29T10:16:00Z',
		shipped_at: '2024-12-30T09:00:00Z'
	},
	{
		id: 'order-3',
		order_number: 'ORD_20251231090000_c5d4e3',
		status: 'PAID',
		orderer: {
			name: '홍길동',
			phone: '010-1234-5678',
			email: 'hong@example.com'
		},
		shipping: {
			recipient: '홍길동',
			phone: '010-1234-5678',
			postal_code: '06000',
			address: '서울특별시 강남구 테헤란로 123',
			address_detail: '456호',
			memo: ''
		},
		items: [
			{
				id: 'item-4',
				product: {
					id: '3',
					name: '와이드 데님 팬츠',
					slug: 'wide-denim-pants',
					thumbnail_url: 'https://picsum.photos/seed/denim1/400/533'
				},
				option: { color: 'Blue', size: 'M' },
				quantity: 1,
				unit_price: 49000,
				subtotal: 49000
			}
		],
		amounts: {
			items_total: 49000,
			shipping_fee: 3000,
			discount: 0,
			total: 52000
		},
		ordered_at: '2024-12-31T09:00:00Z',
		paid_at: '2024-12-31T09:01:00Z'
	},
	{
		id: 'order-4',
		order_number: 'ORD_20251225120000_d6e5f4',
		status: 'CANCELLED',
		orderer: {
			name: '홍길동',
			phone: '010-1234-5678',
			email: 'hong@example.com'
		},
		shipping: {
			recipient: '홍길동',
			phone: '010-1234-5678',
			postal_code: '06000',
			address: '서울특별시 강남구 테헤란로 123',
			address_detail: '456호',
			memo: ''
		},
		items: [
			{
				id: 'item-5',
				product: {
					id: '4',
					name: '크롭 패딩 자켓',
					slug: 'crop-padding-jacket',
					thumbnail_url: 'https://picsum.photos/seed/padding1/400/533'
				},
				option: { color: 'Black', size: 'S' },
				quantity: 1,
				unit_price: 89000,
				subtotal: 89000
			}
		],
		amounts: {
			items_total: 89000,
			shipping_fee: 0,
			discount: 0,
			total: 89000
		},
		ordered_at: '2024-12-25T12:00:00Z'
	}
];

export function getOrderById(id: string): Order | undefined {
	return mockOrders.find(order => order.id === id);
}

export function getOrderByNumber(orderNumber: string): Order | undefined {
	return mockOrders.find(order => order.order_number === orderNumber);
}

export function formatOrderDate(dateString: string): string {
	const date = new Date(dateString);
	return date.toLocaleDateString('ko-KR', {
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});
}

export function formatOrderDateTime(dateString: string): string {
	const date = new Date(dateString);
	return date.toLocaleString('ko-KR', {
		year: 'numeric',
		month: 'long',
		day: 'numeric',
		hour: '2-digit',
		minute: '2-digit'
	});
}

// 주문 취소
export async function cancelOrder(orderId: string, reason?: string): Promise<boolean> {
	const order = mockOrders.find(o => o.id === orderId);

	if (!order) {
		throw new Error('주문을 찾을 수 없습니다.');
	}

	if (order.status !== 'PENDING' && order.status !== 'PAID') {
		throw new Error('취소할 수 없는 주문입니다.');
	}

	// API 호출 시뮬레이션 (0.5초 대기)
	await new Promise(resolve => setTimeout(resolve, 500));

	// Mock 데이터 업데이트
	order.status = 'CANCELLED';
	order.cancelled_at = new Date().toISOString();
	order.cancel_reason = reason;

	return true;
}

// 배송 추적 조회
export async function getDeliveryTracking(orderId: string): Promise<DeliveryTracking[]> {
	const order = mockOrders.find(o => o.id === orderId);

	if (!order) {
		throw new Error('주문을 찾을 수 없습니다.');
	}

	if (!order.shipping.tracking_number) {
		throw new Error('운송장 번호가 없습니다.');
	}

	// API 호출 시뮬레이션 (0.5초 대기)
	await new Promise(resolve => setTimeout(resolve, 500));

	// Mock 배송 추적 데이터
	const mockTracking: Record<string, DeliveryTracking[]> = {
		'order-1': [
			{
				status: 'DELIVERED',
				location: '서울특별시 강남구',
				description: '배송완료',
				timestamp: '2024-12-30T14:00:00Z'
			},
			{
				status: 'OUT_FOR_DELIVERY',
				location: '서울특별시 강남구 배송센터',
				description: '배송 출발',
				timestamp: '2024-12-30T09:30:00Z'
			},
			{
				status: 'IN_TRANSIT',
				location: '서울 물류센터',
				description: '배송지로 이동중',
				timestamp: '2024-12-29T18:00:00Z'
			},
			{
				status: 'IN_TRANSIT',
				location: '경기 고양 물류센터',
				description: '간선 상차',
				timestamp: '2024-12-29T12:00:00Z'
			},
			{
				status: 'IN_TRANSIT',
				location: '판매자',
				description: '상품 인수',
				timestamp: '2024-12-29T09:00:00Z'
			}
		],
		'order-2': [
			{
				status: 'OUT_FOR_DELIVERY',
				location: '경기도 성남시 분당구 배송센터',
				description: '배송 출발',
				timestamp: '2024-12-30T10:00:00Z'
			},
			{
				status: 'IN_TRANSIT',
				location: '경기 성남 물류센터',
				description: '배송지로 이동중',
				timestamp: '2024-12-30T08:00:00Z'
			},
			{
				status: 'IN_TRANSIT',
				location: '판매자',
				description: '상품 인수',
				timestamp: '2024-12-30T09:00:00Z'
			}
		]
	};

	return mockTracking[orderId] || [];
}
